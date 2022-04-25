from flask import Blueprint, render_template

blueprint = Blueprint('dynamic_pgs', __name__)

@blueprint.route('/user/<username>')
def user(username):
  return render_template('dynamic_pgs/user.html', username=username, title=username)
