
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
        image_to_upload = request.files["image"]
        if image_to_upload:
            upload_result = upload(image_to_upload)
            url = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=100,
                                                     height=100)
            full_size_url = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=200,
                                                     height=100, radius=20, effect="sepia")

            image_json = request.get_json()
            image_json["url"] = url
            image_json["full_size_url"] = full_size_url
            image = image_schema.load(request.get_json())

            try:
                image.save_to_db()
            except:
                return {"message": "error uploading file"}
            return image_schema.dump(image), 201
        return {"message": "no image uploaded"}, 401
