import json
import os
import sqlite3
from os import path

import keras
import peewee
from PIL import Image

from src.datasets.cifar10 import Cifar10Input
from src.models.db_models import Dataset, NNTrainedModel, NNModel, ModelsQueue, ModelEpochData


def ensure_directory(directory):
    if not path.exists(directory):
        os.makedirs(directory)


def init_database():
    if not os.path.exists('db'):
        os.makedirs('db')
    database = peewee.SqliteDatabase('db/db.sqlite', **{})
    database.create_tables([NNTrainedModel, Dataset, NNModel, ModelsQueue, ModelEpochData])
    database.close()


def add_mnist():
    print('adding mnist')
    ensure_directory("db/datasets/mnist/train")
    ensure_directory("db/datasets/mnist/test")
    mnist = Dataset()
    mnist.img_depth = 1
    mnist.img_height = 28
    mnist.img_width = 28
    mnist.labels = json.dumps(list(str(i) for i in range(10)))
    mnist.name = "mnist"
    mnist.train_images_count = 60000
    mnist.test_images_count = 10000
 

    mnist.save()

def recreate_images_and_labels():
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    print('adding mnist labels')
    add_labels(y_train,"db/datasets/mnist/train/")
    add_labels(y_test,"db/datasets/mnist/test/")
    mnist = MnistInput()
    data = mnist.x_train
    print('adding mnist train bitmaps')
    add_bitmaps(data,"db/datasets/mnist/train/",[28,28],'L')
    data = mnist.x_test
    print('adding mnist test bitmaps')
    add_bitmaps(data,"db/datasets/mnist/test/",[28,28],'L')
    
    
def add_bitmaps(data, dataset_path, shape_of_image, image_type):
    image_array = data.reshape([data.shape[0]]+shape_of_image))
    for index, image in enumerate(image_array):
        with open(str.format(path.join(dataset_path,"{}.bmp"), index), "wb+") as f:
            img = Image.fromarray((img_array * 255).astype('uint8'),image_type).save(f, 'bmp')
            

def add_labels(data, dataset_path):
    with open(str.format(path.join(dataset_path,"labels.txt")), "w+") as f:
        f.write(" ".join([str(label) for label in y_test]))



def add_cifar(recreate_images_and_labels):
    print('adding cifar')
    db = sqlite3.connect("db/db.sqlite")
    Cifar10Input.acquire(db,recreate_images=recreate_images_and_labels)
    db.close()


if __name__ == "__main__":
    #init_database()
    #add_mnist()
    #recreate_images_and_labels()
    add_cifar(False)
