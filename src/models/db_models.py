import json

from peewee import *

database = SqliteDatabase('db/db.sqlite', **{})


class BaseModel(Model):
    class Meta:
        database = database

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        pass


class Dataset(BaseModel):
    img_depth = IntegerField(null=True)
    img_height = IntegerField(null=True)
    img_width = IntegerField(null=True)
    labels = TextField(null=True)
    name = TextField(null=True, unique=True)
    test_images_count = IntegerField(null=True)
    train_images_count = IntegerField(null=True)

    def to_dict(self):
        return {
            "id": self.get_id(),
            "name": self.name,
            "train_images_count": self.train_images_count,
            "test_images_count": self.test_images_count,
            "img_width": self.img_width,
            "img_height": self.img_height,
            "img_depth": self.img_depth,
            "labels": json.loads(self.labels)
        }

    class Meta:
        table_name = 'datasets'


class NNModel(BaseModel):
    model_json = TextField(null=False)
    name = TextField(null=True)

    class Meta:
        table_name = 'models'

    def to_dict(self):
        return {
            "id": self.get_id(), 
            "model_json": json.loads(self.model_json), 
            "name":self.name
            }


class NNTrainedModel(BaseModel):
    dataset = ForeignKeyField(column_name='dataset_id', field='id', model=Dataset, null=True)
    epochs_learnt = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    epochs_to_learn = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    model = ForeignKeyField(column_name='scheme_id', field='id', model=NNModel, null=True)
    name = TextField(null=True)
    batch_size = IntegerField(column_name='batch_size')
    def to_dict(self):
        return {
            "id": self.get_id(),
            "dataset": self.dataset.to_dict(),
            "epochs_learnt": self.epochs_learnt,
            "epochs_to_learn": self.epochs_to_learn,
            "batch_size": self.batch_size,
            "name": self.name
        }

    class Meta:
        table_name = 'trainedModels'

class ModelsQueue(BaseModel):
    model_to_be_trained = ForeignKeyField(column_name='trained_model_id', field='id', model=NNTrainedModel, null=False)
    class Meta:
        table_name = 'ModelsQueue'
