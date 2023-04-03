from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth
from routes.doctor_routes import doctor
from routes.patient_routes import patient
from routes.mp_routes import merpago
from routes.comments_route import comments
from routes.cloudinary_routes import upload

app = Flask(__name__)
CORS(app)

# Ruta de autenticación
app.register_blueprint(auth)

# Ruta CRUD doctores
app.register_blueprint(doctor)

# Ruta CRUD pacientes
app.register_blueprint(patient)

# Ruta MERCADO_PAGO
app.register_blueprint(merpago)

# Ruta Comentarios/Reviews
app.register_blueprint(comments)

# Ruta Cloudinary
app.register_blueprint(upload)

# Inicializar el servidor SocketIO con el blueprint de chat
chat_socketio.init_app(app, blueprint=chat_bp)

if __name__ == '__main__':
    # Iniciar el servidor de desarrollo Flask
    app.run()
    # Iniciar el servidor SocketIO en segundo plano
    chat_socketio.run(app)
