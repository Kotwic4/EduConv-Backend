from __future__ import print_function

import sys
from keras.layers import *
import keras
import tensorflowjs as tfjs
from keras.callbacks import Callback
from keras.models import Sequential

from db_models import Model


class ProgressCallback(Callback):
    def __init__(self,model_id):
        super().__init__()
        self.db_model = Model.select().where(Model.id==model_id).get()

    def on_epoch_end(self, epoch, logs={}):
        self.db_model.epochs_learnt+=1
        self.db_model.save()

    def on_train_begin(self, logs=None):
        epochs = self.params["epochs"]
        self.db_model.epochs_to_learn += epochs
        self.db_model.save()


class KerasModelBuilder:
    def __init__(self, dataset, model_id, epochs=1, batch_size=32):
        self.dataset = dataset
        self.epochs = epochs
        self.model = Sequential()
        self.batch_size=batch_size
        self.model_id=model_id

    def add_layer(self, layer_dict):
        layer_class = getattr(sys.modules[__name__], layer_dict['layer_name'])
        self.model.add(layer_class(**layer_dict['args']))

    def build(self, path):
        self.model.compile(loss=keras.losses.categorical_crossentropy,
                           optimizer=keras.optimizers.Adadelta(),
                           metrics=['accuracy'])

        self.model.fit(self.dataset.x_train, self.dataset.y_train,
                                batch_size=self.batch_size,
                                epochs=self.epochs,
                                verbose=1,
                                validation_data=(self.dataset.x_test, self.dataset.y_test),
                                callbacks=[ProgressCallback(model_id=self.model_id)])
        score = self.model.evaluate(self.dataset.x_test, self.dataset.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        tfjs.converters.save_keras_model(self.model, path)
        keras.backend.clear_session()
