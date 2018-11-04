from src.models.db_models import *
from main import app
import unittest

class test_api(unittest.TestCase):
    def setUp(self):
        MODELS = [NNModel,NNTrainedModel,Dataset]
        # use an in-memory SQLite for tests.
        self.db_test = SqliteDatabase(':memory:')

        app.config['TESTING'] = True
        with app.app_context():
            pass
        self.client = app.test_client()

        self.db_test.bind(MODELS, bind_refs=False, bind_backrefs=False)
        self.db_test.connect()
        self.db_test.create_tables(MODELS)
        d = Dataset()
        d.name="mnist"
        d.img_depth=1
        d.img_height=28
        d.img_width=28
        d.test_images_count=0
        d.train_images_count=0
        d.labels='['+','.join(['"'+str(i)+'"' for i in range(1,11)])+']'
        d.save()
        d = Dataset()
        d.name="cifar10"
        d.img_depth=3
        d.img_height=30
        d.img_width=30
        d.test_images_count=0
        d.train_images_count=0
        d.labels='['+','.join(['"'+str(i)+'"' for i in range(1,11)])+']'
        d.save()
        self.models=[]
        for i in range(1,3):
            model=NNModel()
            model.name=f"name{i}"
            model.model_json='{"model'+str(i)+'": "model'+str(i)+'"}'
            self.models.append(model)
    
    def tearDown(self):
        self.db_test.close()

    def test_get_model_by_non_existing_id(self):
        response = self.client.get("/model/999999")
        assert response.status_code==404
    
    def test_get_model_by_id(self):
        self.models[0].save()
        self.models[1].save()
        response = self.client.get(f'/model/{self.models[1].id}')
        model = response.get_json()
        assert model['name']==self.models[1].name

    def test_get_models(self):
        self.models[0].save()
        self.models[1].save()
        response = self.client.get(f'/model')
        models = response.get_json()
        self.assertEqual(len(models),2)
        for i in range(2):
            self.assertIn("name",models[i].keys())
            self.assertIn("model_json",models[i].keys())

    def test_put_model_no_body(self):
        response = self.client.post("/model")
        assert response.status_code==400

    def test_put_model_not_json(self):
        response = self.client.post("/model",json="Lorem Ipsum")
        assert response.status_code==400

    def test_put_model_proper_json(self):
        response = self.client.post("/model",json="""{"model_json":""}""")
        assert response.status_code==200

    def test_get_model_info(self):
        self.models[1].save()
        response = self.client.get(str.format("/model/{}",self.models[1].get_id()))
        response_dict = response.get_json()
        assert response_dict["model_json"]=={"model2": "model2"}
        self.assertIn("name",response_dict.keys())
        self.assertIn("model_json",response_dict.keys())

    def test_put_train_model_incorrect_json(self):
        response = self.client.post("/trained_model",json="""{"}""")
        assert response.status_code==400

    def test_put_train_model_no_json(self):
        response = self.client.post("/trained_model")
        assert response.status_code==400

    def test_put_train_model_no_dataset(self):
        response = self.client.post("/trained_model",json="""{
        "model_id":1,
        "name":"trained_model name",
        "params":
        {
            "epochs":1,
            "batch_size":128
        }
        }""")
        assert response.status_code==400

    def test_put_train_model_no_params(self):
        response = self.client.post("/trained_model",json="""{
        "model_id":1,
        "dataset":"Mnist",
        "name":"trained_model name"
        }""")
        assert response.status_code==400

    def test_put_train_model_no_model_id(self):
        response = self.client.post("/trained_model",json="""{
        "dataset":"dataset_name",
        "name":"trained_model name",
        "params":
        {
            "epochs":epochs_number,
            "batch_size":batch_size_number
        }
        }""")
        assert response.status_code==400

    def test_put_train_model_non_existing_model_id(self):
        json="""{
            "model_id":999999,
            "dataset":"mnist",
            "name":"trained_model name",
            "params":
            {
            "epochs":1,
            "batch_size":1
            }
        }"""
        response = self.client.post("/trained_model", json=json)
        self.assertEqual(response.status_code,400)

    def test_put_train_model_OK(self):
        self.models[0].save()
        json="""{
            "model_id":1,
            "dataset":"mnist",
            "name":"trained_model name",
            "params":
            {
            "epochs":0,
            "batch_size":1
            }
        }"""
        response = self.client.post("/trained_model", json=json)
        self.assertEqual(response.status_code,200)

    def test_get_trained_model_by_id(self):
        self.models[0].save()
        m = NNTrainedModel()
        m.model=self.models[0]
        m.dataset=Dataset.get()
        m.epochs_learnt=0
        m.epochs_to_learn=0
        m.name='trained_model'
        m.save()
        response = self.client.get('/trained_model/1')
        actual = response.get_json()
        self.assertIn('id',actual.keys())
        self.assertIn('name',actual.keys())
        self.assertIn('dataset',actual.keys())
        self.assertIn('epochs_learnt',actual.keys())
        self.assertIn('epochs_to_learn',actual.keys())

    def test_get_trained_model_non_existing_id(self):
        response = self.client.get('/trained_model/999999')
        self.assertEqual(response.status_code,404)

    def test_get_trained_models(self):
        self.models[0].save()
        m = NNTrainedModel()
        m.model=self.models[0]
        m.dataset=Dataset.get()
        m.epochs_learnt=0
        m.epochs_to_learn=0
        m.name='trained_model'
        m.save()
        m = NNTrainedModel()
        m.model=self.models[0]
        m.dataset=Dataset.get()
        m.epochs_learnt=0
        m.epochs_to_learn=0
        m.name='trained_model2'
        m.save()
        response = self.client.get('/trained_model')
        self.assertEqual(response.status_code,200)
        actual = response.get_json()
        self.assertEqual(len(actual),2)

    def test_get_dataset(self):
        response = self.client.get('/data/1/')
        self.assertEqual(response.status_code,200)
        actual = response.get_json()
        self.assertIn('id',actual.keys())
        self.assertIn('name',actual.keys())
        self.assertIn('train_images_count',actual.keys())
        self.assertIn('test_images_count',actual.keys())
        self.assertIn('img_width',actual.keys())
        self.assertIn('img_height',actual.keys())
        self.assertIn('img_depth',actual.keys())
        self.assertIn('labels',actual.keys())

    def test_get_datasets(self):
        response = self.client.get('/data')
        self.assertEqual(response.status_code,200)
        actual = response.get_json()
        for i in range(2):
            self.assertIn('id',actual[i].keys())
            self.assertIn('name',actual[i].keys())
            self.assertIn('train_images_count',actual[i].keys())
            self.assertIn('test_images_count',actual[i].keys())
            self.assertIn('img_width',actual[i].keys())
            self.assertIn('img_height',actual[i].keys())
            self.assertIn('img_depth',actual[i].keys())
            self.assertIn('labels',actual[i].keys())

    def test_get_dataset_non_existing_id(self):
        response = self.client.get('/data/999999/')
        self.assertEqual(response.status_code,404)
