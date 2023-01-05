from datetime import time
import json
import re, time
import stripe
import os
import base64
from flask import Blueprint, render_template, request, flash, session, jsonify
from flask.helpers import url_for
from . import db
from .db_models import User, Studio, StudioImages, StudioBookings, UserBookings
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
    email = current_user.email

    bookings = UserBookings.query.filter_by(email=email).all()

    if not bookings:
        bookings=False

    return render_template('profile.html', name=name, bookings=bookings)

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

    if bookings:
        if bookings[0].slot_one == True and time_slot == '1':
            return 'failure'
        elif bookings[0].slot_two == True and time_slot =='2':
            return 'failure'
        elif bookings[0].slot_three == True and time_slot == '3':
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
        customer_email=current_user.email,
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
    payload_meta_data = request.json
    session = payload_meta_data['data']['object']
    booking_data = session['metadata']

    payload_event = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = os.getenv('STRIPE_WEBHOOK_TESTING_KEY')

    event = stripe.Webhook.construct_event(
        payload_event, sig_header, endpoint_secret
    )

    time_slots = {'1':'12PM-4PM', '2':'4PM-8PM', '3':'8PM-12AM'}

    if event['type'] == 'checkout.session.completed':
        print('payment received...')
        print('adding data to userbookings table...')

        new_user_booking = UserBookings(date=booking_data['date'], email=customer_email,
                                            studio_name=booking_data['studio_name'],
                                            price=int(session_customer['amount_total'])*0.01,
                                            time_slot=time_slots[booking_data['time_slot']])
        
        db.session.add(new_user_booking)

        bookings = StudioBookings.query.filter_by(studio_name=booking_data['studio_name'], 
                                                date=booking_data['date']).all()

        if bookings:
            print('booking found at {} on {}'.format(booking_data['studio_name'], booking_data['date']))
            if booking_data['time_slot'] == '1':
                bookings[0].slot_one = True
            elif booking_data['time_slot'] == '2':
                bookings[0].slot_two = True
            elif booking_data['time_slot'] == '3':
                bookings[0].slot_three = True
        else:
            print('no booking found, adding new booking to db...')
            session_customer = event['data']['object']
            customer_email = session_customer["customer_details"]["email"]

            if booking_data['time_slot'] == '1':
                new_studio_booking = StudioBookings(studio_name=booking_data['studio_name'], 
                                            date=booking_data['date'],
                                            slot_one=True)
            elif booking_data['time_slot'] == '2':
                new_studio_booking = StudioBookings(studio_name=booking_data['studio_name'], 
                                            date=booking_data['date'],
                                            slot_two=True)
            elif booking_data['time_slot'] == '3':
                new_studio_booking = StudioBookings(studio_name=booking_data['studio_name'], 
                                            date=booking_data['date'],
                                            slot_three=True)

            db.session.add(new_studio_booking)
            
        db.session.commit()
        print('booking confirmed...')
        print(booking_data)
    
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

    if images:
        return render_template('studio_details.html', 
                            studio_name=studio.name,
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
#     # with open('/Users/joesasson/Desktop/sites/studio-lock/app/static/img/bullpen/bullpen.png', 'rb') as f:
#     #     image_one = f.read()

#     # with open('/Users/joesasson/Desktop/sites/studio-lock/app/static/img/bullpen/bullpen2.png', 'rb') as f1:
#     #     image_two = f1.read()

#     # with open('/Users/joesasson/Desktop/sites/studio-lock/app/static/img/bullpen/bullpen3.png', 'rb') as f2:
#     #     image_three = f2.read()

#     # new_entry = StudioImages(name='Bullpen', image_one=image_one, image_two=image_two, image_three=image_three)

#     fastlife = Studio(name='Fastlife', phone_number='347-201-2620')
#     breezi = Studio(name='Breezi', phone_number='516-510-8902')
#     bullpen = Studio(name='Bullpen', phone_number='917-971-9412')

#     db.session.add(fastlife)
#     db.session.add(breezi)
#     db.session.add(bullpen)

#     db.session.commit()

#     return 'success'
