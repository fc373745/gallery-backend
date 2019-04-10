from db import db
from typing import List
import json


class ImageModel(db.Model):
    __tablename__ = "images"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    url = db.Column(db.String(200), nullable=False)
    full_size_url = db.Column(db.String(200), nullable=False)

    @classmethod
    def find_by_name(cls, name: str) -> "ImageModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls) -> List["ImageModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def json(self):
        dict = {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "full_url": self.full_size_url,
        }
        return dict
