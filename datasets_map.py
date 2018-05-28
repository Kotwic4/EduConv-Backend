from datasets.cifar10 import Cifar10Input
from datasets.mnist import MnistInput
from exceptions import InvalidUsage

datasets_map = {"mnist":MnistInput, "cifar-10":Cifar10Input}

def get_dataset_class(dataset_name):
    if dataset_name not in datasets_map.keys():
        raise InvalidUsage("server does not support given dataset")
    return datasets_map[dataset_name]