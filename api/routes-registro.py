from flask import Blueprint
import sqlite3

# Crear un objeto Blueprint
registro = Blueprint('registro', __name__)

# Ruta para registrar un nuevo usuario

@app.route('/registro', methods=['POST'])
def registrar_usuario():
    tipo_usuario = request.json['tipo_usuario']
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

    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # # Verificar que el nombre de usuario no esté en uso
    # cursor = conn.execute(
    #     'SELECT usuario FROM paciente WHERE usuario = ?', (usuario,))
    # resultado = cursor.fetchone()
    # if resultado is not None:
    #     return jsonify({'mensaje': 'El nombre de usuario ya está en uso.'}), 400

    # Verificar que el nombre de usuario no esté en uso en la tabla paciente
    cursor = conn.execute(
        'SELECT usuario FROM paciente WHERE usuario = ?', (usuario,))
    resultado = cursor.fetchone()

    # Si el nombre de usuario ya está en uso en la tabla paciente, devolver un error
    if resultado is not None:
        return jsonify({'mensaje': 'El nombre de usuario ya está en uso.'}), 400

    # Verificar que el nombre de usuario no esté en uso en la tabla doctor
    cursor = conn.execute(
        'SELECT usuario FROM doctor WHERE usuario = ?', (usuario,))
    resultado = cursor.fetchone()

    # Si el nombre de usuario ya está en uso en la tabla doctor, devolver un error
    if resultado is not None:
        return jsonify({'mensaje': 'El nombre de usuario ya está en uso.'}), 400

    # Insertar el nuevo usuario en la base de datos
    if tipo_usuario == 'doctor':
        especialidad = request.json['especialidad']
        credenciales = request.json['credenciales']
        conn.execute(
            'INSERT INTO doctor (nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, especialidad, credenciales) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, especialidad, credenciales))

    conn.commit()

    if tipo_usuario == 'paciente':
        conn.execute(
            'INSERT INTO paciente (nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, resultado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono))
    conn.commit()

    return jsonify({'mensaje': 'Usuario registrado correctamente.'}), 201

    # Cerrar la conexión a la base de datos
    conn.close()

# Exportar el Blueprint
return registro