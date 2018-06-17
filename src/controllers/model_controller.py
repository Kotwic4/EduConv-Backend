from flask import send_from_directory

from src.datasets.datasets_map import check_if_dataset_class_exists
from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import Scheme, Model, Dataset
from src.train.keras_model_creator import KerasModelBuilder


class ModelController:

    @staticmethod
    def _model_path(model):
        return "models/" + str(model.get_id())

    @staticmethod
    def _create_model(scheme, dataset):
        model = Model()
        model.scheme = scheme
        model.dataset = dataset
        model.save()
        return model

    @staticmethod
    def _get_model(model_no):
        model = Model.select().where(Model.id == model_no).get()
        if model is None:
            raise InvalidUsage("no model specified in request found in database")
        return model

    @staticmethod
    def train_model(body):
        if "dataset" not in body.keys():
            raise InvalidUsage("no dataset specified in request")

        scheme_id = body["scheme_id"]
        dataset_name = body["dataset"]

        scheme = Scheme.select().where(Scheme.id == scheme_id).get()

        dataset = Dataset.select().where(Dataset.name == dataset_name).get()
        dataset_class = check_if_dataset_class_exists(dataset_name)

        model = ModelController._create_model(scheme, dataset)

        del body['dataset']
        del body["scheme_id"]
        builder = KerasModelBuilder(dataset=dataset_class(), db_model=model, **body)
        dir_path = ModelController._model_path(model)
        builder.train(dir_path)

        return model.to_json()

    @staticmethod
    def get_model_info(model_no):
        return ModelController._get_model(model_no)

    @staticmethod
    def get_models():
        models = Model.select()
        return "[" + ",".join([model.to_json() for model in models]) + "]"

    @staticmethod
    def get_trained_model(model_no, filename):
        model = ModelController._get_model(model_no)
        dir_path = ModelController._model_path(model)
        return send_from_directory(dir_path, filename)