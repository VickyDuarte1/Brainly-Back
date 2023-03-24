from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import mercadopago

app = Flask(__name__)
CORS(app)
# conexion = sqlite3.connect('usuarios.db')
# cursor = conexion.cursor()
# cursor.execute('''CREATE TABLE doctor
#                   (id INTEGER PRIMARY KEY, nombre TEXT, correo TEXT, usuario TEXT, contraseña TEXT, imagen TEXT, edad INTEGER, genero TEXT, fecha_nacimiento DATE, direccion TEXT, telefono TEXT, especialidad TEXT, credenciales TEXT)''')
# conexion.close()

#MERCADO_PAGO

sdk = mercadopago.SDK('APP_USR-20109353218546-032217-2fb30a023e1c6a65a60b29367729a685-1332740081')

sdk.preference()

@app.route('/generar_pago', methods=['POST'])
def generar_pago():    
  # Creacion del plan
    plan_data = { 
        "reason": "Usuario Premiun Brainly",
        "auto_recurring": {
        "frequency": 1,
        "frequency_type": "months",
        "free_trial": {
            "frequency": 1,
            "frequency_type": "months"
        },
        "transaction_amount": 250,
        "currency_id": "ARS"
        },
        "back_url": "https://www.mercadopago.com.ar"
    }
    plan_response = sdk.plan().create(plan_data)
  # Creacion de la suscripcion
    subscription_data = {
      "preapproval_plan_id": plan_response["response"]["id"],
      "reason": plan_response["response"]["reason"],
      "payer_email": request.json["payer"]["email"],
      "auto_recurring": plan_response["response"]["auto_recurring"],
      "card_token_id": request.json["token"],
      "back_url": plan_response["response"]["back_url"],
    }
    subscription_response = sdk.subscription().create(subscription_data)
    print(subscription_response) 
    # print(pay_link)
    return jsonify({"link": subscription_response["response"]["init_point"]}), 200

#ruta success
@app.route('/pago_exitoso', methods=['GET'])
def pago_exitoso ():    
    return f'<p>Pago exitoso, ya podes acceder a las ventajas premiun</p>'




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

# Ruta para autenticar un usuario existente


@app.route('/login', methods=['POST'])
def iniciar_sesion():
    usuario = request.json['usuario']
    contraseña = request.json['contraseña']

    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Verificar que el nombre de usuario y la contraseña sean correctos
    cursor = conn.execute(
        'SELECT usuario, contraseña, "paciente" as tipo_usuario FROM paciente WHERE usuario = ? AND contraseña = ?'
        ' UNION '
        'SELECT usuario, contraseña, "doctor" as tipo_usuario FROM doctor WHERE usuario = ? AND contraseña = ?',
        (usuario, contraseña, usuario, contraseña))
    resultado = cursor.fetchone()
    if resultado is None:
        return jsonify({'mensaje': 'Nombre de usuario o contraseña incorrectos.'}), 401

    tipo_usuario = resultado[2]

    # El inicio de sesión es correcto
    return jsonify({'mensaje': 'Inicio de sesión correcto.', 'tipo_usuario': tipo_usuario}), 200

    # Cerrar la conexión a la base de datos
    conn.close()

# Ruta para obtener todos los usuarios


@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    # Conectar a la base de datos
    conn = sqlite3.connect('usuarios.db')

    # Obtener todos los usuarios de la base de datos
    cursor = conn.execute('SELECT id, nombre, contraseña FROM paciente')
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
        'SELECT id, nombre, contraseña FROM paciente WHERE id = ?', (id,))
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
