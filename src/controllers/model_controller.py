import threading

from flask import send_from_directory, jsonify

from src.datasets.datasets_map import check_if_dataset_class_exists
from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import Scheme, NNModel, Dataset
from src.train.keras_model_creator import KerasModelBuilder


class ModelController:

    @staticmethod
    def _model_path(model):
        return "db/models/" + str(model.get_id())

    @staticmethod
    def _create_model(scheme, dataset):
        model = NNModel()
        model.scheme = scheme
        model.dataset = dataset
        model.epochs_learnt = 0
        model.epochs_to_learn = 0
        model.save()
        return model

    @staticmethod
    def _get_model(model_no):
        model = NNModel.select().where(NNModel.id == model_no).get()
        if model is None:
            raise InvalidUsage("Model not found", status_code=404)
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
        thread = threading.Thread(target=KerasModelBuilder.build, args=(builder, dir_path))
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        return model.get_id()

    @staticmethod
    def get_model_info(model_no):
        return jsonify(ModelController._get_model(model_no).to_dict())

    @staticmethod
    def get_models():
        models = NNModel.select()
        return jsonify([model.to_dict() for model in models])

    @staticmethod
    def get_trained_model(model_no, filename):
        model = ModelController._get_model(model_no)
        dir_path = ModelController._model_path(model)
        return send_from_directory(dir_path, filename)

    @staticmethod
    def delete_model(model_no):
        model = ModelController._get_model(model_no)
        model.delete_instance()
