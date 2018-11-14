import json
import shutil
import threading
import time
from os import path

from flask import jsonify

from src.datasets.scheme_validator import ModelValidator
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
            new_model.model_json = json.dumps(body.get("model_json"))
        except:
            raise InvalidUsage("There is no model_json in sent model", status_code=400)
        b = body.get("model_json")
        if not isinstance(b, dict):
            raise InvalidUsage("There is no model_json in sent model", status_code=400)
        new_model.name = body.get("name", "")
        ModelValidator.validate_model(new_model)
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
