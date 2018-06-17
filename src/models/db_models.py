import json

import peewee

database = peewee.SqliteDatabase('db.sqlite', **{})


class BaseModel(peewee.Model):
    class Meta:
        database = database


class Dataset(BaseModel):
    img_depth = peewee.IntegerField(null=True)
    img_height = peewee.IntegerField(null=True)
    img_width = peewee.IntegerField(null=True)
    labels = peewee.TextField(null=True)
    name = peewee.TextField(null=True, unique=True)
    test_images_count = peewee.IntegerField(null=True)
    train_images_count = peewee.IntegerField(null=True)

    def to_json(self):
        return json.dumps({
            "id": self.get_id(),
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
    scheme_json = peewee.TextField(null=False)

    class Meta:
        table_name = 'schemes'

    def to_json(self):
        return json.dumps({"id": self.get_id(), "scheme_json": json.loads(self.scheme_json)})


class Model(BaseModel):
    dataset = peewee.ForeignKeyField(column_name='dataset_id', field='id', model=Dataset, null=True)
    epochs_learnt = peewee.IntegerField(constraints=[peewee.SQL("DEFAULT 0")], null=True)
    epochs_to_learn = peewee.IntegerField(constraints=[peewee.SQL("DEFAULT 0")], null=True)
    scheme = peewee.ForeignKeyField(column_name='scheme_id', field='id', model=Scheme, null=True)

    def to_json(self):
        return json.dumps({
            "id": self.get_id(),
            "dataset": self.dataset.toJSON,
            "epochs_learnt": self.epochs_learnt,
            "epochs_to_learn": self.epochs_to_learn
        })

    class Meta:
        table_name = 'models'
