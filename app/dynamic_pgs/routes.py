from wsgiref.validate import validator
from flask import Blueprint, redirect, render_template, flash, request
from .models import Users, BlogPosts
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from app.extensions.database import db
from werkzeug.security import generate_password_hash

blueprint = Blueprint('dynamic_pgs', __name__)

# create forms class
class SignUpForm(FlaskForm):
    user_name = StringField("Username:", validators=[DataRequired()])
    first_name = StringField("First Name:", validators=[DataRequired()])
    last_name = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    password_hash = PasswordField('Password:', validators=[DataRequired(), EqualTo('password_hash_confirm', message='Passwords must match.')])
    password_hash_confirm = PasswordField('Confirm Password:', validators=[DataRequired()])

    submit = SubmitField("Submit")

class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    image = StringField("Image URL", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")
   
# placeholder
@blueprint.route('/user/<username>')
def user(username):
  return render_template('dynamic_pgs/user.html', username=username, title=username)

# add db record
@blueprint.route('/signup', methods=["GET", "POST"])
def signup():
  user_name = None
  first_name = None
  last_name = None
  email = None

  form = SignUpForm()
  # validate form  
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user is None:
      hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
      user = Users(user_name=form.user_name.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, password_hash=hashed_pw)
      db.session.add(user)
      db.session.commit()
    user_name = form.user_name.data
    
    # clear the form
    form.user_name.data = ''
    form.first_name.data = ''
    form.last_name.data = ''
    form.email.data = ''
    form.password_hash.data = ''

    flash("You are now part of the GISart Community.")

  users_db = Users.query.order_by(Users.date_added)
  return render_template('dynamic_pgs/signup.html', title='Sign-Up', user_name=user_name, first_name=first_name, last_name=last_name, email=email, form=form, users_db=users_db)

# update db record
@blueprint.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
  form = SignUpForm()
  update_user_info = Users.query.get_or_404(id)

  if request.method == "POST":
    update_user_info.user_name = request.form['user_name']
    update_user_info.first_name = request.form['first_name']
    update_user_info.last_name = request.form['last_name']
    update_user_info.email = request.form['email']

    try:
      db.session.commit()
      flash("Your details are Updated!")
    
      users_db = Users.query.order_by(Users.date_added)
      return render_template('dynamic_pgs/success.html', title='Update Details', form=form, users_db=users_db, update_user_info=update_user_info, id=id)

    except:
      flash("Oops. Something went wrong. Try again later.")
    
      users_db = Users.query.order_by(Users.date_added)
      return render_template('dynamic_pgs/update.html', title='Details Updated', form=form, users_db=users_db, update_user_info=update_user_info, id=id)

  else:
    users_db = Users.query.order_by(Users.date_added)
    return render_template('dynamic_pgs/update.html', title='Update Details', form=form, users_db=users_db, update_user_info=update_user_info, id=id)

# delete db record
@blueprint.route('/delete/<int:id>')
def delete(id):
  user_name = None
  form = SignUpForm()
  delete_user_info = Users.query.get_or_404(id)

  try: 
    db.session.delete(delete_user_info)
    db.session.commit()
    flash("User Deleted Successfully.")
    users_db = Users.query.order_by(Users.date_added)
    return render_template('dynamic_pgs/success.html', title='User Deleted', user_name=user_name, form=form, users_db=users_db, delete_user_info=delete_user_info, id=id)

  except:
    flash("Hmmm... Something did not work. Try again later.")
    users_db = Users.query.order_by(Users.date_added)
    return render_template('dynamic_pgs/signup.html', title='Delete User', user_name=user_name, form=form, users_db=users_db, delete_user_info=delete_user_info, id=id)

# todo: log errors?
# todo: sort out slugs

# add post
@blueprint.route('/create-post', methods=["GET", "POST"])
def create_post():
  form = PostForm()

  if form.validate_on_submit():
    post = BlogPosts(title=form.title.data, image=form.image.data, description=form.description.data)
    # clear the form
    form.title.data = ''
    form.image.data = ''
    form.description.data = ''

    db.session.add(post)
    db.session.commit()

    flash("Post successfully created!")
    
  return render_template('dynamic_pgs/create_post.html', title='Share Your GISart', form=form)

# todo: change image url place holder to actual images

@blueprint.route('/gisart-gallery')
def view_posts():
  # collect posts from db
  posts = BlogPosts.query.order_by(BlogPosts.date_posted)
  return render_template('dynamic_pgs/view_posts.html', title='GISart Gallery', posts=posts)

# @blueprint.route('/gisart/<int:id>')
@blueprint.route('/gisart-gallery/<int:id>')
def single_post(id):
  post = BlogPosts.query.get_or_404(id)
  return render_template('dynamic_pgs/single_post.html', post=post, id=id)
