from src.models.db_models import *
from main import app
import unittest


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
        d.name = "mnist"
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
            model.model_json = f"""{{"model{str(i)}": "model{str(i)}", "dataset": "mnist",
            "layers": [{{"layer_name": "Conv2D", "args": {{"filters": 32, "kernel_size": [3, 3], "activation": "relu"}}}},
            {{"layer_name": "Conv2D", "args": {{"filters": 64, "kernel_size": [3, 3], "activation": "relu"}}}},
            {{"layer_name": "MaxPooling2D", "args": {{"pool_size": [2, 2]}}}},
            {{"layer_name": "Dropout", "args": {{"rate": 0.25}}}}, {{"layer_name": "Flatten", "args": {{}}}},
            {{"layer_name": "Dense", "args": {{"units": 128, "activation": "relu"}}}}, {{"layer_name": "Dropout", "args": {{"rate": 0.25}}}},
            {{"layer_name": "Dense", "args": {{"units": 10, "activation": "softmax"}}}}]}}"""
            models.append(model)

        return (db_test, models)


class TestModelController(unittest.TestCase):

    def setUp(self):
        self.client = TestAPIBase.set_up_client()
        self.db_test, self.models = TestAPIBase.set_up_db()

    def tearDown(self):
        self.db_test.close()

    def test_get_model_by_non_existing_id(self):
        response = self.client.get("/model/999999")
        assert response.status_code == 404

    def test_get_model_by_id(self):
        self.models[0].save()
        self.models[1].save()
        response = self.client.get(f'/model/{self.models[1].id}')
        model = response.get_json()
        assert model['name'] == self.models[1].name

    def test_get_models(self):
        self.models[0].save()
        self.models[1].save()
        response = self.client.get(f'/model')
        models = response.get_json()
        self.assertEqual(len(models), 2)
        for i in range(2):
            self.assertIn("name", models[i].keys())
            self.assertIn("model_json", models[i].keys())

    def test_put_model_no_body(self):
        response = self.client.post("/model")
        assert response.status_code == 400

    def test_put_model_not_json(self):
        response = self.client.post("/model", json="Lorem Ipsum")
        assert response.status_code == 400

    def test_put_model_with_no_model_id(self):
        response = self.client.post("/model", json={"model_json": ""})
        assert response.status_code == 400
    
    def test_put_model_proper_json(self):
        response = self.client.post("/model", json=self.models[0].to_dict())
        assert response.status_code == 400

    def test_get_model_info(self):
        self.models[1].save()
        response = self.client.get(str.format("/model/{}", self.models[1].get_id()))
        response_dict = response.get_json()
        self.assertIn("model2",response_dict["model_json"])
        self.assertIn("name", response_dict.keys())
        self.assertIn("model_json", response_dict.keys())


