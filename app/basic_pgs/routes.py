from flask import Blueprint, render_template, redirect

blueprint = Blueprint('basic_pgs', __name__)

# root 
@blueprint.route('/')
# create route decorator
@blueprint.route('/welcome')
def index():
  return render_template('basic_pgs/index.html',  title="Welcome!")

# custom error handling 404

# create redirect route decorator
@blueprint.route('/inspiration')
def inpsiration():
  return redirect('https://unsplash.com/s/photos/satellite-imagery')