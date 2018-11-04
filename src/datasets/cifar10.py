import json
import os
import pickle
import tarfile
from urllib import request
from os import path
import keras.backend as keras_b
import numpy
from PIL import Image
from keras.utils import np_utils
from src.exceptions.invalid_usage import InvalidUsage

DEFAULT_SHORT_PATH = "db/datasets/Cifar-10/"
PATH_EXTENSION = "cifar-10-batches-py/"
DEFAULT_PATH = DEFAULT_SHORT_PATH+PATH_EXTENSION

def unpickle(file):
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict


class Cifar10Input:
    def __init__(self, path=None):
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
        self.x_train = data.reshape(data.shape[0], 3, self.img_rows, self.img_cols)
        self.x_test = test_data.reshape(test_data.shape[0], 3, self.img_rows, self.img_cols)
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
        self.test_labels=test_labels
        

    @staticmethod
    def acquire(db, path=None):
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
        path = path + PATH_EXTENSION
        if db.cursor().execute('SELECT * FROM datasets WHERE name=?', ('cifar-10',)).fetchone() is None:
            db.cursor().execute('INSERT INTO datasets'
                                '(name,train_images_count,test_images_count,img_width,img_height,img_depth,labels) '
                                'VALUES (?,?,?,?,?,?,?)',
                                ["cifar-10", 50000, 10000, 32, 32, 3,
                                 str(json.dumps(Cifar10Input.get_labels(path)))])
            db.commit()
        c = Cifar10Input()
        Cifar10Input.save_images(c.x_train,c.train_labels,Cifar10Input.get_bitmap_directory(True))
        Cifar10Input.save_images(c.x_test,c.test_labels,Cifar10Input.get_bitmap_directory(False))

    @staticmethod
    def save_images(image_set, labels_set, bitmap_directory):
        labels = Cifar10Input.get_labels()
        ensure_directory(bitmap_directory)
        for i, img_array in enumerate(image_set):
            img_path = os.path.join(bitmap_directory,str(i)+".bmp")
            img = Image.fromarray((img_array * 255).astype('uint8'))
            img.save(img_path,'bmp')
        with open(os.path.join(bitmap_directory,"labels.txt"),"w+") as labels_file:
            labels_file.writelines([labels[i]+" " for i in labels_set])

    @staticmethod
    def get_labels(path=None):
        if path is not None:
            path = path
        else:
            path = DEFAULT_PATH
        meta_data = unpickle(path + "batches.meta")
        return [label.decode() for label in meta_data[b'label_names']]

    @staticmethod
    def get_bitmap_directory(train_dataset=False):
        if train_dataset:
            return "db/datasets/Cifar-10/train/"
        return "db/datasets/Cifar-10/test/"

    @staticmethod
    def get_label(image_no, train_dataset=False):
        bitmap_path = Cifar10Input.get_bitmap_directory(train_dataset)
        bitmap_path = path.join(bitmap_path,"labels.txt")
        with open(bitmap_path,"r") as f:
            line = f.readline()
            labels = line.split(' ')
            if image_no >= len(labels):
                raise InvalidUsage("Label not found",404)
            return labels[image_no]

def ensure_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
