from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Ruta para registrar un nuevo usuario


@app.route('/registro', methods=['POST'])
def registrar_usuario():
    nombre = request.json['nombre']
    contraseña = request.json['contraseña']

    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Verificar que el nombre de usuario no esté en uso
    cursor = conn.execute(
        'SELECT nombre FROM usuarios WHERE nombre = ?', (nombre,))
    resultado = cursor.fetchone()
    if resultado is not None:
        return jsonify({'mensaje': 'El nombre de usuario ya está en uso.'}), 400

    # Insertar el nuevo usuario en la base de datos
    conn.execute(
        'INSERT INTO usuarios (nombre, contraseña) VALUES (?, ?)', (nombre, contraseña))
    conn.commit()

    return jsonify({'mensaje': 'Usuario registrado correctamente.'}), 201

    # Cerrar la conexión a la base de datos
    conn.close()

# Ruta para autenticar un usuario existente


@app.route('/login', methods=['POST'])
def iniciar_sesion():
    nombre = request.json['nombre']
    contraseña = request.json['contraseña']

    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Verificar que el nombre de usuario y la contraseña sean correctos
    cursor = conn.execute(
        'SELECT nombre FROM usuarios WHERE nombre = ? AND contraseña = ?', (nombre, contraseña))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Nombre de usuario o contraseña incorrectos.'}), 401

    # El inicio de sesión es correcto
    return jsonify({'mensaje': 'Inicio de sesión correcto.'}), 200

    # Cerrar la conexión a la base de datos
    conn.close()

# Ruta para obtener todos los usuarios


@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Obtener todos los usuarios de la base de datos
    cursor = conn.execute('SELECT id, nombre, contraseña FROM usuarios')
    usuarios = [{'id': fila[0], 'nombre': fila[1], 'contraseña': fila[2]}
                for fila in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'usuarios': usuarios}), 200

# Ruta para obtener un usuario por su ID


@app.route('/usuarios/<int:id>', methods=['GET'])
def obtener_usuario(id):
    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Obtener el usuario correspondiente al ID
    cursor = conn.execute(
        'SELECT id, nombre, contraseña FROM usuarios WHERE id = ?', (id,))
    resultado = cursor.fetchone()

    # Si el usuario no existe, devolver un error 404
    if resultado is None:
        return jsonify({'mensaje': 'Usuario no encontrado.'}), 404

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'usuario': {'id': resultado[0], 'nombre': resultado[1], 'contraseña': resultado[2]}}), 200

# Ruta para actualizar un usuario existente


@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    nombre = request.json['nombre']
    contraseña = request.json['contraseña']

    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Verificar que el usuario exista
    cursor = conn.execute('SELECT id FROM usuarios WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Usuario no encontrado.'}), 404

    # Actualizar el usuario en la base de datos
    conn.execute('UPDATE usuarios SET nombre = ?, contraseña = ? WHERE id = ?',
                 (nombre, contraseña, id))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Usuario actualizado correctamente.'}), 200

# Ruta para eliminar un usuario existente


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Verificar que el usuario exista
    cursor = conn.execute('SELECT id FROM usuarios WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Usuario no encontrado.'}), 404

    # Eliminar el usuario de la base de datos
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Usuario eliminado correctamente.'}), 200


if __name__ == '__main__':
    app.run()
