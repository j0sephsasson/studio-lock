from . import db
from flask_login import UserMixin

## user table ##
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.Text, unique=False, nullable=False)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, unique=False, nullable=False)

## newsletter subscribers ##
class Subscribers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, nullable=False, unique=True)

## studios table ##
class Studio(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.Text, unique=True, nullable=False)
    phone_number = db.Column(db.Text, unique=True, nullable=False)

## studio images ##
class StudioImages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    image_one = db.Column(db.BLOB, nullable=False)
    image_two = db.Column(db.BLOB, nullable=False)
    image_three = db.Column(db.BLOB, nullable=False)

## track studio booking availability ## --> studio bookings
class StudioBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    studio_name = db.Column(db.Text, unique=False, nullable=False) ## studio name
    date = db.Column(db.Text, unique=False, nullable=False) ## date
    slot_one = db.Column(db.Boolean, default=False) ## slot is booked --> default False
    slot_two = db.Column(db.Boolean, default=False) ## slot is booked --> default False
    slot_three = db.Column(db.Boolean, default=False) ## slot is booked --> default False

## track bookings in profile ## --> user bookings
class UserBookings(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    date = db.Column(db.Text, unique=False, nullable=False) ## date
    email = db.Column(db.Text, unique=False, nullable=False) ## email
    studio_name = db.Column(db.Text, unique=False, nullable=False) ## studio
    price = db.Column(db.Text, unique=False, nullable=False) ## price
    time_slot = db.Column(db.Text, unique=False, nullable=False) ## time_slot