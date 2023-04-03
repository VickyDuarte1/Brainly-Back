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

if __name__ == '__main__':
    socketio.run(app)
    app.run()
