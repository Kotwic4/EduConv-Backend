import json

from flask import jsonify

from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import Scheme


class SchemeController:

    @staticmethod
    def _get_scheme(scheme_no):
        scheme = Scheme.get_or_none(Scheme.id == scheme_no)
        if scheme is None:
            raise InvalidUsage("Scheme not found", status_code=404)
        return scheme

    @staticmethod
    def put_scheme(body):
        new_scheme = Scheme()
        new_scheme.scheme_json = json.dumps(body)
        new_scheme.save()
        return jsonify(new_scheme.to_dict())

    @staticmethod
    def get_scheme_info(scheme_no):
        scheme = SchemeController._get_scheme(scheme_no)
        return jsonify(scheme.to_dict())

    @staticmethod
    def get_schemes():
        schemes = Scheme.select()
        return jsonify([scheme.to_dict() for scheme in schemes])

    @staticmethod
    def delete_scheme(scheme_no):
        scheme = SchemeController._get_scheme(scheme_no)
        scheme.delete_instance()
