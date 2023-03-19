from flask import Flask, Blueprint, request, jsonify
from users import users
from login import login
from register import register
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos
conn = sqlite3.connect('users.db')

"""
conexion = sqlite3.connect('users.db')
cursor = conexion.cursor()
cursor.execute('''CREATE TABLE doctor 
              (id INTEGER PRIMARY KEY, nombre TEXT, correo TEXT, usuario TEXT, contraseña TEXT, imagen TEXT, edad INTEGER, genero TEXT, fecha_nacimiento DATE, direccion TEXT, telefono TEXT, especialidad TEXT, credenciales TEXT)''')
conexion.close()
"""

app.register_blueprint(users)
app.register_blueprint(login)
app.register_blueprint(register)


if __name__ == '__main__':
    app.run(debug=True)
