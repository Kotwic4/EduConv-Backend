import json

from peewee import *

database = SqliteDatabase('db.sqlite', **{})


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Dataset(BaseModel):
    dir_path = TextField(null=True)
    img_depth = IntegerField(null=True)
    img_height = IntegerField(null=True)
    img_width = IntegerField(null=True)
    labels = TextField(null=True)
    name = TextField(null=True, unique=True)
    test_images_count = IntegerField(null=True)
    train_images_count = IntegerField(null=True)

    def toJSON(self):
        return json.dumps({
            "id":self.get_id(),
            "name": self.name,
            "train_images_count": self.train_images_count,
            "test_images_count": self.test_images_count,
            "img_width": self.img_width,
            "img_height": self.img_height,
            "labels": json.loads(self.labels)
        })

    class Meta:
        table_name = 'datasets'


class Scheme(BaseModel):
    scheme_json = TextField(null=False)

    class Meta:
        table_name = 'schemes'

    def toJSON(self):
        return json.dumps({"id":self.get_id(),"scheme_json":json.loads(self.scheme_json)})

class Model(BaseModel):
    dataset = ForeignKeyField(column_name='dataset_id', field='id', model=Dataset, null=True)
    dir_path = TextField(null=True)
    epochs_learnt = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    epochs_to_learn = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    scheme = ForeignKeyField(column_name='scheme_id', field='id', model=Scheme, null=True)

    def toJSON(self):
        return json.dumps({
            "id":self.get_id(),
            "dataset":self.dataset.name,
            "epochs_learnt":self.epochs_learnt,
            "epochs_to_learn":self.epochs_to_learn
        })


    class Meta:
        table_name = 'models'


def init_database():
    database.create_tables([Model, Dataset,Scheme])
    database.close()


def add_mnist():
    mnist = Dataset()
    mnist.img_depth = 1
    mnist.img_height = 28
    mnist.img_width = 28
    mnist.labels = json.dumps(list(str(i) for i in range(10)))
    mnist.name = "mnist"
    mnist.train_images_count = 60000
    mnist.test_images_count = 10000
    mnist.save()


if __name__ == "__main__":
    init_database()
    if len(Dataset.select().where(Dataset.name == "mnist")) == 0:
        add_mnist()
