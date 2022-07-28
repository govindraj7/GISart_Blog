# load the environmernt variables
from dotenv import load_dotenv
load_dotenv()

# db variable from .env
from os import environ
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
# DATABASE_URL=sqlite:///users.db

# super secret key
SECRET_KEY = environ.get('SECRET_KEY')
S3BASEURL = environ.get('S3BASEURL')
S3_BUCKET = environ.get('S3_BUCKET')
S3_KEY = environ.get('S3_KEY')
S3_SECRET = environ.get('S3_SECRET')
S3_LOCATION = environ.get('S3_LOCATION')
