from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    store = db.Column(db.String(1000), unique=True)
    fname = db.Column(db.String(250))
    lname = db.Column(db.String(250))
    tel = db.Column(db.Integer, unique=True)

class Audio (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype1 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)
    status = db.Column(db.String(100))

class Brakes (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype2 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

class Engine (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype3 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

class Exterior (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype4 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

class Headlights (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype5 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

class Interior (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype6 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

class Motorcycle (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype7 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)


class Safety (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype8 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)


class Wheels (db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200))
    type = db.Column(db.String(100))
    subtype9 = db.Column(db.String(100))
    location = db.Column(db.String(100))
    condition = db.Column(db.String(100))
    description = db.Column(db.Text)
    price = db.Column(db.Integer)

