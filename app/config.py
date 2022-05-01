# load the environmernt variables
from dotenv import load_dotenv
load_dotenv()

# db variable from .env
from os import environ
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
# DATABASE_URL=sqlite:///users.db

# super secret key
SECRET_KEY = environ.get('SECRET_KEY')
