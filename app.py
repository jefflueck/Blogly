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
  return render_template('list.html', users=users)

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

  return render_template('list.html', new_user=new_user, users=users)

@app.route('/details/<int:user_id>')
def show_details(user_id):
  user = User.query.get_or_404(user_id)
  return render_template('details.html', user=user)

@app.route('/edit/<int:user_id>')
def pull_user(user_id):

  user = User.query.get_or_404(user_id)
  # first_name = request.form['first_name']
  # last_name = request.form['last_name']
  # image_url = request.form['image_url']
  # image_url = image_url if image_url else None

  # db.session.add_all(user,first_name,last_name,image_url)
  # db.session.commit()


  return render_template('edit.html', user=user)

@app.route('/edit/<int:user_id>', methods=["POST"])
def update_user(user_id):
  user = User.query.get_or_404(user_id)

  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image_url = request.form['image_url']


  db.session.add(user)
  db.session.commit()

  return redirect('/list')


@app.route('/delete/<int:user_id>')
def delete_user(user_id):
  user = User.query.get_or_404(user_id)
  # db.session(user).delete()
  # db.session.commit()

  return render_template('delete.html', user=user)


@app.route('/delete/<int:user_id>', methods=["POST"])
def confirm_delete(user_id):
  user = User.query.get_or_404(user_id)

  db.session().delete(user)
  db.session.commit()

  return redirect('/list')


