import numpy
from keras.utils import np_utils

from image_util import generate_24bit_color_bitmap


def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict
class Cifar10Input:
    def __init__(self):
        self.batch_size=32
        self.num_classes=10

        self.img_rows, self.img_cols = (32, 32)
        data_batches = [unpickle("datasets/Cifar-10/cifar-10-batches-py/data_batch_1"),
                        unpickle("datasets/Cifar-10/cifar-10-batches-py/data_batch_2"),
                        unpickle("datasets/Cifar-10/cifar-10-batches-py/data_batch_3"),
                        unpickle("datasets/Cifar-10/cifar-10-batches-py/data_batch_4"),
                        unpickle("datasets/Cifar-10/cifar-10-batches-py/data_batch_5")]
        labels = numpy.concatenate((data_batches[0][b'labels'],data_batches[1][b'labels'],data_batches[2][b'labels'],data_batches[3][b'labels'],data_batches[4][b'labels']))
        data = numpy.concatenate((data_batches[0][b'data'],data_batches[1][b'data'],data_batches[2][b'data'],data_batches[3][b'data'],data_batches[4][b'data']))
        test_labels = unpickle("datasets/Cifar-10/cifar-10-batches-py/test_batch")[b'labels']
        test_data = unpickle("datasets/Cifar-10/cifar-10-batches-py/test_batch")[b'data']
        self.x_train = data.reshape(50000,3,self.img_rows,self.img_cols).astype("float32")
        self.x_test = test_data.reshape(10000,3,self.img_rows,self.img_cols).astype("float32")
        self.x_train /= 255
        self.x_test /= 255
        self.y_train = np_utils.to_categorical(labels,10)
        self.y_test = np_utils.to_categorical(test_labels,10)
# cifar = Cifar10Input()
# image = generate_24bit_color_bitmap(32,32,(numpy.swapaxes(numpy.swapaxes(cifar.x_train[1],0,1),1,2)*255).astype('uint8'))
# image.show()