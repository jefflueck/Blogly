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
