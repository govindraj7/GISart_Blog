from os import environ
from dotenv import load_dotenv

SECRET_KEY = environ.get('SECRET_KEY')

load_dotenv()