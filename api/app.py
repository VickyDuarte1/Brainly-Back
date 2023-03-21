from flask import Flask
from auth_routes import auth
from doctor_routes import doctor
from patient_routes import patient

app = Flask(__name__)

# Ruta de autenticación
app.register_blueprint(auth)

# Ruta CRUD doctores
app.register_blueprint(doctor)

# Ruta CRUD pacientes
app.register_blueprint(patient)

if __name__ == '__main__':
    app.run(debug=True)
