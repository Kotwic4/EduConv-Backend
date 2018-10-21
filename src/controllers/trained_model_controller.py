import threading

from flask import send_from_directory, jsonify

from src.datasets.datasets_map import check_if_dataset_class_exists
from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import NNModel, NNTrainedModel, Dataset
from src.train.keras_model_creator import KerasModelBuilder


class trained_ModelController:

    @staticmethod
    def _trained_model_path(trained_model):
        return "db/trained_models/" + str(trained_model.get_id())

    @staticmethod
    def _create_trained_model(model, dataset, name=None):
        trained_model = NNTrainedModel()
        trained_model.model = model
        trained_model.dataset = dataset
        trained_model.epochs_learnt = 0
        trained_model.epochs_to_learn = 0
        trained_model.save()
        trained_model.name = name
        return trained_model

    @staticmethod
    def _get_trained_model(trained_model_no):
        trained_model = NNTrainedModel.select().where(NNTrainedModel.id == trained_model_no).get()
        if trained_model is None:
            raise InvalidUsage("trained_model not found", status_code=404)
        return trained_model

    @staticmethod
    def train_trained_model(body):
        if "dataset" not in body.keys():
            raise InvalidUsage("no dataset specified in request")

        model_id = body["model_id"]
        dataset_name = body["dataset"]
        name = body.get("name") #None if not found in json
        params = body["params"]
        model = NNModel.select().where(NNModel.id == model_id).get()

        dataset = Dataset.select().where(Dataset.name == dataset_name).get()
        dataset_class = check_if_dataset_class_exists(dataset_name)

        trained_model = trained_ModelController._create_trained_model(model, dataset, name)

        builder = KerasModelBuilder(dataset=dataset_class(), db_trained_model=trained_model, **params)
        dir_path = trained_ModelController._trained_model_path(trained_model)
        thread = threading.Thread(target=KerasModelBuilder.build, args=(builder, dir_path))
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution
        return jsonify(trained_model.to_dict())

    @staticmethod
    def get_trained_model_info(trained_model_no):
        return jsonify(trained_ModelController._get_trained_model(trained_model_no).to_dict())

    @staticmethod
    def get_trained_models():
        trained_models = NNTrainedModel.select()
        return jsonify([trained_model.to_dict() for trained_model in trained_models])

    @staticmethod
    def get_trained_trained_model(trained_model_no, filename):
        trained_model = trained_ModelController._get_trained_model(trained_model_no)
        dir_path = trained_ModelController._trained_model_path(trained_model)
        return send_from_directory(dir_path, filename)

    @staticmethod
    def delete_trained_model(trained_model_no):
        trained_model = trained_ModelController._get_trained_model(trained_model_no)
        trained_model.delete_instance()
