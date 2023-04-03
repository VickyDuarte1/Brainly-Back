from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from routes.auth_routes import auth
from routes.doctor_routes import doctor
from routes.patient_routes import patient
from routes.mp_routes import merpago
from routes.comments_route import comments

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

# Ruta de autenticación
app.register_blueprint(auth)

# Ruta CRUD doctores
app.register_blueprint(doctor)

# Ruta CRUD pacientes
app.register_blueprint(patient, my_app=my_app, socketio=socketio)

# Ruta MERCADO_PAGO
app.register_blueprint(merpago)

# Ruta Comentarios/Reviews
app.register_blueprint(comments)

socketio = SocketIO(app, async_mode='eventlet')

if __name__ == '__main__':
    socketio.run(app)
    app.run()
