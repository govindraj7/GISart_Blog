from wsgiref.validate import validator
from flask import Blueprint, redirect, render_template, flash, request, redirect, url_for
from .models import Users, BlogPosts
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from app.extensions.database import db
from werkzeug.security import generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

blueprint = Blueprint('blog_post_pgs', __name__)

# create forms class

# * form for creating a user
class SignUpForm(FlaskForm):
    user_name = StringField("Username:", validators=[DataRequired()])
    first_name = StringField("First Name:", validators=[DataRequired()])
    last_name = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])
    password_hash = PasswordField('Password:', validators=[DataRequired(), EqualTo('password_hash_confirm', message='Passwords must match.')])
    password_hash_confirm = PasswordField('Confirm Password:', validators=[DataRequired()])

    submit = SubmitField("Submit")

# * form for creating a post
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    image = StringField("Image URL", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")
   
# placeholder
@blueprint.route('/user/<username>')
def user(username):
  return render_template('user_pgs/user.html', username=username, title=username)

# ! user signup related
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
  return render_template('user_pgs/signup.html', title='Sign-Up', user_name=user_name, first_name=first_name, last_name=last_name, email=email, form=form, users_db=users_db)

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
      return render_template('user_pgs/success.html', title='Update Details', form=form, users_db=users_db, update_user_info=update_user_info, id=id)

    except:
      flash("Oops. Something went wrong. Try again later.")
    
      users_db = Users.query.order_by(Users.date_added)
      return render_template('user_pgs/update.html', title='Details Updated', form=form, users_db=users_db, update_user_info=update_user_info, id=id)

  else:
    users_db = Users.query.order_by(Users.date_added)
    return render_template('user_pgs/update.html', title='Update Details', form=form, users_db=users_db, update_user_info=update_user_info, id=id)

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
    return render_template('user_pgs/success.html', title='User Deleted', user_name=user_name, form=form, users_db=users_db, delete_user_info=delete_user_info, id=id)

  except:
    flash("Hmmm... Something did not work. Try again later.")
    users_db = Users.query.order_by(Users.date_added)
    return render_template('user_pgs/signup.html', title='Delete User', user_name=user_name, form=form, users_db=users_db, delete_user_info=delete_user_info, id=id)

# todo: log errors?
# todo: sort out slugs

# ! blog post related
# create a post
@blueprint.route('/gisart-gallery/create', methods=["GET", "POST"])
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
    
  return render_template('blog_post_pgs/create_post.html', title='Share Your GISart', form=form)

# todo: change image url place holder to actual images

# view all posts
@blueprint.route('/gisart-gallery/view')
def view_posts():
  # collect posts from db
  posts = BlogPosts.query.order_by(BlogPosts.date_posted)
  return render_template('blog_post_pgs/view_posts.html', title='GISart Gallery', posts=posts)

# view a single post on a page
@blueprint.route('/gisart-gallery/view/<int:id>')
def single_post(id):
  post = BlogPosts.query.get_or_404(id)
  return render_template('blog_post_pgs/single_post.html', post=post, id=post.id)

# deleta a post 
@blueprint.route('/gisart-gallery/delete/<int:id>')
def delete_post(id):
  delete_this_post = BlogPosts.query.get_or_404(id)

  try:
    db.session.delete(delete_this_post)
    db.session.commit()
    flash("Your post was successfully deleted.")
    posts = BlogPosts.query.order_by(BlogPosts.date_posted)
    return render_template('blog_post_pgs/view_posts.html', title='GISart Gallery', posts=posts)

    # redirect issue with flash messages ?? Calls both ??

  except:
    flash('Hmm... Something did not work. Try again later.')
    posts = BlogPosts.query.order_by(BlogPosts.date_posted)
    return render_template('blog_post_pgs/view_posts.html', title='GISart Gallery', posts=posts)


# ! do I want this in the app??
# edit a post
# @blueprint.route('/gisart-gallery/edit/<int:id>', methods=["GET", "POST"])
# def edit_post(id):
#   form = PostForm()
#   post = BlogPosts.query.get_or_404(id)

#   if form.validate_on_submit():
#       post.title = form.title.data 
#       post.image = form.image.data 
#       post.description = form.description.data
#       # update db
#       db.session.add(post)
#       db.session.commit()

#       flash("Post successfully updated!")
#       return redirect(url_for('blog_post_pgs/single_post.html', id=post.id))
  
#   form.title.data = form.title 
#   form.image.data = form.image 
#   form.description.data = form.description
#   return render_template('blog_post_pgs/edit_post.html', title='Edit Post', form=form)


@blueprint.route('/gisart-gallery/edit/<int:id>', methods=["GET", "POST"])
def edit_post(id):
  form = PostForm()
  edit_this_post = BlogPosts.query.get_or_404(id)

  if request.method == "POST":
    edit_this_post.title = request.form['post.title']
    edit_this_post.description = request.form['post.description']

    try:
      db.session.add(edit_this_post)
      db.session.commit()
      flash("Post successfully updated!")
      return redirect(url_for('blog_post_pgs/single_post.html', title='Edit Post', form=form, id=id, edit_this_post=edit_this_post))

    except:
      flash("Oops. Something went wrong. Try again later.")
      return render_template('blog_post_pgs/edit_post.html', title='Edit Post', form=form, edit_this_post=edit_this_post, id=edit_this_post.id)

  else:
    return render_template('blog_post_pgs/edit_post.html', title='Edit Post', form=form, edit_this_post=edit_this_post, id=edit_this_post.id)
