from os import path

import keras
import keras.backend as K
from keras.datasets import mnist
from os import path
from src.exceptions.invalid_usage import InvalidUsage


class MnistInput:
    def __init__(self):
        self.name = 'MNIST'
        self.batch_size = 128
        self.num_classes = 10
        # input image dimensions
        self.img_rows, self.img_cols = 28, 28

        # the data, split between train and test sets
        (self.x_train, self.y_train), (self.x_test, self.y_test) = mnist.load_data()

        if K.image_data_format() == 'channels_first':
            self.x_train = self.x_train.reshape((self.x_train.shape[0], 1, self.img_rows, self.img_cols))
            self.x_test = self.x_test.reshape((self.x_test.shape[0], 1, self.img_rows, self.img_cols))
            self.input_shape = (1, self.img_rows, self.img_cols)
        else:
            self.x_train = self.x_train.reshape((self.x_train.shape[0], self.img_rows, self.img_cols, 1))
            self.x_test = self.x_test.reshape((self.x_test.shape[0], self.img_rows, self.img_cols, 1))
            self.input_shape = (self.img_rows, self.img_cols, 1)

        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255

        # convert class vectors to binary class matrices
        self.y_train = keras.utils.to_categorical(self.y_train, self.num_classes)
        self.y_test = keras.utils.to_categorical(self.y_test, self.num_classes)

    # IDatasetInput implementation:
    def get_x_train(self):
        return self.x_train

    def get_x_test(self):
        return self.x_test

    def get_y_train(self):
        return self.y_train

    def get_y_test(self):
        return self.y_test

    def get_labels(self):
        return [f"{i}" for i in range(10)]

    def get_name(self):
        return self.name

    def get_num_classes(self):
        return self.num_classes

    def get_img_depth(self):
        return 1

    def get_img_width(self):
        return 28

    def get_img_height(self):
        return 28
