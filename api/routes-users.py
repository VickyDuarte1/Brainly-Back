from flask import Blueprint
import sqlite3

# Crear un objeto Blueprint
users = Blueprint('users', __name__)

# conexion = sqlite3.connect('usuarios.db')
# cursor = conexion.cursor()
# cursor.execute('''CREATE TABLE doctor 
#               (id INTEGER PRIMARY KEY, nombre TEXT, correo TEXT, usuario TEXT, contraseña TEXT, imagen TEXT, edad INTEGER, genero TEXT, fecha_nacimiento DATE, direccion TEXT, telefono TEXT, especialidad TEXT, credenciales TEXT)''')
# conexion.close()

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

# Exportar el Blueprint
return users