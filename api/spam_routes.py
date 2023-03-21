from flask import Blueprint, request
from flask_mail import Mail, Message

spam = Blueprint('spam', __name__)

spam.config['MAIL_SERVER']='smtp.gmail.com'
spam.config['MAIL_PORT'] = 465
spam.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'
spam.config['MAIL_PASSWORD'] = 'tu_contraseña'
spam.config['MAIL_USE_TLS'] = False
spam.config['MAIL_USE_SSL'] = True
mail = Mail(spam)

@spam.route("/", methods=['POST'])
def index():
    if request.method == 'POST':
        destinatario = request.form['destinatario']
        mensaje = request.form['mensaje']
        msg = Message('Asunto del correo', sender='tu_correo@gmail.com', recipients=[destinatario])
        msg.body = mensaje
        mail.send(msg)
        return "Correo enviado!"
    else:
        return "Esta página solo maneja solicitudes POST"
    
"""
<form method="POST" action="{{ url_for('spam.index') }}">
  <label for="destinatario">Destinatario:</label>
  <input type="email" id="destinatario" name="destinatario">
  <br>
  <label for="mensaje">Mensaje:</label>
  <textarea id="mensaje" name="mensaje"></textarea>
  <br>
  <button type="submit">Enviar correo electrónico</button>
</form>
"""