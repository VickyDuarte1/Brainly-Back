from flask import Blueprint
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

# Create a new blueprint
spam = Blueprint("spam", __name__)

@spam.route("/spam", methods=["POST"])
def spam():
message = Mail(
    from_email='from_email@example.com',
    to_emails='to@example.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
