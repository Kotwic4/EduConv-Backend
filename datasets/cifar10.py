import numpy
from PIL import Image
from keras.utils import np_utils
import keras.backend as K

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
        self.x_train = data.reshape(data.shape[0], 3, self.img_rows, self.img_cols)
        self.x_test = test_data.reshape(test_data.shape[0], 3, self.img_rows, self.img_cols)
        if K.image_data_format() == 'channels_first':
            self.input_shape = (3, self.img_rows, self.img_cols)
        else:
            self.x_train = numpy.swapaxes(numpy.swapaxes(self.x_train,1,2),2,3)
            self.x_test = numpy.swapaxes(numpy.swapaxes(self.x_test,1,2),2,3)
            self.input_shape = (self.img_rows, self.img_cols, 3)
        self.x_train = self.x_train.astype('float32')
        self.x_test = self.x_test.astype('float32')
        self.x_train /= 255
        self.x_test /= 255
        self.y_train = np_utils.to_categorical(labels,10)
        self.y_test = np_utils.to_categorical(test_labels,10)

    @staticmethod
    def get_bitmap(image_no):
        batch_no = image_no//10000+1
        image_in_batch = image_no % 10000
        data_batch = unpickle("datasets/Cifar-10/cifar-10-batches-py/data_batch_"+str(batch_no))
        image_np_array = data_batch[b'data'].reshape(10000,3,32,32)[image_in_batch]
        numpy.swapaxes(numpy.swapaxes(image_np_array ,0,1),1,2)
        image = Image.fromarray((numpy.swapaxes(numpy.swapaxes(image_np_array, 0, 1), 1, 2) * 255).astype('uint8'),'RGB')
        return image

    @staticmethod
    def get_labels():
        meta_data = unpickle("datasets/Cifar-10/cifar-10-batches-py/batches.meta")
        return [label.decode() for label in meta_data[b'label_names']]
