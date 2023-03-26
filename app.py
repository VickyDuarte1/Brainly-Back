from flask import Flask, request, jsonify
from flask_cors import CORS
from auth_routes import auth
from doctor_routes import doctor
from patient_routes import patient
import mercadopago
import requests

app = Flask(__name__)
CORS(app)

# Ruta de autenticación
app.register_blueprint(auth)

# Ruta CRUD doctores
app.register_blueprint(doctor)

# Ruta CRUD pacientes
app.register_blueprint(patient)

#MERCADO_PAGO
access_token = 'APP_USR-20109353218546-032217-2fb30a023e1c6a65a60b29367729a685-1332740081'
sdk = mercadopago.SDK(access_token)

@app.route('/generar_pago', methods=['POST'])
def generar_pago():    
  # Traer del plan creado
    print(request.json)
    url = 'https://api.mercadopago.com/preapproval_plan/2c9380848712f89601871662a59e0153'
    headers = {'Authorization': 'Bearer APP_USR-20109353218546-032217-2fb30a023e1c6a65a60b29367729a685-1332740081'}
    response = requests.get(url, headers=headers)
    plan_response = response.json()

    subscription_data = {
      "preapproval_plan_id": plan_response["id"],
      "reason": plan_response["reason"],
      "payer_email": request.json["payer"]["email"],
      "auto_recurring": plan_response["auto_recurring"],
      "card_token_id": request.json["token"],
      "back_url": "http://localhost:5000/pago_exitoso",
    }
    subscription_response = sdk.subscription().create(subscription_data)
    print(subscription_response) 
    
    status_code = subscription_response["status"]
    if status_code == 201:
        return jsonify({"link": subscription_response["response"]["init_point"]}), 200
    else:
        return jsonify({"error": subscription_response["response"]["message"]}), status_code

#ruta success
@app.route('/pago_exitoso', methods=['GET','POST'])
def pago_exitoso ():    
    return f'<p>Pago exitoso, ya podes acceder a las ventajas premiun</p>'


if __name__ == '__main__':
    app.run()
