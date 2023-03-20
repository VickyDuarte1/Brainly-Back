from flask import Flask
from auth_routes import auth
from crud_routes import crud

app = Flask(__name__)

# Rutas de autenticación
app.register_blueprint(auth)
app.register_blueprint(crud)

if __name__ == '__main__':
    app.run()
