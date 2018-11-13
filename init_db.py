import json
import os
import sqlite3
from os import path
import argparse

import keras
import peewee
from PIL import Image

from src.datasets.cifar10 import Cifar10Input
from src.datasets.mnist import MnistInput
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


def recreate_images_and_labels(dataset_class, shape_of_image, image_type):
    dataset = dataset_class()
    ensure_directory(f"db/datasets/{dataset.name}/train/")
    ensure_directory(f"db/datasets/{dataset.name}/test/")
    print(f'adding {dataset.name} labels')
    add_labels(dataset.y_train, dataset_class.get_labels(), f"db/datasets/{dataset.name}/train/")
    add_labels(dataset.y_test, dataset_class.get_labels(), f"db/datasets/{dataset.name}/test/")
    data = dataset.x_train
    print(f'adding {dataset.name} train bitmaps')
    add_bitmaps(data, f"db/datasets/{dataset.name}/train/", shape_of_image, image_type)
    data = dataset.x_test
    print(f'adding {dataset.name} test bitmaps')
    add_bitmaps(data, f"db/datasets/{dataset.name}/test/", shape_of_image, image_type)


def add_bitmaps(data, dataset_path, shape_of_image, image_type):
    image_array = data.reshape([data.shape[0]]+shape_of_image)
    for index, image in enumerate(image_array):
        with open(str.format(path.join(dataset_path, "{}.bmp"), index), "wb+") as f:
            img = Image.fromarray((image * 255).astype('uint8'), image_type).save(f, 'bmp')


def add_labels(data, labels, dataset_path):
    with open(str.format(path.join(dataset_path, "labels.txt")), "w+") as f:
        f.write(" ".join([str(labels[label.tolist().index(max(label))]) for label in data]))


def add_cifar():
    print('adding cifar')
    db = sqlite3.connect("db/db.sqlite")
    Cifar10Input.acquire(db, recreate_images=recreate_images_and_labels)
    db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', action='store_true')
    parser.add_argument('--mnist', action='store_true')
    parser.add_argument('--cifar10', action='store_true')
    parser.add_argument('--images', action='store_true')
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    if args.all:
        args.db = args.mnist = args.cifar10 = args.images = True
    if args.db:
        init_database()
    if args.mnist:
        add_mnist()
        if args.images:
            recreate_images_and_labels(MnistInput, [28, 28], 'L')
    if args.cifar10:
        add_cifar()
        if args.images:
            recreate_images_and_labels(Cifar10Input, [32, 32, 3], 'RGB')
