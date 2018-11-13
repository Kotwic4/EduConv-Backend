from src.test.ApiTestsBase import TestAPIBase
import unittest


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
