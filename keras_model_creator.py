from __future__ import print_function
import keras
from keras.callbacks import Callback
from keras.layers import *
import sys
from keras.models import Sequential
import tensorflowjs as tfjs

from db_helper import add_epochs_to_learn, increment_learnt_epochs


class ProgressCallback(Callback):
    def __init__(self,model_id):
        super().__init__()
        self.model_id = model_id

    def on_epoch_end(self, epoch, logs={}):
        increment_learnt_epochs(self.model_id)

    def on_train_begin(self, logs=None):
        epochs = self.params["epochs"]
        add_epochs_to_learn(self.model_id,epochs)


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
