from flask import Blueprint, request, jsonify
import sqlite3
import os

comments = Blueprint('comments', __name__)

# Obtener la ruta base de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Definir la ruta relativa a la base de datos
database_path = os.path.join(basedir, 'usuarios.db')

# conn = sqlite3.connect(database_path)
# conn.execute(
# """CREATE TABLE IF NOT EXISTS comentarios (
#     id INTEGER PRIMARY KEY,
#     comentario TEXT,
#     puntuacion INTEGER,
#     paciente_id INTEGER,
#     FOREIGN KEY(paciente_id) REFERENCES paciente(id)
# )"""
# )
# conn.commit()
# conn.close()

### Ruta insertar comentarios/reviews ###


@comments.route('/comentarios', methods=['POST'])
def guardar_comentarios():

    # Json
    id = request.json["id"]
    texto = request.json["texto"]
    puntuacion = request.json["puntuacion"]
    usuario_paciente = request.json["usuario"]
    if texto is None or puntuacion is None or id is None or usuario_paciente is None:
        return jsonify({'mensaje': 'Por favor complete bien todos los campos.'}), 404

    # Conexión database
    conn = sqlite3.connect(database_path)

    # Insertar review en tabla
    conn.execute(
        'INSERT INTO comentarios(comentario,puntuacion,paciente_id,usuario_paciente) values (?,?,?,?)', (texto, puntuacion, id, usuario_paciente))
    conn.commit()

    # Cerrar conexión
    conn.close()

    return jsonify({'mensaje': 'Feedback cargado exitosamente, muchas gracias!'}), 201

### Ruta traer comentarios/reviews ###


@comments.route('/get_comments', methods=['GET'])
def traer_comentarios():

    # Conexión database
    conn = sqlite3.connect(database_path)

    # Traer todos los comentarios
    cursor = conn.execute(
        'SELECT id,comentario,puntuacion,paciente_id,usuario_paciente FROM comentarios')
    comentarios = [{'id': fila[0], 'comentario': fila[1], 'puntuacion': fila[2],
                    'paciente_id': fila[3], 'usuario_paciente': fila[4]} for fila in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    return jsonify({'comentarios': comentarios}), 200
