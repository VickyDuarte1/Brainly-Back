from flask import Blueprint, request, jsonify
import sqlite3
import os

detection = Blueprint('detection', __name__)

# Obtener la ruta base de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Definir la ruta relativa a la base de datos
database_path = os.path.join(basedir, 'usuarios.db')

# Crear la tabla 'resultados' si no existe
def crear_tabla_resultados():
    with sqlite3.connect(database_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS resultados (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        usuario TEXT NOT NULL,
                        imagen TEXT NOT NULL,
                        resultado TEXT NOT NULL
                        );''')

# Ruta para registrar un nuevo resultado
@detection.route('/detection', methods=['POST'])
def registrar_resultado():
    usuario = request.json['usuario']
    imagen = request.json['imagen']
    resultado = request.json['resultado']

    # Conectar a la base de datos
    with sqlite3.connect(database_path) as conn:
        # Crear la tabla 'resultados' si no existe
        crear_tabla_resultados()

        # Insertar el nuevo resultado en la tabla 'resultados'
        conn.execute(
            'INSERT INTO resultados (usuario, imagen, resultado) VALUES (?, ?, ?)', (usuario, imagen, resultado))

    return jsonify({'mensaje': 'Resultado registrado correctamente.'}), 201

# Ruta para obtener todos los resultados
@detection.route('/detection/resultados', methods=['GET'])
def obtener_resultados():
    with sqlite3.connect(database_path) as conn:
        # Obtener todos los resultados de la tabla 'resultados'
        cursor = conn.execute('SELECT * FROM resultados')

        # Convertir los resultados a una lista de diccionarios
        resultados = [{'id': row[0], 'usuario': row[1], 'imagen': row[2], 'resultado': row[3]} for row in cursor.fetchall()]

    return jsonify({'resultados': resultados}), 200
