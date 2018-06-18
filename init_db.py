import json

import peewee
import sqlite3

from src.datasets.cifar10 import Cifar10Input
from src.models.db_models import Dataset, Model, Scheme

database = peewee.SqliteDatabase('db/db.sqlite', **{})


def init_database():
    database.create_tables([Model, Dataset, Scheme])
    database.close()


def add_mnist():
    mnist = Dataset()
    mnist.img_depth = 1
    mnist.img_height = 28
    mnist.img_width = 28
    mnist.labels = json.dumps(list(str(i) for i in range(10)))
    mnist.name = "mnist"
    mnist.train_images_count = 60000
    mnist.test_images_count = 10000
    mnist.save()
    
    
def add_cifar():
    db = sqlite3.connect("db/db.sqlite")
    Cifar10Input.acquire(db)
    db.close()


if __name__ == "__main__":
    init_database()
    add_mnist()
    add_cifar()
