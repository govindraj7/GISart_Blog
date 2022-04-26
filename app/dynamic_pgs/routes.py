from wsgiref.validate import validator
from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

blueprint = Blueprint('dynamic_pgs', __name__)

# create forms class
class SignUpForm(FlaskForm):
    user_name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Sign Up!")

@blueprint.route('/user/<username>')
def user(username):
  return render_template('dynamic_pgs/user.html', username=username, title=username)

@blueprint.route('/signup', methods=["GET", "POST"])
def signup():
  user_name = None
  form = SignUpForm()
  # validate form  
  if form.validate_on_submit():
      user_name = form.user_name.data
      form.user_name.data = ''
  return render_template('dynamic_pgs/signup.html', title='Sign-Up', user_name=user_name, form=form)
