from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, RadioField
from wtforms.validators import InputRequired, Optional, URL, AnyOf, NumberRange


class AddPet(FlaskForm):
    """ Form for adding an available pet """

    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField(
        "Species",
        validators=[
            AnyOf(['cat', 'dog', 'porcupine'],
                  message="Please input cat, dog or porcupine"),
            InputRequired()
        ])
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    age = IntegerField(
        "Age",
        validators=[
            InputRequired(),
            NumberRange(
                min=0, max=30, message="Please input an age between 0 and 30")
        ])
    notes = StringField("Notes")


class EditPet(FlaskForm):
    """ Form for editing pet information """

    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = StringField("Notes")
    available = BooleanField("Available")


class FindPet(FlaskForm):
    """ Form for searching for a new pet from PetFinder """

    age = RadioField('Age', choices=[('any', 'Any'), ('Baby', 'Baby'), (
        'Young', 'Young'), ('Adult', 'Adult'), ('Senior', 'Senior')])
    species = RadioField('Species', choices=[('any', 'Any'), ('barnyard', 'Barnyard'), ('bird', 'Bird'), (
        'cat', 'Cat'), ('dog', 'Dog'), ('horse', 'Horse'), ('reptile', 'Reptile'), ('smallfurry', 'Smallfurry')])
