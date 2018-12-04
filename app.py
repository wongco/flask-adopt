from flask import Flask, request, session, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pet
from forms import AddPet, EditPet
from secrets import PETFINDER_API_KEY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)
# app.debug = True

connect_db(app)
db.create_all()


@app.route('/')
def display_homepage():
    """ displays the homepage for the app  """
    pets = Pet.query.all()

    return render_template('/index.html', pets=pets)


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

        # db add & commit stuff from api
        # redirect to homepage after successfully adding pet
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

        flash(f'{ pet.name } details were updated.')

        return redirect(f'/{pet.id}')

    else:
        return render_template('pet_details.html', pet=pet, form=form)
