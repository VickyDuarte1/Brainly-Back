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
        subject='Enviando con Twilio SendGrid es divertido',
        html_content='<strong>y fácil de hacer en cualquier lugar, incluso con Python</strong>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return f"Email enviado! Código de estado: {response.status_code}"
    except Exception as e:
        return f"Error al enviar el correo electrónico: {e}"