class TestTrainedModelController(unittest.TestCase):
    def setUp(self):
        self.client = TestAPIBase.set_up_client()
        self.db_test, self.models = TestAPIBase.set_up_db()

    def tearDown(self):
        self.db_test.close()

    def test_put_train_model_incorrect_json(self):
        response = self.client.post("/trained_model", json="""{"}""")
        assert response.status_code == 400

    def test_put_train_model_no_json(self):
        response = self.client.post("/trained_model")
        assert response.status_code == 400

    def test_put_train_model_no_dataset(self):
        response = self.client.post("/trained_model", json="""{
        "model_id": 1,
        "name": "trained_model name",
        "params":
        {
            "epochs": 1,
            "batch_size": 128
        }
        }""")
        assert response.status_code == 400

    def test_put_train_model_no_params(self):
        response = self.client.post("/trained_model", json="""{
        "model_id": 1,
        "dataset": "Mnist",
        "name": "trained_model name"
        }""")
        assert response.status_code == 400

    def test_put_train_model_no_model_id(self):
        response = self.client.post("/trained_model", json="""{
        "dataset": "dataset_name",
        "name": "trained_model name",
        "params":
        {
            "epochs": epochs_number,
            "batch_size": batch_size_number
        }
        }""")
        assert response.status_code == 400

    def test_put_train_model_non_existing_model_id(self):
        json = """{
            "model_id": 999999,
            "dataset": "mnist",
            "name": "trained_model name",
            "params":
            {
            "epochs": 1,
            "batch_size": 1
            }
        }"""
        response = self.client.post("/trained_model", json=json)
        self.assertEqual(response.status_code, 400)

    def test_put_train_model_OK(self):
        self.models[0].save()
        json = {
            "model_id": 1,
            "dataset": "mnist",
            "name": "trained_model name",
            "params":
            {
                "epochs": 1,
                "batch_size": 1
            }
        }
        response = self.client.post("/trained_model", json=json)
        self.assertEqual(response.status_code, 200)

    def test_get_trained_model_by_id(self):
        self.models[0].save()
        m = NNTrainedModel()
        m.model = self.models[0]
        m.dataset = Dataset.get()
        m.epochs_learnt == 1
        m.epochs_to_learn == 1
        m.name = 'trained_model'
        m.batch_size == 100
        m.save()
        response = self.client.get('/trained_model/1')
        actual = response.get_json()
        self.assertIn('id', actual.keys())
        self.assertIn('name', actual.keys())
        self.assertIn('dataset', actual.keys())
        self.assertIn('epochs_learnt', actual.keys())
        self.assertIn('epochs_to_learn', actual.keys())

    def test_get_trained_model_non_existing_id(self):
        response = self.client.get('/trained_model/999999')
        self.assertEqual(response.status_code, 404)

    def test_get_trained_models(self):
        self.models[0].save()
        m = NNTrainedModel()
        m.model = self.models[0]
        m.dataset = Dataset.get()
        m.epochs_learnt == 1
        m.epochs_to_learn == 1
        m.name = 'trained_model'
        m.batch_size == 100
        m.save()
        m = NNTrainedModel()
        m.model = self.models[0]
        m.dataset = Dataset.get()
        m.epochs_learnt == 1
        m.epochs_to_learn == 1
        m.name = 'trained_model2'
        m.batch_size == 100
        m.save()
        response = self.client.get('/trained_model')
        self.assertEqual(response.status_code, 200)
        actual = response.get_json()
        self.assertEqual(len(actual), 2)


class TestDatasetController(unittest.TestCase):
    def setUp(self):
        self.client = TestAPIBase.set_up_client()
        self.db_test, self.models = TestAPIBase.set_up_db()

    def tearDown(self):
        self.db_test.close()

    def test_get_dataset(self):
        response = self.client.get('/data/1/')
        self.assertEqual(response.status_code, 200)
        actual = response.get_json()
        self.assertIn('id', actual.keys())
        self.assertIn('name', actual.keys())
        self.assertIn('train_images_count', actual.keys())
        self.assertIn('test_images_count', actual.keys())
        self.assertIn('img_width', actual.keys())
        self.assertIn('img_height', actual.keys())
        self.assertIn('img_depth', actual.keys())
        self.assertIn('labels', actual.keys())

    def test_get_datasets(self):
        response = self.client.get('/data')
        self.assertEqual(response.status_code, 200)
        actual = response.get_json()
        for i in range(2):
            self.assertIn('id', actual[i].keys())
            self.assertIn('name', actual[i].keys())
            self.assertIn('train_images_count', actual[i].keys())
            self.assertIn('test_images_count', actual[i].keys())
            self.assertIn('img_width', actual[i].keys())
            self.assertIn('img_height', actual[i].keys())
            self.assertIn('img_depth', actual[i].keys())
            self.assertIn('labels', actual[i].keys())

    def test_get_dataset_non_existing_id(self):
        response = self.client.get('/data/999999/')
        self.assertEqual(response.status_code, 404)
