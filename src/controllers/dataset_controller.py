from flask import send_file, jsonify

from io import BytesIO
from src.datasets.datasets_map import check_if_dataset_class_exists
from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import Dataset, Images
from os.path import isfile


class DatasetController:

    @staticmethod
    def _get_dataset(dataset_id):
        dataset = Dataset.get_or_none(Dataset.id == dataset_id)
        if dataset is None:
            raise InvalidUsage("Dataset not found", status_code=404)
        return dataset

    @staticmethod
    def get_bitmap(dataset_id, image_no, train_set=False):
        buffer = BytesIO()
        img = Images.get_or_none().image
        with open('aaa.bmp','wb+') as aaa:
            aaa.write(img)
        buffer.write(img)
        return send_file(buffer, mimetype='image/jpg')  # , attachment_filename='1.bmp', as_attachment=True

    @staticmethod
    def get_label(dataset_id, image_no, train_set=False):
        dataset = DatasetController._get_dataset(dataset_id)
        dataset_class = check_if_dataset_class_exists(dataset.name)  # TODO: change a way of getting dataset classes

        return str.format("{{\"label\":\"{}\"}}", dataset_class.get_label(image_no, train_set))

    @staticmethod
    def get_datasets():
        return jsonify(list(map(lambda x: x.to_dict(), Dataset.select())))

    @staticmethod
    def get_dataset_info(dataset_id):
        dataset = DatasetController._get_dataset(dataset_id)
        return jsonify(dataset.to_dict())
