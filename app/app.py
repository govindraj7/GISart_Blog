from flask import Flask, render_template, url_for
from . import basic_pgs, dynamic_pgs

# create flask instance
def create_app():
  app = Flask(__name__)
  app.config.from_object('app.config')

  register_blueprints(app)

  @app.errorhandler(404)    # invalid URL
  def page_not_found(e):
    return render_template("404.html"), 404

  @app.errorhandler(500)    # internal server error
  def page_not_working(e):
    return render_template("500.html"), 500

  return app

# Blueprints
def register_blueprints(app: Flask):
  app.register_blueprint(basic_pgs.routes.blueprint)
  app.register_blueprint(dynamic_pgs.routes.blueprint)
