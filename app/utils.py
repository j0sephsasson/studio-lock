from icalendar import Calendar, Event
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import smtplib
import uuid
import os

def string_to_datetime(date_string, slot, end=False):
    """
    This function converts a date_string from an input tag type date
    and converts it to datetime format

    Args:
        - 'date_string': str --> '2022-12-20'
        - 'slot': str --> '1' or '2' or '3'

    Returns:
        - datetime format string: str --> datetime.datetime(2023, 12, 20, hr, min)
    """

    # Parse the date string
    date = datetime.strptime(date_string, '%Y-%m-%d')

    times = {'1':{'start':12, 'end':16}, '2':{'start':16, 'end':20}, '3':{'start'}}

    if end:
        # return the datetime object with format
        return datetime(date.year, date.month, date.day, times[slot]['end'], 0, 0)
    
    # return the datetime object with format
    return datetime(date.year, date.month, date.day, times[slot]['start'], 0, 0)

def create_event(date, slot, user_email, location, studio_name):

  # Create the calendar object
  cal = Calendar()
  cal.add('prodid', '-//My calendar invite//mxm.dk//')
  cal.add('version', '2.0')

  # Create the event object
  event = Event()
  event.add('summary', 'Your Studio Session at {}'.format(studio_name))
  event.add('dtstart', string_to_datetime(date, slot))
  event.add('dtend', string_to_datetime(date, slot, end=True))
  event.add('dtstamp', datetime.now())
  event.add('uid', uuid.uuid4())
  event.add('organizer', 'mailto:support@studiolock.us')
  event.add('attendee', 'mailto:{}'.format(user_email))
  event.add('location', location)

  # Add the event to the calendar
  cal.add_component(event)

  # Convert the calendar to a string
  cal_str = cal.to_ical().decode()

  # Create the email message
  msg = MIMEMultipart()
  msg['Subject'] = 'Studio Lock - Studio Session Confirmation'
  msg['From'] = 'support@studiolock.us'
  msg['To'] = user_email
  msg.attach(MIMEText(cal_str, 'calendar'))

  # Send the email
  with smtplib.SMTP(os.getenv('MAIL_SERVER'), 587) as server:
    server.starttls()
    server.login("support@studiolock.us", os.getenv('MAIL_PASSWORD'))
    server.sendmail(msg['From'], msg['To'], msg.as_string())