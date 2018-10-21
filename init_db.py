import json

import os
from os import path

import keras
import peewee
import sqlite3

from PIL import Image

from src.datasets.cifar10 import Cifar10Input
from src.models.db_models import Dataset, NNTrainedModel, NNModel

def ensure_directory(directory):
    if not path.exists(directory):
        os.makedirs(directory)


def init_database():
    if not os.path.exists('db'):
        os.makedirs('db')
    database = peewee.SqliteDatabase('db/db.sqlite', **{})
    database.create_tables([NNTrainedModel, Dataset, NNModel])
    database.close()


def add_mnist():
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
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
    print('adding mnist labels')
    with open(str.format("db/datasets/mnist/train/labels.txt"),"w+") as f:
        f.write(" ".join([str(label) for label in y_train]))
    with open(str.format("db/datasets/mnist/test/labels.txt"),"w+") as f:
        f.write(" ".join([str(label) for label in y_test]))
    data = x_train
    print('adding mnist train bitmaps')
    image_array = data.reshape(data.shape[0], 28, 28)
    for index, image in enumerate(image_array):
        with open(str.format("db/datasets/mnist/train/{}.bmp",index),"wb+") as f:
            Image.fromarray(image, 'L').save(f, 'bmp')
    data = x_test
    print('adding mnist test bitmaps')
    image_array = data.reshape(data.shape[0], 28, 28)
    for index, image in enumerate(image_array):
        with open(str.format("db/datasets/mnist/test/{}.bmp", index), "wb+") as f:
            Image.fromarray(image, 'L').save(f, 'bmp')

    mnist.save()
    
    
def add_cifar():
    db = sqlite3.connect("db/db.sqlite")
    Cifar10Input.acquire(db)
    db.close()


if __name__ == "__main__":
    init_database()
    add_mnist()
    print('adding cifar')
    add_cifar()
