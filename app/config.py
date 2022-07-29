# load the environment variables
from dotenv import load_dotenv
load_dotenv()

# db variable from .env
from os import environ
# db URL
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL') 
# for security
SECRET_KEY = environ.get('SECRET_KEY')
#  AWS S3 related
S3BASEURL = environ.get('S3BASEURL')
S3_BUCKET = environ.get('S3_BUCKET')
S3_KEY = environ.get('S3_KEY')
S3_SECRET = environ.get('S3_SECRET')
S3_LOCATION = environ.get('S3_LOCATION')
# to add some security
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_CONTENT_LENGTH = 1024 * 5 * 1024