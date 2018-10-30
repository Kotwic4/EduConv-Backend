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
      response = self.client.get(f'/model/{self.models[1].id}')
      models = response.get_json()
      assert len(models)==2
      assert models


  def test_put_model_no_body(self):
      response = self.client.post("/model")
      assert response.status_code==400

  def test_put_model_not_json(self):
      response = self.client.post("/model",json="Lorem Ipsum")
      assert response.status_code==400

  def test_proper_json(self):
      response = self.client.post("/model",json="""{"model_json":""}""")
      assert response.status_code==200

  def test_get_model_info(self):
      self.models[1].save()
      response = self.client.get(str.format("/model/{}",self.models[1].get_id()))
      response_dict = response.get_json()
      assert response_dict["model_json"]=={"value1": "aaa"}

  def test_train_model_incorrect_json(self):
      response = self.client.get("/trained_model",json="""{"}""")
      assert response.status_code==400

  def test_train_model_no_json(self):
      response = self.client.get("/trained_model")
      assert response.status_code==400

  def test_train_model_no_dataset(self):
      response = self.client.get("/trained_model",json="""{
      "model_id":1,
      "name":"trained_model name",
      "params":
      {
        "epochs":1,
        "batch_size":128
      }
    }""")
      assert response.status_code==400

  def test_train_model_no_params(self):
      response = self.client.get("/trained_model",json="""{
      "model_id":1,
      "dataset":"Mnist",
      "name":"trained_model name",
      }""")
      assert response.status_code==400

  def test_train_model_no_model_id(self):
      response = self.client.get("/trained_model",json="""{
      "dataset":"dataset_name",
      "name":"trained_model name",
      "params":
      {
        "epochs":epochs_number,
        "batch_size":batch_size_number
      }
    }""")
      assert response.status_code==400

