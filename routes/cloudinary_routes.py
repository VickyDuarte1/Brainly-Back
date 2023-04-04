from flask import Blueprint, request
import cloudinary
import cloudinary.uploader
import cloudinary.api

upload = Blueprint('upload', __name__)

cloudinary.config(
  cloud_name = "brainlypf",
  api_key = "143982914773545",
  api_secret = "Qt7iifjrFNj2-rFkrn9dssdYaME"
)

def upload_image(imagen):
  resultado = cloudinary.uploader.upload(imagen)
  return resultado['secure_url']

@upload.route('/upload', methods=['POST'])
def procesar_imagen():
  imagen = request.files['imagen']
  url = upload_image(imagen)
  return url