from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique = True)
    name = db.Column(db.String(250), unique = True)
    tel = db.Column(db.Integer, unique = True)
    password = db.Column(db.String(250))
    is_active = db.Column(db.Boolean, default = False)
    code = db.Column(db.Integer)

