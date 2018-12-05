from flask import Flask, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPet, EditPet
from petfinder_api_requests import get_random_pet
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
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data

        new_pet = Pet(
            name=name,
            species=species,
            photo_url=photo_url,
            age=age,
            notes=notes)

        db.session.add(new_pet)
        db.session.commit()

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
