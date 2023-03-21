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

if __name__ == '__main__':
    app.run(debug=True)
from auth_routes import auth
from crud_routes import crud

app = Flask(__name__)

# Rutas de autenticación
app.register_blueprint(auth)
app.register_blueprint(crud)

if __name__ == '__main__':
    app.run()

