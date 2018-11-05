from __future__ import print_function

import json

import keras
import tensorflowjs as tfjs
from keras.callbacks import Callback
from keras.models import Sequential

from src.models.db_models import ModelEpochData


class ProgressCallback(Callback):
    def __init__(self, db_model):
        super().__init__()
        self.db_model = db_model

    def on_epoch_end(self, epoch, logs=None):
        self.db_model.epochs_learnt += 1
        self.db_model.save()
        ModelEpochData.create(model=self.db_model, epoch_number=epoch + 1, acc=logs['val_acc'], loss=logs['val_loss'])


class KerasModelBuilder:
    def __init__(self, dataset, db_model, epochs=1, batch_size=32):
        self.dataset = dataset
        self.epochs = epochs
        self.model = Sequential()
        self.batch_size = batch_size
        self.db_model = db_model

    def add_layer(self, layer_dict):
        layer_class = getattr(keras.layers, layer_dict['layer_name'])
        self.model.add(layer_class(**layer_dict['args']))

    def add_layers(self, layers_dicts):
        for layer in layers_dicts:
            self.add_layer(layer)

    def train(self, path):
        self.model.compile(loss=keras.losses.categorical_crossentropy,
                           optimizer=keras.optimizers.Adadelta(),
                           metrics=['accuracy'])
        self.set_epoch_data()
        self.model.fit(self.dataset.x_train, self.dataset.y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=0,
                       validation_data=(self.dataset.x_test, self.dataset.y_test),
                       callbacks=[ProgressCallback(db_model=self.db_model)])
        tfjs.converters.save_keras_model(self.model, path)
        keras.backend.clear_session()

    def parse_model_data(self):
        data = json.loads(self.db_model.model.model_json)
        dataset = self.db_model.dataset
        data['layers'][0]['args']['input_shape'] = [dataset.img_width, dataset.img_height, dataset.img_depth]
        for layer in reversed(data['layers']):
            if layer['layer_name'] == 'Dense':
                layer['args']['units'] = len(json.loads(dataset.labels))
                break
        return data

    def build(self, path):
        data = self.parse_model_data()
        self.add_layers(data['layers'])
        self.train(path)

    def set_epoch_data(self):
        self.db_model.epochs_to_learn = self.epochs
        self.db_model.epochs_learnt = 0
        self.db_model.save()

        ModelEpochData.delete().where(ModelEpochData.model == self.db_model).execute()
        score = self.model.evaluate(self.dataset.x_test, self.dataset.y_test, verbose=0)
        ModelEpochData.create(model=self.db_model, epoch_number=0, acc=score[1], loss=score[0])
