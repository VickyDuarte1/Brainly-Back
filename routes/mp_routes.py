from flask import Blueprint, request, jsonify
import mercadopago
import requests
import sqlite3
import os

merpago = Blueprint('merpago', __name__)

# Obtener la ruta base de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))
# Definir la ruta relativa a la base de datos
database_path = os.path.join(basedir, 'usuarios.db')

#token de acceso y config inicial
access_token = 'APP_USR-20109353218546-032217-2fb30a023e1c6a65a60b29367729a685-1332740081'
sdk = mercadopago.SDK(access_token)

#Ruta para generar el pago
@merpago.route('/generar_pago', methods=['POST'])
def generar_pago():    
  # Traer del plan creado
    print({'ESTO ES EL FORM': request.json})
    
    url = 'https://api.mercadopago.com/preapproval_plan/2c9380848712f89601871662a59e0153'

    headers = {'Authorization': 'Bearer APP_USR-20109353218546-032217-2fb30a023e1c6a65a60b29367729a685-1332740081'}
    response = requests.get(url, headers=headers)
    plan_response = response.json()
    print({'ESTO ES EL PLAN': plan_response})
    subscription_data = {
      "preapproval_plan_id": plan_response["id"],
      "reason": plan_response["reason"],
      "payer_email": request.json["payer"]["email"],
      "auto_recurring": plan_response["auto_recurring"],
      "card_token_id": request.json["token"],
      "back_url": plan_response["back_url"],
    }
    print({'ESTO ES LA SUB': subscription_data})
    subscription_response = sdk.subscription().create(subscription_data)
    print(subscription_response) 
    
    status_code = subscription_response["status"]
    if status_code == 201:
        return jsonify({"link": subscription_response["response"]["init_point"]}), 200
    else:
        return jsonify({"error": subscription_response["response"]["message"]}), status_code

#ruta success
@merpago.route('/pago_exitoso', methods=['POST'])
def pago_exitoso ():    
    # Obtener datos de la noti de MP
    # notificacion = request.get_json()
    # status del pago
    # status_pago = notificacion["status"]
      correo_electronico = request.json["correo"]
      if correo_electronico is None:
        return jsonify({'error': 'no recibio correo'})
      
        # Conexión con DB y setear a premium
      conn = sqlite3.connect(database_path)   
         
      cursor = conn.execute(
        'SELECT * FROM paciente WHERE correo = ?', (correo_electronico,))
      resultado = cursor.fetchone()
      # Si el paciente no existe, devolver un error 404
      if resultado is None:
        return jsonify({'mensaje': 'Paciente no encontrado.'}), 404      
      else:      
        conn.execute(
          'UPDATE paciente SET premium = ? WHERE correo = ?', (True, correo_electronico))
        conn.commit()

      return jsonify({'mensaje': 'usuario seteado a premium'})
      # Cerrar conexión 
      conn.close()
     