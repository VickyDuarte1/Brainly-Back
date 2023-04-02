from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from routes.auth_routes import auth
from routes.doctor_routes import doctor
from routes.patient_routes import patient
from routes.mp_routes import merpago
from routes.comments_route import comments


app = Flask(__name__)
socketio = SocketIO(app)
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

socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)
    app.run()
