from flask import Blueprint, render_template, flash
from .models import Users
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from app.extensions.database import db

blueprint = Blueprint('dynamic_pgs', __name__)

# create forms class
class SignUpForm(FlaskForm):
    user_name = StringField("Decide on a Username?", validators=[DataRequired()])
    first_name = StringField("First Name:", validators=[DataRequired()])
    last_name = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])

    # password placeholder
    # password = PasswordField("Password Please", validators=[DataRequired()])
    submit = SubmitField("Sign Up!")

@blueprint.route('/user/<username>')
def user(username):
  return render_template('dynamic_pgs/user.html', username=username, title=username)

@blueprint.route('/signup', methods=["GET", "POST"])
def signup():
  user_name = None
  first_name = None
  last_name = None
  email = None

  # password = None
  form = SignUpForm()
  # validate form  
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email.data).first()
    if user is None:
      user = Users(user_name=form.user_name.data, first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
      db.session.add(user)
      db.session.commit()
    user_name = form.user_name.data
    form.user_name.data = form

    form.user_name.data = ''
    form.first_name.data = ''
    form.last_name.data = ''
    form.email.data = ''
    # form.password.data = ''
    flash("You are now part of the GISart Community.")

  testing_db = Users.query.order_by(Users.date_added)
  return render_template('dynamic_pgs/signup.html', title='Sign-Up', user_name=user_name, first_name=first_name, last_name=last_name, email=email, form=form, testing_db=testing_db)
# TODO: secure password + sessions