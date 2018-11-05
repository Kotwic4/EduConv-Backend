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
    img_depth = IntegerField(column_name='img_depth',
                             constraints=[Check('img_depth > 0')],
                             default=1,
                             unique=False,
                             null=False)
    img_height = IntegerField(column_name='img_height',
                              constraints=[Check('img_height > 0')],
                              default=1,
                              unique=False,
                              null=False)
    img_width = IntegerField(column_name='img_width',
                             constraints=[Check('img_width > 0')],
                             default=1,
                             unique=False,
                             null=False)
    labels = TextField(column_name='labels',
                       unique=False,
                       null=False)
    name = TextField(column_name='name',
                     unique=True,
                     null=False)
    test_images_count = IntegerField(column_name='test_images_count',
                                     constraints=[Check('test_images_count >= 0')],
                                     default=0,
                                     unique=False,
                                     null=False)
    train_images_count = IntegerField(column_name='train_images_count',
                                      constraints=[Check('train_images_count >= 0')],
                                      default=0,
                                      unique=False,
                                      null=False)

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
            "name": self.name
        }


class NNTrainedModel(BaseModel):
    dataset = ForeignKeyField(column_name='dataset_id',
                              field='id',
                              model=Dataset,
                              null=False,
                              unique=False)
    epochs_learnt = IntegerField(column_name='epochs_learnt',
                                 constraints=[Check('epochs_learnt >= 0')],
                                 default=0,
                                 unique=False,
                                 null=False)
    epochs_to_learn = IntegerField(column_name='epochs_to_learn',
                                   constraints=[Check('epochs_to_learn > 0')],
                                   default=1,
                                   unique=False,
                                   null=False)
    model = ForeignKeyField(column_name='model_id',
                            field='id',
                            model=NNModel,
                            unique=False,
                            null=False)
    name = TextField(column_name='name',
                     unique=False,
                     null=True)
    batch_size = IntegerField(column_name='batch_size',
                              constraints=[Check('batch_size > 0')],
                              default=1,
                              unique=False,
                              null=False)

    def to_dict(self):
        return {
            "id": self.get_id(),
            "dataset": self.dataset.to_dict(),
            "epochs_learnt": self.epochs_learnt,
            "epochs_to_learn": self.epochs_to_learn,
            "batch_size": self.batch_size,
            "name": self.name,
            "model_id": self.model.id,
            "epochs_data": self.epochs_data()
        }

    def epochs_data(self):
        epoch_data_list = list(ModelEpochData
                               .select()
                               .where(ModelEpochData.model == self))
        epoch_data_dict = {}
        for x in epoch_data_list:
            epoch_data_dict[x.epoch_number] = x.to_dict()
        return epoch_data_dict

    class Meta:
        table_name = 'trained_models'


class ModelEpochData(BaseModel):
    model = ForeignKeyField(column_name='trained_model_id',
                            field='id',
                            model=NNTrainedModel,
                            unique=False,
                            null=False)
    epoch_number = IntegerField(column_name='epoch_number',
                                constraints=[Check('epoch_number >= 0')],
                                unique=False,
                                null=False)
    acc = DoubleField(column_name='acc',
                      constraints=[Check('acc >= 0')],
                      unique=False,
                      null=False)
    loss = DoubleField(column_name='loss',
                       constraints=[Check('loss >= 0')],
                       unique=False,
                       null=False)

    def to_dict(self):
        return {
            "acc": self.acc,
            "loss": self.loss
        }

    class Meta:
        table_name = 'model_epoch_data'
        primary_key = False
        constraints = [SQL('UNIQUE(trained_model_id, epoch_number)')]


class ModelsQueue(BaseModel):
    model_to_be_trained = ForeignKeyField(column_name='trained_model_id',
                                          field='id',
                                          model=NNTrainedModel,
                                          unique=True,
                                          null=False)

    class Meta:
        table_name = 'models_queue'
