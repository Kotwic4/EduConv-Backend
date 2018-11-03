from time import sleep
from src.controllers.trained_model_controller import trained_ModelController
from src.models.db_models import ModelsQueue
from src.train.keras_model_creator import KerasModelBuilder
from src.datasets.datasets_map import check_if_dataset_class_exists
def start_training():
    while(True):
        queue = ModelsQueue.get_or_none()
        if queue is not None:
            model = queue.model_to_be_trained
            model.epochs_learnt=0
            model.save()
            dataset_class = check_if_dataset_class_exists(model.dataset.name)
            params = {'batch_size': model.batch_size, 'epochs': model.epochs_to_learn}
            builder = KerasModelBuilder(dataset=dataset_class(), db_model=model, **params)
            dir_path = trained_ModelController._trained_model_path(model)
            builder.build(dir_path)
            ModelsQueue.delete_by_id(queue.id)
        sleep(2)
    