from flask import Blueprint, render_template, flash, request
from .models import Users
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from app.extensions.database import db

blueprint = Blueprint('dynamic_pgs', __name__)

# create forms class
class SignUpForm(FlaskForm):
    user_name = StringField("Username:", validators=[DataRequired()])
    first_name = StringField("First Name:", validators=[DataRequired()])
    last_name = StringField("Surname:", validators=[DataRequired()])
    email = StringField("Email:", validators=[DataRequired()])

    # password placeholder
    # password = PasswordField("Password Please", validators=[DataRequired()])
    submit = SubmitField("Submit")

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
    # form.user_name.data = form

    form.user_name.data = ''
    form.first_name.data = ''
    form.last_name.data = ''
    form.email.data = ''
    # form.password.data = ''
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
      return render_template('dynamic_pgs/update.html', title='Update Details', form=form, users_db=users_db, update_user_info=update_user_info, id=id)

    except:
      flash("Oops. Something went wrong. Try again later.")
    
      users_db = Users.query.order_by(Users.date_added)
      return render_template('dynamic_pgs/update.html', title='Update Details', form=form, users_db=users_db, update_user_info=update_user_info, id=id)

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
    return render_template('dynamic_pgs/signup.html', title='Delete User', user_name=user_name, form=form, users_db=users_db, delete_user_info=delete_user_info, id=id)

  except:
    flash("Hmmm... Something did not work. Try again later.")
    users_db = Users.query.order_by(Users.date_added)
    return render_template('dynamic_pgs/signup.html', title='Delete User', user_name=user_name, form=form, users_db=users_db, delete_user_info=delete_user_info, id=id)


# TODO: secure password + sessions