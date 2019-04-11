import os
import cloudinary

from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from marshmallow import ValidationError
from db import db
from ma import ma
from resources.image import Image, ImageList

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default configs from default_config.py
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py (APPLICATION_SETTINGS points to config.py)

api = Api(app)

cloudinary.config(
    cloud_name=os.environ.get("CL_CLOUD_NAME"),
    api_key=os.environ.get("CL_API_KEY"),
    api_secret=os.environ.get("CL_API_SECRET"),
)


@app.before_first_request
def create_tables():
    db.create_all()


# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


api.add_resource(Image, "/image")
api.add_resource(ImageList, "/images")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
