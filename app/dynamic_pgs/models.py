from datetime import datetime
from app.extensions.database import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    user_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(373), nullable=False)
    last_name = db.Column(db.String(374), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<user_name %r>' % self.user_name