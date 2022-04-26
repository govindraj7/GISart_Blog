from flask import Blueprint, render_template, redirect, url_for

blueprint = Blueprint('basic_pgs', __name__)

# root 
@blueprint.route('/')
# create route decorator
@blueprint.route('/welcome')
def index():
  return render_template('basic_pgs/index.html',  title="Welcome!")

# create route decorator
@blueprint.route('/about')
def about():
  return render_template('basic_pgs/about.html',  title="About")
    # return redirect(url_for('basic_pgs.about')) 
    # redirect kept giving error 404

# create redirect route decorator
@blueprint.route('/inspiration')
def inpsiration():
  return redirect('https://unsplash.com/s/photos/satellite-imagery')