from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app)
    app.run()
