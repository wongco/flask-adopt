from flask import Flask, request, session, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import FlaskForm
from models import db, connect_db, Pet

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
