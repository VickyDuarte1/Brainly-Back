
from flask import Flask
from flask_cors import CORS
from auth_routes import auth
from doctor_routes import doctor
from patient_routes import patient


app = Flask(__name__)
CORS(app)

# Ruta de autenticación
app.register_blueprint(auth)

# Ruta CRUD doctores
app.register_blueprint(doctor)

# Ruta CRUD pacientes
app.register_blueprint(patient)

<<<<<<< HEAD


if __name__ == '__main__':
    app.run()
=======
if __name__ == '__main__':
    app.run( )

>>>>>>> 4aed5328f4fb2236c251b9b0ae531ad445da94b8

