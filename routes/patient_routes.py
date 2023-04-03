from flask import Blueprint, request, jsonify
from flask_socketio import SocketIO
import sqlite3
import os

patient = Blueprint('patient', __name__,)

# Obtener la ruta base de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Definir la ruta relativa a la base de datos
database_path = os.path.join(basedir, 'usuarios.db')

# Ruta para obtener todos los pacientes


@patient.route('/pacientes', methods=['GET'])
def obtener_pacientes():
    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Obtener todos los usuarios de la base de datos
    cursor = conn.execute(
        'SELECT id, nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, resultado, activo, premium FROM paciente')
    pacientes = [{'id': fila[0], 'nombre': fila[1], 'correo': fila[2], 'usuario': fila[3], 'contraseña': fila[4], 'imagen': fila[5], 'edad': fila[6], 'genero': fila[7], 'fecha_nacimiento': fila[8],
                  'direccion': fila[9], 'telefono': fila[10], 'resultado': fila[11], 'activo':fila[12], 'premium': fila[13]} for fila in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()
    
    # Enviar evento a través de SocketIO
    socketio.emit('my_event', {'data': 'Se ha usado la ruta "my_route"'}, namespace='/my_namespace')

    return jsonify({'pacientes': pacientes}), 200


# Ruta para obtener un paciente por su ID


@patient.route('/pacientes/<int:id>', methods=['GET'])
def obtener_paciente(id):
    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Obtener el paciente correspondiente al ID
    cursor = conn.execute(
        'SELECT id, nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, resultado, activo, premium FROM paciente WHERE id = ?', (id,))
    resultado = cursor.fetchone()

    # Si el paciente no existe, devolver un error 404
    if resultado is None:
        return jsonify({'mensaje': 'Paciente no encontrado.'}), 404

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'paciente': {'id': resultado[0], 'nombre': resultado[1], 'correo': resultado[2], 'usuario': resultado[3], 'contraseña': resultado[4], 'imagen': resultado[5], 'edad': resultado[6], 'genero': resultado[7], 'fecha_nacimiento': resultado[8], 'direccion': resultado[9], 'telefono': resultado[10], 'resultado': resultado[11], 'activo':  resultado[12], 'premium': resultado[13]}}), 200

# Ruta para actualizar un paciente existente


@patient.route('/pacientes/<int:id>', methods=['PUT'])
def actualizar_paciente(id):
    nombre = request.json['nombre']
    correo = request.json['correo']
    usuario = request.json['usuario']
    contraseña = request.json['contraseña']
    imagen = request.json['imagen']
    edad = request.json['edad']
    genero = request.json['genero']
    fecha_nacimiento = request.json['fecha_nacimiento']
    direccion = request.json['direccion']
    telefono = request.json['telefono']
    resultado = request.json['resultado']

    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Verificar que el paciente exista
    cursor = conn.execute('SELECT id FROM paciente WHERE id = ?', (id,))
    paciente = cursor.fetchone()
    if paciente is None:
        return jsonify({'mensaje': 'Paciente no encontrado.'}), 404

    # Actualizar el paciente en la base de datos
    conn.execute('UPDATE paciente SET nombre = ?, correo = ?, usuario = ?, contraseña = ?, imagen = ?, edad = ?, genero = ?, fecha_nacimiento = ?, direccion = ?, telefono = ?, resultado = ? WHERE id = ?',
                 (nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, resultado, id))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Paciente actualizado correctamente.'}), 200

# Ruta para eliminar un paciente existente


@patient.route('/pacientes/<int:id>', methods=['DELETE'])
def eliminar_paciente(id):
    # Conectar a la base de datos

    conn = sqlite3.connect(database_path)

    # Verificar que el paciente exista
    cursor = conn.execute('SELECT id FROM paciente WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Paciente no encontrado.'}), 404

    # Eliminar el paciente de la base de datos
    conn.execute('DELETE FROM paciente WHERE id = ?', (id,))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Paciente eliminado correctamente.'}), 200

# Ruta para deshabilitar un paciente existente


@patient.route('/pacientes/<int:id>/deshabilitar', methods=['PUT'])
def deshabilitar_paciente(id):
    # Conectar a la base de datos

    conn = sqlite3.connect(database_path)

    # Verificar que el paciente exista
    cursor = conn.execute('SELECT id FROM paciente WHERE id = ?', (id,))
    paciente = cursor.fetchone()
    if paciente is None:
        return jsonify({'mensaje': 'Paciente no encontrado.'}), 404

    # Deshabilitar el paciente en la base de datos
    conn.execute(
        'UPDATE paciente SET activo = ? WHERE id = ?', (False, id))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Paciente deshabilitado correctamente.'}), 200


@patient.route('/pacientes/<int:id>/habilitar', methods=['PUT'])
def habilitar_paciente(id):
    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Verificar que el paciente exista
    cursor = conn.execute('SELECT id FROM paciente WHERE id = ?', (id,))
    paciente = cursor.fetchone()
    if paciente is None:
        return jsonify({'mensaje': 'Paciente no encontrado.'}), 404

    # Habilitar el paciente en la base de datos
    conn.execute(
        'UPDATE paciente SET activo = ? WHERE id = ?', (True, id))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Paciente habilitado correctamente.'}), 200

