from src.models.db_models import *
from main import app


class TestAPIBase():
    @staticmethod
    def set_up_client():
        app.config['TESTING'] = True
        with app.app_context():
            pass
        return app.test_client()

    @staticmethod
    def set_up_db():
        MODELS = [NNModel, NNTrainedModel, Dataset, ModelsQueue]
        # use an in-memory SQLite for tests.
        db_test = SqliteDatabase(':memory:')
        db_test.bind(MODELS, bind_refs=False, bind_backrefs=False)
        db_test.connect()
        db_test.create_tables(MODELS)
        d = Dataset()
        d.name = "MNIST"
        d.img_depth = 1
        d.img_height = 28
        d.img_width = 28
        d.test_images_count = 1
        d.train_images_count = 1
        d.labels = '[' + ', '.join(['"' + str(i) + '"' for i in range(1, 11)]) + ']'
        d.save()
        d2 = Dataset()
        d2.name = "cifar10"
        d2.img_depth = 3
        d2.img_height = 30
        d2.img_width = 30
        d2.test_images_count = 1
        d2.train_images_count = 1
        d2.labels = '[' + ', '.join(['"' + str(i) + '"' for i in range(1, 11)]) + ']'
        d2.save()
        models = []
        for i in range(1, 3):
            model = NNModel()
            model.name = f"name{i}"
            model.model_json = f"""{{"model{str(i)}": "model{str(i)}", "dataset": "MNIST",
            "layers": [{{"layer_name": "Conv2D", "args": {{"filters": 32, "kernel_size": [3, 3], "activation": "relu"}}}},
            {{"layer_name": "Conv2D", "args": {{"filters": 64, "kernel_size": [3, 3], "activation": "relu"}}}},
            {{"layer_name": "MaxPooling2D", "args": {{"pool_size": [2, 2]}}}},
            {{"layer_name": "Dropout", "args": {{"rate": 0.25}}}}, {{"layer_name": "Flatten", "args": {{}}}},
            {{"layer_name": "Dense", "args": {{"units": 128, "activation": "relu"}}}}, {{"layer_name": "Dropout", "args": {{"rate": 0.25}}}},
            {{"layer_name": "Dense", "args": {{"units": 10, "activation": "softmax"}}}}]}}"""
            models.append(model)

        return (db_test, models)
