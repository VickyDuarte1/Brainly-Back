
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from routes.auth_routes import auth
from routes.doctor_routes import doctor
from routes.patient_routes import patient
from routes.mp_routes import merpago
from routes.comments_route import comments

my_app = Flask(__name__)
socketio = SocketIO(my_app)
CORS(my_app)

if __name__ == '__main__':
    my_app.run()
    socketio.run(my_app)
