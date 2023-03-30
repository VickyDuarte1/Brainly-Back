from flask import Flask
from flask_cors import CORS
from auth_routes import auth
from doctor_routes import doctor
from patient_routes import patient
from mp_routes import merpago
from comments_route import comments


app = Flask(__name__)
CORS(app)

# Ruta de autenticación
app.register_blueprint(auth)

# Ruta CRUD doctores
app.register_blueprint(doctor)

# Ruta CRUD pacientes
app.register_blueprint(patient)

# Ruta MERCADO_PAGO 
app.register_blueprint(merpago)

# Ruta Comentarios/Reviews
app.register_blueprint(comments)


if __name__ == '__main__':
    app.run()
