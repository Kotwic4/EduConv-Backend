from __future__ import print_function
import keras
import sys
from keras.datasets import mnist
from keras.models import Sequential
from  keras.layers import *
from keras import backend as K
import tensorflowjs as tfjs


class KerasModelBuilder:
    def __init__(self):
        self.batch_size = 128
        self.num_classes = 10
        self.epochs = 1

        # input image dimensions
        self.img_rows, self.img_cols = 28, 28

        # the data, split between train and test sets
        (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()

        if K.image_data_format() == 'channels_first':
            self.x_train = self.x_train.reshape(self.x_train.shape[0], 1, self.img_rows, self.img_cols)
            self.x_test = self.x_test.reshape(self.x_test.shape[0], 1, self.img_rows, self.img_cols)
            self.input_shape = (1, self.img_rows, self.img_cols)
        else:
            self.x_train = self.x_train.reshape(self.x_train.shape[0], self.img_rows, self.img_cols, 1)
            self.x_test = self.x_test.reshape(self.x_test.shape[0], self.img_rows, self.img_cols, 1)
            self.input_shape = (self.img_rows, self.img_cols, 1)

        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255
        print('x_train shape:', self.x_train.shape)
        print(self.x_train.shape[0], 'train samples')
        print(self.x_test.shape[0], 'test samples')

        # convert class vectors to binary class matrices
        self.y_train = keras.utils.to_categorical(self.y_train, self.num_classes)
        self.y_test = keras.utils.to_categorical(self.y_test, self.num_classes)

        self.model = Sequential()


    def add_layer(self,layer_dict):
        layer_class = getattr(sys.modules[__name__],layer_dict['layer_name'])
        self.model.add(layer_class(**layer_dict['args']))

    def build(self, path):
        self.model.compile(loss=keras.losses.categorical_crossentropy,
                           optimizer=keras.optimizers.Adadelta(),
                           metrics=['accuracy'])

        self.model.fit(self.x_train, self.y_train,
                       batch_size=self.batch_size,
                       epochs=self.epochs,
                       verbose=1,
                       validation_data=(self.x_test, self.y_test))
        score = self.model.evaluate(self.x_test, self.y_test, verbose=0)
        print('Test loss:', score[0])
        print('Test accuracy:', score[1])
        tfjs.converters.save_keras_model(self.model,path)
