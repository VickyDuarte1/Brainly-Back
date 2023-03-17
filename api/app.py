from flask import Blueprint, request, jsonify
from routes import routes-users, routes-checkout
import sqlite3

app = Flask(__name__)

app.register_blueprint(routes-users)
app.register_blueprint(routes-checkout)

if __name__ == '__main__':
    app.run(debug=True)