from __future__ import print_function
import keras
from keras.callbacks import Callback
from keras.layers import *
import sys
from keras.models import Sequential
import tensorflowjs as tfjs


class ProgressCallback(Callback):
    def on_epoch_end(self, epoch, logs={}):
        print("my callback epoch", epoch)
        #TODO: update model in database


class KerasModelBuilder:
    def __init__(self, dataset, epochs=1, batch_size=32):
        self.dataset = dataset
        self.epochs = epochs
        self.model = Sequential()
        self.batch_size=batch_size

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
                                callbacks=[ProgressCallback()])
        score = self.model.evaluate(self.dataset.x_test, self.dataset.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        tfjs.converters.save_keras_model(self.model, path)
        keras.backend.clear_session()
