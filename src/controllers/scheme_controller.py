import json

from flask import jsonify

from src.datasets.scheme_validator import SchemeValidator
from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import Scheme


class SchemeController:

    @staticmethod
    def __get_scheme(scheme_no):
        scheme = Scheme.select().where(Scheme.id == scheme_no).get()
        if scheme is None:
            raise InvalidUsage("Scheme not found", status_code=404)
        return scheme

    @staticmethod
    def put_scheme(body):
        new_scheme = Scheme()
        if "scheme_json" not in body:
            raise InvalidUsage("Scheme do not have field: scheme_json", status_code=400)
        new_scheme.scheme_json = json.dumps(body["scheme_json"])
        new_scheme.name = body.get("name")
        SchemeValidator.valid_scheme(new_scheme)
        new_scheme.save()
        return jsonify(new_scheme.to_dict())

    @staticmethod
    def get_scheme_info(scheme_no):
        scheme = SchemeController.__get_scheme(scheme_no)
        return jsonify(scheme.to_dict())

    @staticmethod
    def get_schemes():
        schemes = Scheme.select()
        return jsonify([scheme.to_dict() for scheme in schemes])

    @staticmethod
    def delete_scheme(scheme_no):
        scheme = SchemeController.__get_scheme(scheme_no)
        scheme.delete_instance()
