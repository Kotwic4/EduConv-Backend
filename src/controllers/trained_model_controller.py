from flask import send_from_directory, jsonify

from src.datasets.datasets_map import check_if_dataset_class_exists
from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import NNModel, NNTrainedModel, Dataset, ModelsQueue
from src.train.keras_model_creator import KerasModelBuilder


class TrainedModelController:

    @staticmethod
    def trained_model_path(trained_model):
        return "db/trained_models/" + str(trained_model.get_id())

    @staticmethod
    def _create_trained_model(model, dataset, params, name=None):
        trained_model = NNTrainedModel()
        trained_model.model = model
        trained_model.dataset = dataset
        trained_model.epochs_learnt = 0
        trained_model.epochs_to_learn = params['epochs']
        trained_model.batch_size = params['batch_size']
        trained_model.name = name
        return trained_model

    @staticmethod
    def _get_trained_model(trained_model_no):
        trained_model = NNTrainedModel.get_or_none(NNTrainedModel.id == trained_model_no)
        if trained_model is None:
            raise InvalidUsage("Trained model not found", status_code=404)
        return trained_model

    @staticmethod
    def train_trained_model(body):
        if body is None:
            raise InvalidUsage("Empty body",400)
        if "dataset" not in body:
            raise InvalidUsage("No dataset specified in request",400)
        try:
            model_id = body["model_id"]
            dataset_name = body["dataset"]
            name = body.get("name") #None if not found in json
            params = body["params"]
        
        except:
            raise InvalidUsage('At least one of param is missing in given json (from [model_id, dataset, params])',status_code=400)
        
        model = NNModel.get_or_none(NNModel.id == model_id)
        if model is None:
            raise InvalidUsage("model with given model id doesn't exist in database",404)
        dataset = Dataset.select().where(Dataset.name == dataset_name).get()
        check_if_dataset_class_exists(dataset_name)

        trained_model = TrainedModelController._create_trained_model(model, dataset, params, name)
        dataset_class = check_if_dataset_class_exists(trained_model.dataset.name)
        params = {'batch_size': trained_model.batch_size, 'epochs': trained_model.epochs_to_learn}
        builder = KerasModelBuilder(dataset=dataset_class(), db_model=trained_model, **params)
        if builder.validate():
            trained_model.save()
            mq = ModelsQueue()
            mq.model_to_be_trained = trained_model
            mq.save()
            return jsonify(trained_model.to_dict())
        else:
            raise InvalidUsage("Model cannot be trained on this dataset", status_code=400)

    @staticmethod
    def get_trained_model_info(trained_model_no):
        return jsonify(TrainedModelController._get_trained_model(trained_model_no).to_dict())

    @staticmethod
    def get_trained_models():
        trained_models = NNTrainedModel.select()
        return jsonify([trained_model.to_dict() for trained_model in trained_models])

    @staticmethod
    def get_trained_trained_model(trained_model_no, filename):
        trained_model = TrainedModelController._get_trained_model(trained_model_no)
        dir_path = TrainedModelController.trained_model_path(trained_model)
        return send_from_directory(dir_path, filename)

    @staticmethod
    def delete_trained_model(trained_model_no):
        trained_model = TrainedModelController._get_trained_model(trained_model_no)
        trained_model.delete_instance()
