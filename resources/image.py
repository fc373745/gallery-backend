import json
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from flask_restful import Resource
from flask import request
from models.image import ImageModel
from schemas.image import ImageSchema

image_schema = ImageSchema()
image_list_schema = ImageSchema(many=True)


class Image(Resource):
    @classmethod
    def post(cls):
        name = request.form.to_dict()["name"]
        if ImageModel.find_by_name(name):
            return {"message": "An image already exists with that name"}, 400
        image_to_upload = request.files["image"]
        if image_to_upload:
            upload_result = upload(image_to_upload)
            # figure out sizes
            url = cloudinary_url(
                upload_result["public_id"],
                format="jpg",
                crop="fill",
                width=100,
                height=100,
            )[0]

            full_size_url = cloudinary_url(
                upload_result["public_id"],
                format="jpg",
                crop="fill",
                width=200,
                height=100,
                radius=20,
                effect="sepia",
            )[0]

            image_json = request.form.to_dict()  # this returns None
            image = ImageModel(
                name=image_json["name"], url=url, full_size_url=full_size_url
            )

            try:
                image.save_to_db()
            except:
                return {"message": "error uploading file"}, 500
            return image.json(), 201
        return {"message": "Please select an image"}, 401
