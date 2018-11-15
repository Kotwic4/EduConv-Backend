import json
import os
import pickle
import tarfile
from os import path
from urllib import request

import keras.backend as keras_b
import numpy
from PIL import Image
from keras.utils import np_utils
from src.exceptions.invalid_usage import InvalidUsage

DEFAULT_SHORT_PATH = "db/datasets/Cifar-10/"
PATH_EXTENSION = "cifar-10-batches-py/"
DEFAULT_PATH = DEFAULT_SHORT_PATH + PATH_EXTENSION


def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


class Cifar10Input:
    def __init__(self, path=None):
        self.acquire(path)
        self.name = 'Cifar-10'
        if path is not None:
            self.path = path
        else:
            self.path = DEFAULT_PATH
        self.batch_size = 32
        self.num_classes = 10

        self.img_rows, self.img_cols = (32, 32)
        data_batches = [unpickle(self.path + "data_batch_1"),
                        unpickle(self.path + "data_batch_2"),
                        unpickle(self.path + "data_batch_3"),
                        unpickle(self.path + "data_batch_4"),
                        unpickle(self.path + "data_batch_5")]
        labels = numpy.concatenate((data_batches[0][b'labels'], data_batches[1][b'labels'], data_batches[2][b'labels'],
                                    data_batches[3][b'labels'], data_batches[4][b'labels']))
        data = numpy.concatenate((data_batches[0][b'data'], data_batches[1][b'data'], data_batches[2][b'data'],
                                  data_batches[3][b'data'], data_batches[4][b'data']))
        test_labels = unpickle(self.path + "test_batch")[b'labels']
        test_data = unpickle(self.path + "test_batch")[b'data']
        self.x_train = data.reshape((data.shape[0], 3, self.img_rows, self.img_cols))
        self.x_test = test_data.reshape((test_data.shape[0], 3, self.img_rows, self.img_cols))
        if keras_b.image_data_format() == 'channels_first':
            self.input_shape = (3, self.img_rows, self.img_cols)
        else:
            self.x_train = numpy.swapaxes(numpy.swapaxes(self.x_train, 1, 2), 2, 3)
            self.x_test = numpy.swapaxes(numpy.swapaxes(self.x_test, 1, 2), 2, 3)
            self.input_shape = (self.img_rows, self.img_cols, 3)
        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255
        self.y_train = np_utils.to_categorical(labels, 10)
        self.y_test = np_utils.to_categorical(test_labels, 10)
        self.train_labels = labels
        self.test_labels = test_labels

    def acquire(self, path=None):
        url = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz'
        if path is not None:
            path = path
        else:
            path = DEFAULT_SHORT_PATH
        if not os.path.isfile(path + PATH_EXTENSION + "batches.meta"):
            file_tmp, http_message = request.urlretrieve(url)
            tar = tarfile.open(file_tmp)
            tar.extractall(path)
            tar.close()

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
        path = DEFAULT_PATH
        meta_data = unpickle(path + "batches.meta")
        return [label.decode() for label in meta_data[b'label_names']]

    def get_name(self):
        return self.name

    def get_num_classes(self):
        return self.num_classes

    def get_img_depth(self):
        return 3

    def get_img_width(self):
        return 32

    def get_img_height(self):
        return 32
