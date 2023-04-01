from flask import Blueprint, request, jsonify
from flask_cors import CORS
import cloudinary
import cloudinary.uploader
import numpy as np
from tensorflow import keras
from werkzeug.utils import secure_filename
from PIL import Image
import os

detection = Blueprint('detection', __name__)

# Obtener la ruta base de tu proyecto
basedir = os.path.abspath(os.path.dirname(__file__))

# Definir la ruta relativa a la base de datos
database_path = os.path.join(basedir, 'usuarios.db')

cloudinary.config(cloud_name='brainlypf',
                  api_key='143982914773545',
                  api_secret='Qt7iifjrFNj2-rFkrn9dssdYaME')

model = keras.models.load_model("./models/classification.h5")
classes = ['Ningún Tumor', 'Tumor Pituitario',
           'Tumor Meningioma', 'Tumor Glioma']


result = ""
ses = False


def names(number):
    if (number == 0):
        return classes[0]
    elif (number == 1):
        return classes[1]
    elif (number == 2):
        return classes[2]
    elif (number == 3):
        return classes[3]


@detection.route("/detection", methods=["POST"])
def mainPage():
    if 'file' not in request.files:
        return jsonify(error="Archivo no encontrado")

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="Nombre de archivo no encontrado")

    filename = secure_filename(file.filename)
    img = Image.open(file)
    dim = (150, 150)
    x = np.array(img.resize(dim))
    x = x.reshape(1, 150, 150, 3)
    answ = model.predict_on_batch(x)
    classification = np.where(answ == np.amax(answ))[1][0]
    predicted_results = names(classification)+' Detectado'

    # Guardar imagen en Cloudinary
    cloudinary_response = cloudinary.uploader.upload(file, folder='images')
    image_url = cloudinary_response.get('url')

    # Devuelve el resultado de la clasificación y la URL de la imagen en formato JSON
    return jsonify(filename=filename, predicted_results=predicted_results, image_url=image_url)
