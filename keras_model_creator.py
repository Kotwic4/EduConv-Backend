from __future__ import print_function
import keras
import sys
from keras.models import Sequential
import tensorflowjs as tfjs


class KerasModelBuilder:
    def __init__(self, dataset, epochs=1):
        self.dataset = dataset
        self.epochs = epochs
        self.model = Sequential()

    def add_layer(self, layer_dict):
        layer_class = getattr(sys.modules[__name__], layer_dict['layer_name'])
        self.model.add(layer_class(**layer_dict['args']))

    def build(self, path):
        self.model.compile(loss=keras.losses.categorical_crossentropy,
                           optimizer=keras.optimizers.Adadelta(),
                           metrics=['accuracy'])

        self.model.fit(self.dataset.x_train, self.dataset.y_train,
                       batch_size=self.dataset.batch_size,
                       epochs=self.epochs,
                       verbose=1,
                       validation_data=(self.dataset.x_test, self.dataset.y_test))
        score = self.model.evaluate(self.dataset.x_test, self.dataset.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        tfjs.converters.save_keras_model(self.model, path)
