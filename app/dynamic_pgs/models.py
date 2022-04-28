from datetime import datetime
from app.extensions.database import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(373), nullable=False)
    last_name = db.Column(db.String(374), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    date_add = db.Column(db.DateTime, db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<name %r>' % self.username