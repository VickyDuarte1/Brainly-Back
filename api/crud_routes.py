from flask import Blueprint, request, jsonify
import sqlite3

crud = Blueprint('crud', __name__)

# Ruta para obtener todos los pacientes


@crud.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Obtener todos los usuarios de la base de datos
    cursor = conn.execute(
        'SELECT nombre, correo, usuario, imagen, edad, genero, fecha_nacimiento, direccion, telefono, resultado FROM paciente')
    pacientes = [{'nombre': fila[0], 'correo': fila[1], 'usuario': fila[2], 'imagen': fila[3], 'edad': fila[4], 'genero': fila[5], 'fecha_nacimiento': fila[6],
                 'direccion': fila[7], 'telefono': fila[8], 'resultado': fila[9]} for fila in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'pacientes': pacientes}), 200

# Ruta para obtener todos los doctores


@crud.route('/doctores', methods=['GET'])
def obtener_doctores():
    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Obtener todos los usuarios de la base de datos
    cursor = conn.execute(
        'SELECT nombre, correo, usuario, imagen, edad, genero, fecha_nacimiento, direccion, telefono, especialidad, credenciales FROM doctor')
    doctores = [{'nombre': fila[0], 'correo': fila[1], 'usuario': fila[2], 'imagen': fila[3], 'edad': fila[4], 'genero': fila[5], 'fecha_nacimiento': fila[6],
                 'direccion': fila[7], 'telefono': fila[8], 'especialidad': fila[9], 'credenciales': fila[10]} for fila in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'doctores': doctores}), 200
