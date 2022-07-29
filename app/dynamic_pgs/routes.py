#* routes for dynamics pgs >> user specific content >> linked to db ------------------------------------------------------------------------------------------------------------------------
# for routes
from flask import Blueprint, redirect, render_template, flash, request, redirect, url_for
# models of db
from .models import Users, BlogPosts
from app.extensions.database import db
from sqlalchemy import desc, true
from slugify import slugify
# flask forms + login
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import TextArea
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

#! AWS S3 ------------------------------------------------------------------------------------------------------------------------
# postgressql does not support blobs, so AWS S3 is used to store imgs & generate img url which is stored in db
from app.config import S3_KEY, S3_SECRET, S3_LOCATION, S3BASEURL, S3_BUCKET, ALLOWED_EXTENSIONS
import boto3
s3_client = boto3.client('s3', 
  aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET,
   region_name=S3_LOCATION
   )

#*AWS S3 for blog post images
# store img from AWS S3 Bucket
def s3_upload(data, name):
  try:
    upload_file_response = s3_client.put_object(Body=data,
                                             Bucket=S3_BUCKET,
                                             Key=name,
                                             ContentType='image/jpeg')
    print(f" ** Response - {upload_file_response}")
  except Exception as e:
        print("Something Happened: ", e)
        return e

# delete img from AWS S3 Bucket
def s3_remove(name):
  try:
    delete_file_response = s3_client.delete_object(
                                              Bucket=S3_BUCKET,
                                              Key=name)
    print(f" ** Response - {delete_file_response}")
  except Exception as e:
          print("Something Happened: ", e)
          return e

# to try ensure only an img file is submitted
def allowed_img_type(image_type):
  if not "." in image_type:
    return False

  ext = image_type.rsplit(".", 1)[1]

  if ext.lower() in ALLOWED_EXTENSIONS:
    return True
  else:
    return False
  

# todo: log errors? flash & error msgs must be fixed - issues on redirect url_for

blueprint = Blueprint('dynamic_pgs', __name__)

#! create forms class ------------------------------------------------------------------------------------------------------------------------

#* form for creating a user
class SignUpForm(FlaskForm):
    user_name = StringField("Username:", validators=[DataRequired()])
    file = FileField("Choose a Profile Picture", validators=[DataRequired()])
    bio = TextAreaField("Short Bio:")
    password_hash = PasswordField('Password:', validators=[DataRequired(), EqualTo('password_hash_confirm', message='Passwords must match.')])
    password_hash_confirm = PasswordField('Confirm Password:', validators=[DataRequired()])

    submit = SubmitField("Submit")

#* form for creating a post
class PostForm(FlaskForm):
    file = FileField("File Please", validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()], widget=TextArea())
    submit = SubmitField("Submit")
   
#* form for login
class LoginForm(FlaskForm):
    user_name = StringField("Username:", validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired(), EqualTo('password_hash_confirm', message='Passwords must match.')])
    submit = SubmitField("Submit")

#! user signup related ------------------------------------------------------------------------------------------------------------------------

# add db record
@blueprint.route('/signup', methods=["GET", "POST"])
def signup():
  user_name = None
  form = SignUpForm()

  if form.validate_on_submit():
    image = request.files["file"]
    image_size = len(form.file.data)
    max_size = 1024 * 1000 * 5
    if image_size > max_size:
      flash("File size is too large, 5MB is the limit.")
      return redirect(request.url)
    # ensure only an image file is submitted
    if image.filename == "":
      flash("File must have a name.")
      return redirect(request.url)
    if not allowed_img_type(image.filename):
      flash("That file format is not supported. Try png, jpg or jpeg.")
      return redirect(request.url)
    else:
      user = Users.query.filter_by(user_name=form.user_name.data).first()
      if user is None:
        try:
          # postgressql does not support blobs, so AWS S3 is used to store imgs & generate img url which is stored in db
          s3_upload(form.file.data, form.user_name.data)
          hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
          user = Users(user_name=form.user_name.data, profile_pic=S3BASEURL+form.user_name.data, bio=form.bio.data, password_hash=hashed_pw)
          db.session.add(user)
          db.session.commit()
          return redirect(url_for('dynamic_pgs.dashboard'))

        except:
            flash("Username already exists")
            return redirect(url_for('dynamic_pgs.signup'))
      
    # clear the form
    form.user_name.data = ''
    form.bio.data = ''
    form.password_hash.data = ''
  return render_template('user_pgs/signup.html', title='Sign-Up', user_name=user_name, form=form)

#* update db record
@blueprint.route('/update/<slug>/<int:id>', methods=["GET", "POST"])
@login_required
def update(id, slug):
  form = SignUpForm()
  update_user_info = Users.query.get_or_404(id)
  form.user_name.data = update_user_info.user_name
  form.bio.data = update_user_info.bio

  if request.method == "POST":
    update_user_info.user_name = request.form['user_name']
    update_user_info.bio = request.form['bio']
    update_user_info.slug = slugify(request.form['user_name'])

    try:
      db.session.commit()
      # flash("Your details are Updated!")
      return redirect(url_for('dynamic_pgs.dashboard'))

    except:
      # flash("Oops. Something went wrong. Try again later.")
      return redirect(url_for('dynamic_pgs.signup'))

  else:
    return render_template('user_pgs/update.html', title='Update Details', form=form, update_user_info=update_user_info, id=id, slug=slug)

