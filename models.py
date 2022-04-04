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

  posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')



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

  # users = db.relationship('User', backref=db.backref('posts'))


class Tag(db.Model):
  '''Tags'''

  __tablename__ = "tags"

  id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)

  name = db.Column(db.Text,
                      nullable=False, unique=True)

  posts = db.relationship('Post', secondary='post_tags', backref=db.backref('tags'))

class PostTag(db.Model):
  '''PostTags'''

  __tablename__ = "post_tags"

  post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
  tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
