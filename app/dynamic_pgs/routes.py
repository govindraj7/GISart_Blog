from flask import Blueprint, redirect, render_template, flash, request, redirect, url_for
from .models import Users, BlogPosts
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from app.extensions.database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

blueprint = Blueprint('dynamic_pgs', __name__)

# ! /////////// flash & error msgs must be fixed - issues on redirect url_for

# create forms class

# * form for creating a user
class SignUpForm(FlaskForm):
    user_name = StringField("Username:", validators=[DataRequired()])
    password_hash = PasswordField('Password:', validators=[DataRequired(), EqualTo('password_hash_confirm', message='Passwords must match.')])
    password_hash_confirm = PasswordField('Confirm Password:', validators=[DataRequired()])

    submit = SubmitField("Submit")

# * form for creating a post
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    image = StringField("Image URL", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")
   
# * form for login
class LoginForm(FlaskForm):
    user_name = StringField("Username:", validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), EqualTo('password_hash_confirm', message='Passwords must match.')])
    submit = SubmitField("Submit")

# ! user signup related
# add db record
@blueprint.route('/signup', methods=["GET", "POST"])
def signup():
  user_name = None
  form = SignUpForm()

  # validate form  
  if form.validate_on_submit():
    
    user = Users.query.filter_by(user_name=form.user_name.data).first()
    if user is None:
      try:
        hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
        user = Users(user_name=form.user_name.data, password_hash=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('dynamic_pgs.dashboard'))

      except:
          # flash("Username already exists")
          return redirect(url_for('dynamic_pgs.signup'))
    
    # clear the form
    form.user_name.data = ''
    form.password_hash.data = ''
  return render_template('user_pgs/signup.html', title='Sign-Up', user_name=user_name, form=form)

# update db record
@blueprint.route('/update/<int:id>', methods=["GET", "POST"])
@login_required
def update(id):
  form = SignUpForm()
  update_user_info = Users.query.get_or_404(id)

  if request.method == "POST":
    update_user_info.user_name = request.form['user_name']

    try:
      db.session.commit()
      # flash("Your details are Updated!")
      return redirect(url_for('dynamic_pgs.dashboard'))

    except:
      # flash("Oops. Something went wrong. Try again later.")
      return redirect(url_for('dynamic_pgs.signup'))

  else:
    return render_template('user_pgs/update.html', title='Update Details', form=form, update_user_info=update_user_info, id=id)

# delete db record
@blueprint.route('/delete/<int:id>')
@login_required
def delete(id):
  user_name = None
  form = SignUpForm()
  delete_user_info = Users.query.get_or_404(id)

  try: 
    db.session.delete(delete_user_info)
    db.session.commit()
    # flash("User Deleted Successfully.")
    return redirect(url_for('dynamic_pgs.signup'))

  except:
    # flash("Hmmm... Something did not work. Try again later.")
    return render_template('user_pgs/signup.html', title='Delete User', user_name=user_name, form=form, delete_user_info=delete_user_info, id=id)

# todo: log errors?
# todo: sort out slugs

# login pg
@blueprint.route('/login', methods=["GET", "POST"])
def login():
  # error = None
  form = LoginForm()
  user = Users.query.filter_by(user_name=form.user_name.data).first()
  if not user or not check_password_hash(user.password_hash, form.password.data):
    # error = 'Please check your login in details and try again.'
    return render_template('user_pgs/login.html', title='Login', form=form)
  login_user(user)
  return redirect(url_for('dynamic_pgs.dashboard'))

@blueprint.get('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dynamic_pgs.login'))

# dashboard
@blueprint.route('/dashboard', methods=["GET", "POST"])
@login_required
def dashboard():
  return render_template('user_pgs/dashboard.html', title='User Dashboard')

# ! blog post related
# create a post
@blueprint.route('/gisart-gallery/create', methods=["GET", "POST"])
@login_required
def create_post():
  form = PostForm()

  if form.validate_on_submit():
    # one-to-many relationship
    author = current_user.id
    post = BlogPosts(title=form.title.data, image=form.image.data, description=form.description.data, author_id=author)
    # clear the form
    form.title.data = ''
    form.image.data = ''
    form.description.data = ''

    db.session.add(post)
    db.session.commit()
    return redirect(url_for('dynamic_pgs.view_posts'))
    # flash("Post successfully created!")
    
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
@login_required
def delete_post(id):
  delete_this_post = BlogPosts.query.get_or_404(id)

  try:
    db.session.delete(delete_this_post)
    db.session.commit()
    # flash("Your post was successfully deleted.")
    return redirect(url_for('dynamic_pgs.view_posts'))
    # redirect issue with flash messages ?? Calls both ??

  except:
    # flash('Hmm... Something did not work. Try again later.')
    return redirect(url_for('dynamic_pgs.view_posts'))

# ! do I want this in the app??
@blueprint.route('/gisart-gallery/edit/<int:id>', methods=["GET", "POST"])
@login_required
def edit_post(id):
  form = PostForm()
  edit_this_post = BlogPosts.query.get_or_404(id)

  if request.method == "POST":
    edit_this_post.title = request.form['title']
    edit_this_post.description = request.form['description']

    try:
      db.session.add(edit_this_post)
      db.session.commit()
      # flash("Post successfully updated!")
      return redirect(url_for('dynamic_pgs.view_posts'))
      # todo: fix this redirect

    except:
      # flash("Oops. Something went wrong. Try again later.")
      return render_template('blog_post_pgs/edit_post.html', title='Edit Post', form=form, edit_this_post=edit_this_post, id=edit_this_post.id)

  else:
    return render_template('blog_post_pgs/edit_post.html', title='Edit Post', form=form, edit_this_post=edit_this_post, id=edit_this_post.id)
