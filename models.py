"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_URL = 'https://pngimg.com/uploads/snoopy/snoopy_PNG82.png'

def connect_db(app):
  db.app = app
  db.init_app(app)

class User(db.Model):
  '''User'''
  __tablename__= "users"

  id = db.Column(db.Integer,
                  primary_key=True,
                  autoincrement=True)

  first_name = db.Column(db.Text,
                    nullable=False)

  last_name = db.Column(db.Text,
                    nullable=False)

  image_url = db.Column(db.Text,
                    nullable=True, default=DEFAULT_URL)



class Post(db.Model):
  '''Posts'''

  __tablename__ = "posts"

  id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

  title = db.Column(db.Text,
                      nullable=False, default='No Title')

  content = db.Column(db.Text,
                      nullable=False)

  created_at = db.Column(db.Text, nullable=False)

  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  user = db.relationship('User', backref=db.backref('posts'))
