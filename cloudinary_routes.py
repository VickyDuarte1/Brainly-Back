import cloudinary
import cloudinary.uploader
from flask import Flask, request, jsonify

cloudinary.config(
  cloud_name = "brainlypf",
  api_key = "143982914773545",
  api_secret = "Qt7iifjrFNj2-rFkrn9dssdYaME"
)

def upload_image(file_path):
  return cloudinary.uploader.upload(file_path)



app = Flask(__name__)

@app.route("/upload-image", methods=["POST"])
def upload_image():
    file = request.files["file"]
    response = cloudinary.uploader.upload(file)
    return jsonify(response)

