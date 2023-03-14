from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# USUARIOS

# Ruta para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    # Obtener los datos del nuevo usuario desde la solicitud POST
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    birthdate = request.json['birthdate']
    # Abrir una conexión con la base de datos SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Insertar el nuevo usuario en la tabla 'users'
    cursor.execute('INSERT INTO users (name, email, password, birthdate) VALUES (?, ?, ?, ?)',
                   (name, email, password, birthdate))
    conn.commit()
    # Obtener el ID del nuevo usuario
    user_id = cursor.lastrowid
    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()
    # Devolver la respuesta con los datos del nuevo usuario
    response = jsonify({'id': user_id, 'name': name, 'email': email, 'birthdate': birthdate})
    response.status_code = 201
    return response

# Ruta para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    # Abrir una conexión con la base de datos SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Obtener todos los usuarios de la tabla 'users'
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()
    # Convertir la lista de usuarios en una lista de diccionarios
    user_list = []
    for user in users:
        user_dict = {'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3], 'birthdate': user[4]}
        user_list.append(user_dict)
    # Devolver la respuesta con todos los usuarios
    response = jsonify(user_list)
    response.status_code = 200
    return response

# Ruta para obtener un usuario por su ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # Abrir una conexión con la base de datos SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Obtener el usuario con el ID especificado
    cursor.execute('SELECT * FROM users WHERE id=?', (user_id,))
    user = cursor.fetchone()
    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()
    # Comprobar si se encontró el usuario con el ID especificado
    if user:
        # Convertir el usuario en un diccionario
        user_dict = {'id': user[0], 'name': user[1], 'email': user[2], 'password': user[3], 'birthdate': user[4]}
        # Devolver la respuesta con el usuario encontrado
        response = jsonify(user_dict)
        response.status_code = 200
    else:
        # Si no se encontró el usuario, devolver una respuesta de error 404
        response = jsonify({'message': 'User not found'})
        response.status_code = 404
    return response


# Ruta para eliminar un usuario por su ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    # Abrir una conexión con la base de datos SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Eliminar el usuario con el ID especificado
    cursor.execute('DELETE FROM users WHERE id=?', (user_id,))
    conn.commit()
    # Obtener el número de filas afectadas por la consulta SQL
    rows_deleted = cursor.rowcount
    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()
    # Comprobar si se eliminó el usuario con el ID especificado
    if rows_deleted > 0:
        # Devolver una respuesta de éxito 200
        response = jsonify({'message': f'User with ID {user_id} has been deleted'})
        response.status_code = 200
    else:
        # Si no se encontró el usuario, devolver una respuesta de error 404
        response = jsonify({'message': 'User not found'})
        response.status_code = 404
    
    return response

# Ruta para actualizar un usuario por su ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    # Obtener los datos del usuario a actualizar del cuerpo de la solicitud
    user_data = request.get_json()
    # Abrir una conexión con la base de datos SQLite
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Actualizar los datos del usuario con el ID especificado
    cursor.execute('UPDATE users SET name=?, email=?, password=? WHERE id=?',
                   (user_data['name'], user_data['email'], user_data['password'], user_id))
    conn.commit()
    # Obtener el número de filas afectadas por la consulta SQL
    rows_updated = cursor.rowcount
    # Cerrar la conexión con la base de datos
    cursor.close()
    conn.close()
    # Comprobar si se actualizó el usuario con el ID especificado
    if rows_updated > 0:
        # Devolver una respuesta de éxito 200
        response = jsonify({'message': f'User with ID {user_id} has been updated'})
        response.status_code = 200
    else:
        # Si no se encontró el usuario, devolver una respuesta de error 404
        response = jsonify({'message': 'User not found'})
        response.status_code = 404
    
    return response

# MEDICOS

# Ruta para crear un nuevo médico
@app.route('/doctors', methods=['POST'])
def create_doctor():
    # Obtener los datos del médico a través del body de la petición
    data = request.get_json()
    name = data['name']
    email = data['email']
    password = data['password']
    birthdate = data['birthdate']
    registration = data['registration']
    admin = data['admin']
    # Abrir una conexión con la base de datos
    with sqlite3.connect('mydb.db') as conn:
        # Crear un cursor para realizar operaciones en la base de datos
        cur = conn.cursor()
        # Insertar al nuevo médico en la tabla 'doctor'
        cur.execute("""
            INSERT INTO doctor (name, email, password, birthdate, registration, admin)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, password, birthdate, registration, admin))
        # Obtener el ID del nuevo médico
        doctor_id = cur.lastrowid
        # Guardar los cambios en la base de datos
        conn.commit()
        # Crear una respuesta con los datos del nuevo médico
        response = {
            'id': doctor_id,
            'name': name,
            'email': email,
            'birthdate': birthdate,
            'registration': registration,
            'admin': admin
        }
        # Devolver la respuesta en formato JSON
        return jsonify(response)

# Ruta para obtener todos los médicos
@app.route('/doctors', methods=['GET'])
def get_doctors():
    # Abrir una conexión con la base de datos
    with sqlite3.connect('mydb.db') as conn:
        # Configurar el objeto conexión para que devuelva filas como objetos Row de SQLite
        conn.row_factory = sqlite3.Row
        # Crear un cursor para realizar operaciones en la base de datos
        cur = conn.cursor()
        # Seleccionar todos los médicos de la tabla 'doctor'
        cur.execute("""
            SELECT * FROM doctor
        """)
        # Obtener todas las filas resultantes de la consulta
        rows = cur.fetchall()
        # Crear una lista de médicos con los datos de las filas resultantes
        response = []
        for row in rows:
            response.append({
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'birthdate': row['birthdate'],
                'registration': row['registration'],
                'admin': row['admin']
            })
        # Devolver la lista de médicos en formato JSON
        return jsonify(response)

# Ruta para obtener un médico por ID
@app.route('/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    # Abrir una conexión con la base de datos
    with sqlite3.connect('mydb.db') as conn:
        # Configurar el objeto conexión para que devuelva filas como objetos Row de SQLite
        conn.row_factory = sqlite3.Row
        # Crear un cursor para realizar operaciones en la base de datos
        cur = conn.cursor()
        # Ejecutamos la consulta SQL para obtener el médico con el ID especificado
        cur.execute("""
            SELECT * FROM doctor WHERE id = ?
        """, (doctor_id,))
        row = cur.fetchone()
        # Si se encontró un médico con el ID especificado, devolvemos sus datos
        if row:
            response = {
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'birthdate': row['birthdate'],
                'registration': row['registration'],
                'admin': row['admin']
            }
            return jsonify(response)
        # Si no se encontró un médico con el ID especificado, devolvemos un mensaje de error
        else:
            return jsonify({'error': 'Doctor not found.'}), 404

@app.route('/doctor/<int:doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    try:
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        # Recuperamos los datos del cuerpo de la solicitud
        data = request.get_json()
        # Extraemos los campos a actualizar
        name = data['name']
        email = data['email']
        password = data['password']
        birthdate = data['birthdate']
        registration = data['registration']
        # Ejecutamos la consulta SQL para actualizar los datos del médico
        c.execute('''UPDATE doctor SET name = ?, email = ?, password = ?, birthdate = ?, registration = ? 
                     WHERE id = ?''', (name, email, password, birthdate, registration, doctor_id))
        conn.commit()
        conn.close()
        # Devolvemos una respuesta con un mensaje de éxito
        return jsonify({'message': 'Doctor updated successfully.'}), 200
    except:
        # En caso de error, devolvemos una respuesta con un mensaje de error
        return jsonify({'error': 'Failed to update doctor.'}), 400
    
@app.route('/doctor/<int:doctor_id>', methods=['DELETE'])
def delete_doctor(doctor_id):
    try:
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        # Ejecutamos la consulta SQL para eliminar el médico con el ID especificado
        c.execute('DELETE FROM doctor WHERE id = ?', (doctor_id,))
        conn.commit()
        conn.close()
        # Devolvemos una respuesta con un mensaje de éxito
        return jsonify({'message': 'Doctor deleted successfully.'}), 200
    except:
        # En caso de error, devolvemos una respuesta con un mensaje de error
        return jsonify({'error': 'Failed to delete doctor.'}), 400
    
# DIAGNOSTICOS

@app.route('/diagnosis', methods=['GET'])
def get_all_diagnosis():
    try:
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        # Ejecutamos la consulta SQL para obtener todos los diagnósticos
        c.execute('SELECT * FROM diagnosis')
        diagnosis = c.fetchall()
        conn.close()
        # Si se encontraron diagnósticos, devolvemos sus datos
        if diagnosis:
            diagnosis_list = []
            for d in diagnosis:
                diagnosis_list.append({'id': d[0], 'type': d[1], 'message': d[2], 'date': d[3]})
            return jsonify({'diagnosis': diagnosis_list})
        # Si no se encontraron diagnósticos, devolvemos un mensaje de error
        else:
            return jsonify({'error': 'No diagnosis found.'}), 404
    except:
        # En caso de error, devolvemos una respuesta con un mensaje de error
        return jsonify({'error': 'Failed to retrieve diagnosis.'}), 400


@app.route('/diagnosis/<int:diagnosis_id>', methods=['GET'])
def get_diagnosis(diagnosis_id):
    try:
        conn = sqlite3.connect('mydb.db')
        c = conn.cursor()
        # Ejecutamos la consulta SQL para obtener el diagnóstico con el ID especificado
        c.execute('SELECT * FROM diagnosis WHERE id = ?', (diagnosis_id,))
        diagnosis = c.fetchone()
        conn.close()
        # Si se encontró un diagnóstico con el ID especificado, devolvemos sus datos
        if diagnosis:
            return jsonify({'diagnosis': {'id': diagnosis[0], 'type': diagnosis[1], 'message': diagnosis[2], 
                                          'date': diagnosis[3]}})
        # Si no se encontró un diagnóstico con el ID especificado, devolvemos un mensaje de error
        else:
            return jsonify({'error': 'Diagnosis not found.'}), 404
    except:
        # En caso de error, devolvemos una respuesta con un mensaje de error
        return jsonify({'error': 'Failed to retrieve diagnosis.'}), 400

if __name__ == '__main__':
    app.run(debug=True)