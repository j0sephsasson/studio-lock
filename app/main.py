from datetime import time
import json
import re, time
import stripe
import os
import base64
from flask import Blueprint, render_template, request, flash, session, jsonify
from flask.helpers import url_for
from . import db
from .db_models import User, Studio, StudioImages, StudioBookings
from dotenv import load_dotenv
from flask_login import login_required, current_user
from werkzeug.utils import redirect, secure_filename

## init env vars
load_dotenv()

## initialize flask app
main = Blueprint('main', __name__)

# default page of our web-app
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# profile page of our web-app
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    name = current_user.name
    return render_template('profile.html', name=name)

# booking page of our web-app
@main.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    return render_template('booking.html')


# booking checker
@main.route('/booking_checker', methods=['POST'])
@login_required
def booking_checker():
    studio_name = request.form['studio']
    date = request.form['date']
    time_slot = request.form['slot']
    engineer = request.form['engineer']

    bookings = StudioBookings.query.filter_by(studio_name=studio_name, date=date).all()

    if len(bookings) == 3:
        return 'failure'
    else:
        for b in bookings:
            if b.slot_one == True and time_slot == '1':
                return 'failure'
            elif b.slot_two == True and time_slot == '2':
                return 'failure'

    return 'success'

# checkout-session "handler" API of our web-app
@main.route('/booking_handler', methods=['POST'])
@login_required
def booking_handler():
    studio_name = request.form['book-studio']
    date = request.form['book-date']
    time_slot = request.form['book-time']
    engineer = request.form['book-engineer']

    ## redirect to checkout & pass meta-data
    return redirect(url_for('main.booking_post', studio_name=studio_name,
    date=date, time_slot=time_slot, engineer=engineer))

# checkout-session page of our web-app
@main.route('/booking_post/<studio_name>/<date>/<time_slot>/<engineer>', methods=['GET'])
@login_required
def booking_post(studio_name, date, time_slot, engineer):
    stripe.api_key = os.getenv('STRIPE_TEST_KEY')
    STUDIO_PRICE_ID = os.getenv(studio_name + '_price_id')


    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': STUDIO_PRICE_ID,
                'quantity': 1,
            },
        ],
        success_url='http://127.0.0.1:5000/success',
        cancel_url='http://127.0.0.1:5000/cancel',
        automatic_tax={'enabled': True},
        mode='payment',
        metadata={
        "studio_name": studio_name,
        "date": date,
        "time_slot": time_slot,
        "engineer": engineer
        }
    )
    return redirect(session.url, code=303)

# checkout-session webhook api of our web-app
@main.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    session = payload['data']['object']

    custom_data = session['metadata']
    print(custom_data)
    return 'success'

# studio_details "handler" API of our web-app
@main.route('/studio_details', methods=['GET'])
def studio_details():
    # Get the item ID from the request
    item_id = request.args.get('studio_name')

    # Redirect to the item URL with the item ID
    return redirect(url_for('main.show_item', studio_name=item_id))

# studio_details page of our web-app
@main.route('/studio_details/<studio_name>', methods=['GET'])
def show_item(studio_name):
    # Retrieve the item with the specified ID
    studio = Studio.query.filter_by(name=studio_name).first()

    images = StudioImages.query.filter_by(name=studio_name).first()
    image_one = images.image_one
    image_two = images.image_two
    image_three = images.image_three

    encoded_image_one = base64.b64encode(image_one).decode('utf-8')
    encoded_image_two = base64.b64encode(image_two).decode('utf-8')
    encoded_image_three = base64.b64encode(image_three).decode('utf-8')

    if studio:
        return render_template('studio_details.html', studio_name=studio.name,
                            image_one=encoded_image_one, 
                            image_two=encoded_image_two, 
                            image_three=encoded_image_three)

# checkout-cancel page of our web-app
@main.route('/cancel', methods=['GET', 'POST'])
def cancel():
    return render_template('cancel.html')

# checkout-success page of our web-app
@main.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')

# misc. functions that should be in admin page
# @main.route('/perform_fn', methods=['GET', 'POST'])
# def perform_fn():
#     with open('/Users/joesasson/Desktop/sites/studio-lock/app/static/img/bullpen/bullpen.png', 'rb') as f:
#         image_one = f.read()

#     with open('/Users/joesasson/Desktop/sites/studio-lock/app/static/img/bullpen/bullpen2.png', 'rb') as f1:
#         image_two = f1.read()

#     with open('/Users/joesasson/Desktop/sites/studio-lock/app/static/img/bullpen/bullpen3.png', 'rb') as f2:
#         image_three = f2.read()

#     new_entry = StudioImages(name='Bullpen', image_one=image_one, image_two=image_two, image_three=image_three)
#     db.session.add(new_entry)
#     db.session.commit()

#     return 'success'