#* delete db record
@blueprint.route('/delete/<slug>/<int:id>')
@login_required
def delete(id, slug):
  user_name = None
  form = SignUpForm()
  delete_user_info = Users.query.get_or_404(id)

  try: 
    db.session.delete(delete_user_info)
    db.session.commit()
    flash("User Deleted Successfully.")
    return redirect(url_for('dynamic_pgs.signup'))

  except:
    flash("Hmmm... Something did not work. Try again later.")
    return render_template('user_pgs/signup.html', title='Delete User', user_name=user_name, form=form, delete_user_info=delete_user_info, id=id, slug=slug)

#* login pg
@blueprint.route('/login', methods=["GET", "POST"])
def login():
  form = LoginForm()
  user = Users.query.filter_by(user_name=form.user_name.data).first()
  if not user or not check_password_hash(user.password_hash, form.password.data):
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

#! blog post related ------------------------------------------------------------------------------------------------------------------------
# create a post
@blueprint.route('/gisart-gallery/create', methods=["GET", "POST"])
@login_required
def create_post():
  form = PostForm()
  
  if form.validate_on_submit():
    image = request.files["file"]
    image_size = len(form.file.data)
    max_size = 1024 * 1000 * 5
    if image_size > max_size:
      flash("File size is too large, 5MB is the limit.")
      return redirect(request.url)
    # ensure only an image file is submitted
    if image.filename == "":
      flash("File must have a name.")
      return redirect(request.url)
    if not allowed_img_type(image.filename):
      flash("That file format is not supported. Try png, jpg or jpeg.")
      return redirect(request.url)
    # postgressql does not support blobs, so AWS S3 is used to store imgs & generate img url which is stored in db
    s3_upload(form.file.data, form.title.data)
    # one-to-many relationship
    author = current_user.id
    post = BlogPosts(title=form.title.data, image=S3BASEURL+form.title.data, description=form.description.data, author_id=author)

    db.session.add(post)
    db.session.commit()

    # clear the form
    form.title.data = ''
    form.description.data = ''
    flash("Post successfully created!")
    return redirect(url_for('dynamic_pgs.view_posts'))
      
  return render_template('blog_post_pgs/create_post.html', title='Share Your GISart', form=form)


#*view all posts
@blueprint.route('/gisart-gallery/view')
def view_posts():
  # collect posts from db
  posts = BlogPosts.query.order_by(BlogPosts.date_posted.desc())
  return render_template('blog_post_pgs/view_posts.html', title='GISart Gallery', posts=posts)

#* view a single post on a page
@blueprint.route('/gisart-gallery/view/<slug>/<int:id>')
def single_post(id, slug):
  post = BlogPosts.query.get_or_404(id)
  return render_template('blog_post_pgs/single_post.html', post=post, id=post.id, slug=post.slug)

#* deleta a post 
@blueprint.route('/gisart-gallery/delete/<slug>/<int:id>')
@login_required
def delete_post(id, slug):
  delete_this_post = BlogPosts.query.get_or_404(id)
  id = current_user.id
  if id == delete_this_post.author.id or id == 1:
    try:
      s3_remove(delete_this_post.title)
      db.session.delete(delete_this_post)
      db.session.commit()
      flash("Your post was successfully deleted.")
      return redirect(url_for('dynamic_pgs.view_posts'))

    except:
      flash('Hmm... Something did not work. Try again later.')
      return redirect(url_for('dynamic_pgs.view_posts'))
  else:
    flash('Unauthorized.')
    return redirect(url_for('dynamic_pgs.view_posts'))

@blueprint.route('/gisart-gallery/edit/<slug>/<int:id>', methods=["GET", "POST"])
@login_required
def edit_post(id, slug):
  form = PostForm()
  edit_this_post = BlogPosts.query.get_or_404(id)
  id = current_user.id

  if id == edit_this_post.author.id or id == 1:
    form.title.data  = edit_this_post.title 
    form.description.data = edit_this_post.description
    if request.method == "POST":
      edit_this_post.title = request.form['title']
      edit_this_post.description = request.form['description']
      edit_this_post.slug = slugify(request.form['title'])

      try:
        db.session.add(edit_this_post)
        db.session.commit()
        flash("Post successfully updated!")
        return redirect(url_for('dynamic_pgs.view_posts'))
        # todo: fix this redirect

      except:
        flash("Oops. Something went wrong. Try again later.")
        return render_template('blog_post_pgs/edit_post.html', title='Edit Post', form=form, edit_this_post=edit_this_post, id=edit_this_post.id, slug=edit_this_post.slug)

    else:
      return render_template('blog_post_pgs/edit_post.html', title='Edit Post', form=form, edit_this_post=edit_this_post, id=edit_this_post.id, slug=edit_this_post.slug)
  else:
    flash('Unauthorized.')
    return redirect(url_for('dynamic_pgs.view_posts'))

#* the chosen one
@blueprint.route('/admin', methods=["GET", "POST"])
@login_required
def admin():
  id = current_user.id
  if id == 1:
    all_users = Users.query.order_by(Users.date_added)
    return render_template('admin/admin.html', all_users=all_users, id=id)
  else:
    flash('Unauthorized.')
    return redirect(url_for('dynamic_pgs.dashboard'))
