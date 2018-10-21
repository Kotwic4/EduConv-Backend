import json

from flask import jsonify

from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import Model


class ModelController:

    @staticmethod
    def _get_model(model_no):
        model = Model.select().where(Model.id == model_no).get()
        if model is None:
            raise InvalidUsage("model not found", status_code=404)
        return model

    @staticmethod
    def put_model(body):
        new_model = Model()
        new_model.model_json = json.dumps(body["model_json"])
        new_model.name = body.get("name")
        new_model.save()
        return jsonify(new_model.to_dict())

    @staticmethod
    def get_model_info(model_no):
        model = ModelController._get_model(model_no)
        return jsonify(model.to_dict())

    @staticmethod
    def get_models():
        models = Model.select()
        return jsonify([model.to_dict() for model in models])

    @staticmethod
    def delete_model(model_no):
        model = ModelController._get_model(model_no)
        model.delete_instance()
