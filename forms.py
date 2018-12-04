from flask_wtf import FlaskForm
from flask_debugtoolbar import DebugToolbarExtension


class AddSnackForm(FlaskForm):
    """Form for adding snacks."""

    name = StringField("Snack Name")
    price = FloatField("Price in USD")
