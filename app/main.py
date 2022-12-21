from datetime import time
import json
import re, time
import stripe
import os
from flask import Blueprint, render_template, request, flash, session, jsonify
from flask.helpers import url_for
from . import db
from .db_models import User, Studio
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
    name = current_user.name
    return render_template('booking.html', name=name)

# checkout-session page of our web-app
@main.route('/booking_post/<studio_name>', methods=['POST'])
@login_required
def booking_post():
    stripe.api_key = os.getenv('STRIPE_TEST_KEY')
    STUDIO_PRICE_ID = os.getenv('STUDIO_NAME_PRICE_ID')


    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': STUDIO_PRICE_ID,
                'quantity': 3,
            },
        ],
        success_url='http://127.0.0.1:5000/success',
        cancel_url='http://127.0.0.1:5000/cancel',
        automatic_tax={'enabled': True},
        mode='payment',
        metadata={
        "customer_id": "123456",
        "order_id": "987654"
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
    return None


# studio_details "handler" page of our web-app
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
    if studio:
        return render_template('studio_details.html', studio_name=studio.name)


# checkout-cancel page of our web-app
@main.route('/cancel', methods=['GET', 'POST'])
def cancel():
    return render_template('cancel.html')

# checkout-success page of our web-app
@main.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('success.html')