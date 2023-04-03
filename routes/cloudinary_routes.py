from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader

upload = Blueprint('upload', __name__)

def upload_image(file):
    cloudinary.config(
        cloud_name="brainlypf",
        api_key="143982914773545",
        api_secret="Qt7iifjrFNj2-rFkrn9dssdYaME"
    )

    upload_data = cloudinary.uploader.upload(file)
    image_url = upload_data['secure_url']

    return image_url


@upload.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error="Archivo no encontrado")

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="Nombre de archivo no encontrado")

    filename = secure_filename(file.filename)
    img_url = upload_image(file)

    # Devuelve la URL de la imagen en formato JSON
    return jsonify(filename=filename, img_url=img_url)