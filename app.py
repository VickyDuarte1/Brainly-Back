from flask import Flask
from flask_cors import CORS
from auth_routes import auth
from doctor_routes import doctor
from patient_routes import patient
<<<<<<< HEAD
from cloudinary_routes import cloud
=======
from mp_routes import merpago
>>>>>>> main

app = Flask(__name__)
CORS(app)

# Ruta de autenticación
app.register_blueprint(auth)

# Ruta CRUD doctores
app.register_blueprint(doctor)

# Ruta CRUD pacientes
app.register_blueprint(patient)

<<<<<<< HEAD
#Ruta cloudinary

app.register_blueprint(cloud)
=======
# Ruta MERCADO_PAGO 
app.register_blueprint(merpago)
>>>>>>> main

if __name__ == '__main__':
    app.run()
