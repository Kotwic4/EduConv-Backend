from src.datasets.cifar10 import Cifar10Input
from src.datasets.mnist import MnistInput
from src.exceptions.invalid_usage import InvalidUsage

datasets_map = {"MNIST": MnistInput, "CIFAR-10": Cifar10Input}


def check_if_dataset_class_exists(dataset_name):
    if dataset_name not in datasets_map.keys():
        raise InvalidUsage("server does not support given dataset")
    return datasets_map[dataset_name]
