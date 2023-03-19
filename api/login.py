from flask import Blueprint, render_template, request, jsonify
import sqlite3

# Crear un objeto Blueprint
login = Blueprint('login', __name__)

# Conectar a la base de datos
conn = sqlite3.connect('users.db')

# Ruta para autenticar un usuario existente

@login.route('/login', methods=['POST'])
def iniciar_sesion():
    usuario = request.json['usuario']
    contraseña = request.json['contraseña']

    # Conectar a la base de datos
    conn = sqlite3.connect('users.db')

    # Verificar que el nombre de usuario y la contraseña sean correctos
    cursor = conn.execute(
        'SELECT usuario, contraseña, "paciente" as tipo_usuario FROM paciente WHERE usuario = ? AND contraseña = ?'
        ' UNION '
        'SELECT usuario, contraseña, "doctor" as tipo_usuario FROM doctor WHERE usuario = ? AND contraseña = ?',
        (usuario, contraseña, usuario, contraseña))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Nombre de usuario o contraseña incorrectos.'}), 401

    tipo_usuario = resultado[2]

    # El inicio de sesión es correcto
    return jsonify({'mensaje': 'Inicio de sesión correcto.', 'tipo_usuario': tipo_usuario}), 200

    # Cerrar la conexión a la base de datos
    conn.close()
