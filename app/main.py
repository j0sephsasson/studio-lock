from datetime import time
import json
import re, time
from os import error
from flask import Blueprint, render_template, request, flash, session, jsonify
from flask.helpers import url_for
from . import db
from .db_models import User
from flask_login import login_required, current_user
from werkzeug.utils import redirect, secure_filename


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

# studio_details page of our web-app
@main.route('/studio_details', methods=['GET', 'POST'])
def studio_details():
    return render_template('studio_details.html', studio_name='Testing')