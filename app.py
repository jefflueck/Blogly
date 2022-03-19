"""Blogly application."""

from tkinter import Button
from flask import Flask, render_template,request,redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'A secret key only for me'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.drop_all()
db.create_all()

@app.route('/')
def home_page():
  '''Simple landing page'''
  return render_template('index.html')

@app.route('/list')
def list_page():
  users = User.query.all()
  return render_template('/list.html',users=users)

@app.route('/list', methods=["POST"])
def add_user_page():
  first_name = request.form['first_name']
  last_name = request.form['last_name']
  image_url = request.form['image_url']
  image_url = image_url if image_url else None

  new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
  db.session.add(new_user)
  db.session.commit()
  users = User.query.all()

  return render_template('/list.html', users=users)
