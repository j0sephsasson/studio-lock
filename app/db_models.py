from . import db
from flask_login import UserMixin

## user table ##
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.Text, unique=False, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=False, nullable=False)

## studios table ##
class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.Text, unique=True, nullable=False)

## bookings table ##
class Bookings(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    studio_name = db.Column(db.Text, unique=False, nullable=False) ## studio name
    username = db.Column(db.Text, unique=False, nullable=False) ## username
    date = db.Column(db.Text, unique=False, nullable=False) ## date
    slot_one = db.Column(db.Boolean, default=False) ## slot is booked --> default False
    slot_two = db.Column(db.Boolean, default=False) ## slot is booked --> default False
    slot_three = db.Column(db.Boolean, default=False) ## slot is booked --> default False
    slot_four = db.Column(db.Boolean, default=False) ## slot is booked --> default False