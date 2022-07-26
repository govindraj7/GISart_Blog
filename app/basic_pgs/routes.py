from flask import Blueprint, render_template, redirect, send_file
from flask_cachecontrol import cache, cache_for, dont_cache, Always, ResponseIsSuccessfulOrRedirect

blueprint = Blueprint('basic_pgs', __name__)

# root 
@blueprint.route('/')
# create route decorator
@blueprint.route('/welcome')
@dont_cache()
def index():
  return render_template('basic_pgs/index.html',  title="Welcome!")

# create route decorator
@blueprint.route('/about')
@dont_cache()
def about():
  return render_template('basic_pgs/about.html',  title="About")

# create redirect route decorator
@blueprint.route('/inspiration')
def inspiration():
  return redirect('https://unsplash.com/s/photos/satellite-imagery')

# placeholder for download file
@blueprint.route('/download')
def download():
  return send_file('static/downloads/info-sheet.txt', as_attachment=True)