from flask import send_file, jsonify
import json
from io import BytesIO
from src.datasets.datasets_map import check_if_dataset_class_exists
from src.exceptions.invalid_usage import InvalidUsage
from src.models.db_models import Dataset, Images, Labels
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
        img = Images.get_or_none((Images.image_no == image_no) & (Images.dataset == dataset_id))
        buffer = BytesIO(img.image)
        return send_file(buffer, mimetype='image/bmp')

    @staticmethod
    def get_label(dataset_id, image_no, train_set=False):
        dataset = DatasetController._get_dataset(dataset_id)
        label = Labels.select().join(Images).where((Images.dataset == dataset_id) & (Images.image_no == image_no) & (Images.is_train == train_set)).get().label
        return str.format("{{\"label\":\"{}\"}}", label)

    @staticmethod
    def get_labels(dataset_id, image_numbers, train_set=False):
        dataset = DatasetController._get_dataset(dataset_id)
        labels = Labels.select(Labels.label, Images.image_no).join(Images).where((Images.dataset == dataset_id)
               & (Images.image_no.in_(image_numbers)
               & (Images.is_train == train_set))).dicts()
        return json.dumps({"labels": [l for l in labels]})

    @staticmethod
    def get_datasets():
        return jsonify(list(map(lambda x: x.to_dict(), Dataset.select())))

    @staticmethod
    def get_dataset_info(dataset_id):
        dataset = DatasetController._get_dataset(dataset_id)
        return jsonify(dataset.to_dict())
