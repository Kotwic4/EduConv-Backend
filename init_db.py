import json
import os
import sqlite3
from os import path
import argparse
from io import BytesIO
import keras
import peewee
from PIL import Image

from src.datasets.cifar10 import Cifar10Input
from src.datasets.mnist import MnistInput
from src.models.db_models import Dataset, NNTrainedModel, NNModel, ModelsQueue, ModelEpochData, Labels, Images


def ensure_directory(directory):
    if not path.exists(directory):
        os.makedirs(directory)


def init_database():
    if not os.path.exists('db'):
        os.makedirs('db')
    database = peewee.SqliteDatabase('db/db.sqlite', **{})
    database.create_tables([NNTrainedModel, Dataset, NNModel, ModelsQueue, ModelEpochData, Labels, Images])
    database.close()


def add_dataset(datasetInput):
    dataset = Dataset()
    dataset.img_depth = datasetInput.get_img_depth()
    dataset.img_height = datasetInput.get_img_width()
    dataset.img_width = datasetInput.get_img_width()
    dataset.labels = datasetInput.get_labels()
    dataset.name = datasetInput.get_name()
    dataset.train_images_count = datasetInput.get_x_train().shape[0]
    dataset.test_images_count = datasetInput.get_x_test().shape[0]
    dataset.save()
    return dataset.id


def recreate_images_and_labels(dataset_class, shape_of_image, image_type, dataset_id):
    dataset = dataset_class()
    labels = dataset.get_labels()
    labels_ids = {}
    for label in labels:
        new_label = Labels()
        new_label.label = label
        new_label.dataset = dataset_id
        new_label.save()
        labels_ids[label] = new_label.id
    data = dataset.get_x_train()
    print(f'adding {dataset.name} train bitmaps')
    add_bitmaps(data, dataset.get_y_train(), shape_of_image, image_type, dataset.get_labels(), dataset_id)
    data = dataset.get_x_test()
    print(f'adding {dataset.name} test bitmaps')
    add_bitmaps(data, dataset.get_y_test(), shape_of_image, image_type, dataset.get_labels(), dataset_id)


def add_bitmaps(data_x, data_y, shape_of_image, image_type, labels, dataset_id):
    labels_avaiable = Labels.select().where(Labels.dataset == dataset_id)
    labels_to_label_ids = {}
    for label in labels_avaiable:
        labels_to_label_ids[label.label] = label.id
    labels_array = [str(labels[label.tolist().index(max(label))]) for label in data_y]
    image_array = data_x.reshape([data_x.shape[0]] + shape_of_image)
    images = []
    for index, image in enumerate(image_array):
        img = Image.fromarray((image * 255).astype('uint8'), image_type)
        buffer = BytesIO()
        img.save(buffer, format='bmp')
        iii = buffer.getvalue()
        images.append((iii, labels_to_label_ids[labels_array[index]], dataset_id, index))
        buffer.close()
    Images.insert_many(images, fields=[Images.image, Images.label, Images.dataset, Images.image_no]).execute()


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
        id = add_dataset(MnistInput())
        if args.images:
            recreate_images_and_labels(MnistInput, [28, 28], 'L', id)
    if args.cifar10:
        id = add_dataset(Cifar10Input())
        if args.images:
            recreate_images_and_labels(Cifar10Input, [32, 32, 3], 'RGB', id)
