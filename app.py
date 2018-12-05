from flask import Flask, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPet, EditPet, FindPet
from petfinder_api_requests import get_random_pet, get_filtered_pets
from random import randint
from secret import FLASK_SECRET_KEY, POSTGRES_DB_PATH

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = POSTGRES_DB_PATH
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = FLASK_SECRET_KEY
debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()


def create_random_pet():
    """Call get_random_pet from API and save to database and return pet instance"""

    pet_data = get_random_pet()
    new_pet = Pet(
        name=pet_data['name'],
        species=pet_data['species'],
        photo_url=pet_data['photo_url'],
        age=pet_data['age'],
        notes=pet_data['notes'])
    db.session.add(new_pet)
    db.session.commit()

    return new_pet


@app.route('/')
def display_homepage():
    """ displays the homepage for the app  """

    pets_available = Pet.query.filter_by(available=True).all()
    pets_owned = Pet.query.filter_by(available=False).all()
    random_pet = pets_available[randint(0, len(pets_available) - 1)]

    # random_pet = create_random_pet()

    return render_template('/pet_display.html', pets_owned=pets_owned, pets_available=pets_available, random_pet=random_pet)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """ Pet add form; handle adding. """

    form = AddPet()

    # POST Handling
    if form.validate_on_submit():

        # create copy of form dict
        new_pet_attr = dict(form.data)
        # remove csrf_token from pet attributes
        del new_pet_attr['csrf_token']
        # unpack dict properties as keyword arguments for Pet Creation
        new_pet = Pet(**new_pet_attr)

        db.session.add(new_pet)
        db.session.commit()

        flash(f"{ new_pet.name } was added to the database!")

        return redirect('/')

    else:
        return render_template('pet_addform.html', form=form)


@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def edit_pet(pet_id):
    """ Pet edit form: handle editing. """

    pet = Pet.query.get_or_404(pet_id)
    form = EditPet(obj=pet)

    # POST Handling
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()

        flash(f"{ pet.name }'s details were updated.")

        return redirect(f'/{pet.id}')

    else:
        return render_template('pet_details.html', pet=pet, form=form)


@app.route('/search', methods=['GET', 'POST'])
def search_pet():
    """ Pet search form: handle searching. """

    form = FindPet()

    # POST Handling
    if form.validate_on_submit():
        # create copy of form dict
        pet_search_attr = dict(form.data)
        # remove csrf_token from pet attributes
        del pet_search_attr['csrf_token']

        # unpack dict properties as keyword arguments for Pet Search
        pet = get_filtered_pets(**pet_search_attr)

        # save pet to session
        session['pet'] = pet
        return redirect('/results')

    else:
        return render_template('pet_search.html', form=form)


@app.route('/results', methods=['GET'])
def display_pets_found():
    """ Pet search results: handles displaying. """

    # retrieve session data for info about pets, send to render
    pet = session['pet']

    return render_template('pet_results.html', pet=pet)
