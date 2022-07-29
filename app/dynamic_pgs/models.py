from datetime import datetime
from app.extensions.database import db, CRUDMixin
from werkzeug.security import generate_password_hash, check_password_hash
from slugify import slugify
from flask_login import UserMixin

# one-to-many relationship, one User >> many BlogPosts
#! ///// users model ///// ------------------------------------------------------------------------------------------------------------------------ */
class Users(db.Model, CRUDMixin, UserMixin): 
    __tablename__='users'
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(128), unique=True)
    user_name = db.Column(db.String(144), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    bio = db.Column(db.String(400), nullable=True)
    profile_pic = db.Column(db.String, nullable=False)
    role = db.Column(db.String(32), nullable=True,  default='User')
    # security - hashed password stored
    password_hash = db.Column(db.String(128))
    # one-to-many relationship
    posts = db.relationship('BlogPosts', backref="author")

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # slugify username when adding to db
    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('user_name', ''))
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return '<user_name %r>' % self.user_name

#! ///// blog post model ///// ------------------------------------------------------------------------------------------------------------------------ */
class BlogPosts(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    slug = db.Column(db.String(128), unique=True, nullable=False)
    image = db.Column(db.String, nullable=False)
    description = db.Column(db.String(255), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    #  foreign key linking one user to post(s)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', ''))
        super().__init__(*args, **kwargs)
    