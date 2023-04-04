from flask import Blueprint, request, jsonify
import sqlite3
import os

auth = Blueprint('auth', __name__)

# Obtener la ruta base de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Definir la ruta relativa a la base de datos
database_path = os.path.join(basedir, 'usuarios.db')

# Ruta para registrar un paciente o un doctor nuevo


@auth.route('/registro', methods=['POST'])
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
    conn = sqlite3.connect(database_path)

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
        resultado = request.json['resultado']
        conn.execute(
            'INSERT INTO paciente (nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, resultado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, resultado))
    conn.commit()

    return jsonify({'mensaje': 'Usuario registrado correctamente.'}), 201

    # Cerrar la conexión a la base de datos
    conn.close()

# Ruta para autenticar un usuario existente


@auth.route('/login', methods=['POST'])
def iniciar_sesion():
    usuario = request.json['usuario']
    contraseña = request.json['contraseña']

    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)
   
    # Verificar que el nombre de usuario y la contraseña sean correctos
    cursor = conn.execute(
        'SELECT usuario, contraseña, activo, "paciente" as tipo_usuario FROM paciente WHERE usuario = ? AND contraseña = ?'
        ' UNION '
        'SELECT usuario, contraseña, NULL as activo, "doctor" as tipo_usuario FROM doctor WHERE usuario = ? AND contraseña = ?',
        (usuario, contraseña, usuario, contraseña))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Nombre de usuario o contraseña incorrectos.'}), 401
    if resultado[2] != 1:
        return jsonify({"mensaje": "No puedes iniciar sesión, tu cuenta se encuentra desactivada."}), 401
   
    tipo_usuario = resultado[3]

    # El inicio de sesión es correcto
    return jsonify({'mensaje': 'Inicio de sesión correcto.', 'tipo_usuario': tipo_usuario}), 200

    # Cerrar la conexión a la base de datos
    conn.close()
    
# Ruta para cambiar contraseña
    
   
@auth.route('/password', methods=['POST'])
def cambiar_contraseña():
    usuario = request.json['usuario']
    contraseña_actual = request.json['current_password']
    contraseña_nueva = request.json['new_password']

    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Verificar que el nombre de usuario y la contraseña actual sean correctos
    cursor = conn.execute(
        'SELECT usuario, contraseña, "paciente" as tipo_usuario FROM paciente WHERE usuario = ? AND contraseña = ?'
        ' UNION '
        'SELECT usuario, contraseña, "doctor" as tipo_usuario FROM doctor WHERE usuario = ? AND contraseña = ?',
        (usuario, contraseña_actual, usuario, contraseña_actual))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Nombre de usuario o contraseña incorrectos.'}), 401

    tipo_usuario = resultado[2]

    # Actualizar la contraseña del usuario
    if tipo_usuario == 'paciente':
        conn.execute(
            'UPDATE paciente SET contraseña = ? WHERE usuario = ?',
            (contraseña_nueva, usuario))
    elif tipo_usuario == 'doctor':
        conn.execute(
            'UPDATE doctor SET contraseña = ? WHERE usuario = ?',
            (contraseña_nueva, usuario))

    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Contraseña actualizada correctamente.'}), 200