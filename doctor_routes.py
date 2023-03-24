from flask import Blueprint, request, jsonify
import sqlite3

doctor = Blueprint('doctor', __name__)

# Obtener la ruta base de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Definir la ruta relativa a la base de datos
database_path = os.path.join(basedir, 'usuarios.db')

# Ruta para obtener todos los doctores


@doctor.route('/doctores', methods=['GET'])
def obtener_doctores():
    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Obtener todos los usuarios de la base de datos
    cursor = conn.execute(
        'SELECT id, nombre, correo, usuario, imagen, edad, genero, fecha_nacimiento, direccion, telefono, especialidad, credenciales FROM doctor')
    doctores = [{'id': fila[0], 'nombre': fila[1], 'correo': fila[2], 'usuario': fila[3], 'imagen': fila[4], 'edad': fila[5], 'genero': fila[6], 'fecha_nacimiento': fila[7],
                 'direccion': fila[8], 'telefono': fila[9], 'especialidad': fila[10], 'credenciales': fila[11]} for fila in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'doctores': doctores}), 200

# Ruta para obtener un paciente por su ID


@doctor.route('/doctores/<int:id>', methods=['GET'])
def obtener_doctor(id):
    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Obtener el doctor correspondiente al ID
    cursor = conn.execute(
        'SELECT id, nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, especialidad, credenciales FROM doctor WHERE id = ?', (id,))
    resultado = cursor.fetchone()

    # Si el doctor no existe, devolver un error 404
    if resultado is None:
        return jsonify({'mensaje': 'Doctor no encontrado.'}), 404

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'doctor': {'id': resultado[0], 'nombre': resultado[1], 'correo': resultado[2], 'usuario': resultado[3], 'contraseña': resultado[4], 'imagen': resultado[5], 'edad': resultado[6], 'genero': resultado[7], 'fecha_nacimiento': resultado[8], 'direccion': resultado[9], 'telefono': resultado[10], 'especialidad': resultado[11], 'credenciales': resultado[12]}}), 200

# Ruta para actualizar un doctor existente


@doctor.route('/doctores/<int:id>', methods=['PUT'])
def actualizar_doctor(id):
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
    especialidad = request.json['especialidad']
    credenciales = request.json['credenciales']

    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Verificar que el doctor exista
    cursor = conn.execute('SELECT id FROM doctor WHERE id = ?', (id,))
    doctor = cursor.fetchone()
    if doctor is None:
        return jsonify({'mensaje': 'Doctor no encontrado.'}), 404

    # Actualizar el doctor en la base de datos
    conn.execute('UPDATE doctor SET nombre = ?, correo = ?, usuario = ?, contraseña = ?, imagen = ?, edad = ?, genero = ?, fecha_nacimiento = ?, direccion = ?, telefono = ?, especialidad = ?, credenciales = ? WHERE id = ?',
                 (nombre, correo, usuario, contraseña, imagen, edad, genero, fecha_nacimiento, direccion, telefono, especialidad, credenciales, id))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Doctor actualizado correctamente.'}), 200

# Ruta para eliminar un doctor existente


@doctor.route('/doctores/<int:id>', methods=['DELETE'])
def eliminar_doctor(id):
    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Verificar que el doctor exista
    cursor = conn.execute('SELECT id FROM doctor WHERE id = ?', (id,))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Doctor no encontrado.'}), 404

    # Eliminar el doctor de la base de datos
    conn.execute('DELETE FROM doctor WHERE id = ?', (id,))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Doctor eliminado correctamente.'}), 200

# Ruta para deshabilitar un doctor existente


@doctor.route('/doctores/<int:id>/deshabilitar', methods=['PUT'])
def deshabilitar_doctor(id):
    # Conectar a la base de datos
    conn = sqlite3.connect(database_path)

    # Verificar que el doctor exista
    cursor = conn.execute('SELECT id FROM doctor WHERE id = ?', (id,))
    doctor = cursor.fetchone()
    if doctor is None:
        return jsonify({'mensaje': 'Doctor no encontrado.'}), 404

    # Deshabilitar el paciente en la base de datos
    conn.execute(
        'UPDATE doctor SET habilitado = ? WHERE id = ?', (False, id))
    conn.commit()

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'mensaje': 'Doctor deshabilitado correctamente.'}), 200
