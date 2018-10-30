import json
import shutil
import threading
import time
from os import path

from flask import jsonify

from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import NNModel


class ModelController:

    @staticmethod
    def _get_model(model_no):
        model = NNModel.get_or_none(NNModel.id == model_no)
        if model is None:
            raise InvalidUsage("model not found", status_code=404)
        return model

    @staticmethod
    def put_model(body):
        new_model = NNModel()
        try:
            body_dict = json.loads(body)
        except:
            raise InvalidUsage("Sent body is not a valid JSON object",status_code=400)
        try:
            new_model.model_json = json.dumps(body_dict.get("model_json"))
        except:
            raise InvalidUsage("There is no model_json in sent model",status_code=400)
        new_model.name = body_dict.get("name","")
        new_model.save()
        return jsonify(new_model.to_dict())

    @staticmethod
    def get_model_info(model_no):
        model = ModelController._get_model(model_no)
        return jsonify(model.to_dict())

    @staticmethod
    def get_models():
        models = NNModel.select()
        return jsonify([model.to_dict() for model in models])

    @staticmethod
    def delete_model(model_no):
        model = ModelController._get_model(model_no)
        shutil.rmtree(ModelController._model_path(model))
        model.delete_instance()
