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
            image_sizes = ImageModel.find_dimensions(image_to_upload)
            width = image_sizes[0]
            height = image_sizes[1]
            # figure out sizes
            url = cloudinary_url(
                upload_result["public_id"],
                format="jpg",
                width=450,
                quality="auto:good"
            )[0]

            full_size_url = cloudinary_url(
                upload_result["public_id"],
                format="jpg"
            )[0]

            image_json = request.form.to_dict()  # this returns None
            image = ImageModel(
                name=image_json["name"], url=url, full_size_url=full_size_url, width=width, height=height
            )

            try:
                image.save_to_db()
            except:
                return {"message": "error uploading file"}, 500
            return image.json(), 201
        return {"message": "Please select an image"}, 401


class ImageList(Resource):
    @classmethod
    def get(cls):
        args = request.args
        return ImageModel.find_by_offset(args["offset"])


