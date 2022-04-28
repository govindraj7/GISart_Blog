from dotenv import load_dotenv
load_dotenv()

from os import environ
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

SECRET_KEY = environ.get('SECRET_KEY')
