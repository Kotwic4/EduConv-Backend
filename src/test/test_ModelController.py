from src.test.ApiTestsBase import TestAPIBase

import unittest


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
        assert response.status_code == 200

    def test_get_model_info(self):
        self.models[1].save()
        response = self.client.get(str.format("/model/{}", self.models[1].get_id()))
        response_dict = response.get_json()
        self.assertIn("model2", response_dict["model_json"])
        self.assertIn("name", response_dict.keys())
        self.assertIn("model_json", response_dict.keys())
