from os import environ
import pytest
from app.app import create_app
from flask_migrate import upgrade

# test the routes and db - warings are not errors

@pytest.fixture
def client():
  environ['DATABASE_URL'] = 'sqlite://'
  app = create_app()

  with app.app_context():
    upgrade()
    yield app.test_client()