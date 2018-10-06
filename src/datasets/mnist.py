import keras
import keras.backend as K
from PIL import Image
from keras.datasets import mnist


class MnistInput:
    def __init__(self):
        self.batch_size = 128
        self.num_classes = 10

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

        # convert class vectors to binary class matrices
        self.y_train = keras.utils.to_categorical(self.y_train, self.num_classes)
        self.y_test = keras.utils.to_categorical(self.y_test, self.num_classes)

    @staticmethod
    def get_bitmap(image_no, from_train_dataset=False):
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        if from_train_dataset:
            data = x_train
        else:
            data = x_test
        image_array = data.reshape(data.shape[0], 28, 28)[image_no].astype('uint8')
        return Image.fromarray(image_array, 'L')

    @staticmethod
    def get_bitmap_directory(train_dataset=False):
        if(train_dataset):    
            return "db/datasets/mnist/train/"
        return "db/datasets/mnist/test/"

    @staticmethod
    def get_label(image_no, train_dataset=False):
        
        if train_dataset:
            with open("db/datasets/mnist/train/labels.txt","r") as f:
                return f.readline().split(' ')[image_no]
        with open("db/datasets/mnist/test/labels.txt","r") as f:
                return f.readline().split(' ')[image_no]
