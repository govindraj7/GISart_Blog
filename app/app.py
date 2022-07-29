from flask import Flask, render_template, url_for
from app.extensions.database import db, migrate
from . import basic_pgs, dynamic_pgs
from app.extensions.authentications import login_manager

# create flask instance
def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config')

  register_extensions(app)
  register_blueprints(app)
  
  @app.errorhandler(404)    # invalid URL
  def page_not_found(e):
    return render_template("404.html"), 404

  @app.errorhandler(500)    # internal server error
  def page_not_working(e):
    return render_template("500.html"), 500

  return app

# blueprints
def register_blueprints(app: Flask):
  app.register_blueprint(basic_pgs.routes.blueprint)
  app.register_blueprint(dynamic_pgs.routes.blueprint)

#  extensions
def register_extensions(app: Flask):
  db.init_app(app)
  migrate.init_app(app, db)
  login_manager.init_app(app)