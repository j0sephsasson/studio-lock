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

# about page of our web-app
@main.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')