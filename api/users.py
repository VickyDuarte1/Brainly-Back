from flask import Blueprint, render_template, request, jsonify
import sqlite3

# Crear un objeto Blueprint
users = Blueprint('users', __name__)

# Conectar a la base de datos
conn = sqlite3.connect('users.db')

# Ruta para obtener todos los users

@users.route('/users', methods=['GET'])
def obtener_users():
    # Conectar a la base de datos
    conn = sqlite3.connect('users.db')

    # Obtener todos los users de la base de datos
    cursor = conn.execute('SELECT id, nombre, contraseña FROM users')
    users = [{'id': fila[0], 'nombre': fila[1], 'contraseña': fila[2]}
                for fila in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'users': users}), 200

# Ruta para obtener un usuario por su ID

@users.route('/users/<int:id>', methods=['GET'])
def obtener_usuario(id):
    # Conectar a la base de datos
    conn = sqlite3.connect('users.db')

    # Obtener el usuario correspondiente al ID
    cursor = conn.execute(
        'SELECT id, nombre, contraseña FROM users WHERE id = ?', (id,))
    resultado = cursor.fetchone()

    # Si el usuario no existe, devolver un error 404
    if resultado is None:
        return jsonify({'mensaje': 'Usuario no encontrado.'}), 404

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'usuario': {'id': resultado[0], 'nombre': resultado[1], 'contraseña': resultado[2]}}), 200

# Ruta para actualizar un usuario existente

@users.route('/users/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    nombre = request.json['nombre']
    contraseña = request.json['contraseña']

    # Conectar a la base de datos
    conn = sqlite3.connect('users.db')

    # Verificar que el usuario exista
    cursor = conn.execute('SELECT id FROM users WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Usuario no encontrado.'}), 404

    # Actualizar el usuario en la base de datos
    conn.execute('UPDATE users SET nombre = ?, contraseña = ? WHERE id = ?',
                 (nombre, contraseña, id))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Usuario actualizado correctamente.'}), 200

# Ruta para eliminar un usuario existente

@users.route('/users/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    # Conectar a la base de datos
    conn = sqlite3.connect('users.db')

    # Verificar que el usuario exista
    cursor = conn.execute('SELECT id FROM users WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Usuario no encontrado.'}), 404

    # Eliminar el usuario de la base de datos
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Usuario eliminado correctamente.'}), 200
