from src.models.db_models import NNTrainedModel, Dataset
from src.test.ApiTestsBase import TestAPIBase
import unittest


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
        response = self.client.post("/trained_model",
                                    json={
                                        "model_id": 1,
                                        "dataset": "MNIST",
                                        "name": "trained_model name"
                                    })
        assert response.status_code == 400

    def test_put_train_model_no_model_id(self):
        response = self.client.post("/trained_model",
                                    json={
                                        "dataset": "dataset_name",
                                        "name": "trained_model name",
                                        "params":
                                        {
                                            "epochs": 1,
                                            "batch_size": 1
                                        }
                                    })
        assert response.status_code == 400

    def test_put_train_model_non_existing_model_id(self):
        json = {
            "model_id": 999999,
            "dataset": "MNIST",
            "name": "trained_model name",
            "params":
            {
                "epochs": 1,
                "batch_size": 1
            }
        }
        response = self.client.post("/trained_model", json=json)
        self.assertEqual(response.status_code, 404)

    def test_put_train_model_OK(self):
        self.models[0].save()
        json = {
            "model_id": 1,
            "dataset": "MNIST",
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
