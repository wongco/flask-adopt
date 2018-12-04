from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """ Pet potentially for adoption Model """

    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text, nullable=True)
    age = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    available = db.Column(db.Boolean, nullable=False, default=True)


# Create a single model, Pet. This models a pet potentially available for adoption:

#     # id: auto-incrementing integer
#     # name: text, required
#     # species: text, required
#     # photo_url: text, optional
#     # age: integer, required
#     # notes: text, optional
# # available: true/false, required, should default to available
# While setting up the project, add the Debug Toolbar.
