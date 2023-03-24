from flask import Flask, request, jsonify
from flask_cors import CORS
from auth_routes import auth
from doctor_routes import doctor
from patient_routes import patient
import mercadopago

app = Flask(__name__)
CORS(app)

# Ruta de autenticación
app.register_blueprint(auth)

# Ruta CRUD doctores
app.register_blueprint(doctor)

# Ruta CRUD pacientes
app.register_blueprint(patient)

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


if __name__ == '__main__':
    app.run()
