"""Blogly application."""

from flask import Flask, render_template,request,redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag, DEFAULT_URL
import datetime;
# DEFAULT_URL = 'https://pngimg.com/uploads/snoopy/snoopy_PNG82.png'

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

  return render_template('edit.html', user=user)

@app.route('/edit/<int:user_id>', methods=["POST"])
def update_user(user_id):
  user = User.query.get_or_404(user_id)

  user.first_name = request.form['first_name']
  user.last_name = request.form['last_name']
  user.image_url = request.form['image_url'] or DEFAULT_URL

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

@app.route('/post/<int:user_id>')
def show_post_form(user_id):
  user = User.query.get_or_404(user_id)
  return render_template('post.html', user=user)

@app.route('/post/<int:user_id>', methods=["POST"])
def submit_post(user_id):
  user = User.query.get_or_404(user_id)

  title = request.form['title']
  content = request.form['content']
  created_at = datetime.datetime.now()


  new_post = Post(title=title, content=content, created_at=created_at, user_id=user_id)

  db.session.add(new_post)
  db.session.commit()
  return render_template('details.html', user=user, new_post=new_post)

@app.route('/delete/post/<int:post_id>')
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  # db.session(user).delete()
  # db.session.commit()

  return render_template('delete_post.html', post=post)


# @app.route('/delete/post/<int:post_id>', methods=["POST"])
# def confirm_delete_post(post_id):
#   post = Post.query.get_or_404(post_id)

#   db.session().delete(post)
#   db.session.commit()

#   user = User.query.get_or_404(post.user_id)
#   return redirect('/details/post' + str(user.id))

@app.route('/view/post/<int:post_id>')
def view_post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('view_post.html', post=post)

@app.route('/edit/post/<int:post_id>')
def edit_post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('edit_post.html', post=post)

@app.route('/edit/post/<int:post_id>', methods=["POST"])
def submit_post_update(post_id):
  post = Post.query.get_or_404(post_id)

  post.title = request.form['title']
  post.content = request.form['content']
  post.created_at = datetime.datetime.now()



  db.session.add(post)
  db.session.commit()
  user = User.query.get_or_404(post.user_id)
  return redirect('/details/' + str(user.id))

@app.route('/tags')
def show_tag():
  tags = Tag.query.all()
  return render_template('tags.html', tags=tags)

@app.route('/add_tag')
def form_add_tag():
  # name = request.form['name']
  # new_tag = Tag(name=name)
  # db.session.add(new_tag)
  # db.session.commit()
  return render_template('add_tag.html')

@app.route('/add_tag', methods=["POST"])
def add_tag():
  name = request.form['name']
  new_tag = Tag(name=name)
  db.session.add(new_tag)
  db.session.commit()
  return redirect('/tags')

# @classmethod

# def __repr__(self):
#     u = self
#     return f"<User id={u.id} first_name={u.first_name} last_name={u.last_name}>"

