from datetime import datetime
from app.extensions.database import db, CRUDMixin
from werkzeug.security import generate_password_hash, check_password_hash

# users model
class Users(db.Model, CRUDMixin):
    __tablename__='users_details'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    user_name = db.Column(db.String(25), unique=True, nullable=False)
    first_name = db.Column(db.String(373), nullable=False)
    last_name = db.Column(db.String(374), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<user_name %r>' % self.user_name

# blog post model
class BlogPosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # author = db.Column(db.Integer, db.ForeignKey('users.user_name'), nullable=False)
    slug = db.Column(db.String(100))
    title = db.Column(db.String(80))
    image = db.Column(db.String)
    description = db.Column(db.String(150))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    