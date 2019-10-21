from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    strategies = db.relationship('UserStrategy', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Strategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    api_ref = db.Column(db.String(140))
    name = db.Column(db.String(140))

    def __repr__(self):
        return '<Strategy {}>'.format(self.name)
        
class UserStrategy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('USER.id'))
    strat_id = db.Column(db.Integer, db.ForeignKey('STRATEGIES.id'))
    symbol_id = db.Column(db.Integer, db.ForeignKey('USER_STRATEGIES.id'))
    last_check = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    interim = db.Column(db.Integer)

    def __repr__(self):
        return '<Post {}>'.format(self.id)
