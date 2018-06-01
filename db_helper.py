import json
import sqlite3


def get_db():
    return sqlite3.connect("db.sqlite")

def close_db(db):
    db.close()

class Dataset:
    def __str__(self):
        return json.dumps({
                "name":self.name,
                "train_images_count":self.train_images_count,
                "test_images_count":self.test_images_count,
                "img_width":self.img_width,
                "img_height":self.img_height,
                "labels":json.loads(self.labels)
        })

class Model:
    def __str__(self):
        return json.dumps({
                "dataset":self.dataset_name,
                "epochs_learnt":self.epochs_learnt,
                "epochs_to_learn":self.epochs_to_learn
        })

def get_dataset(name):
    db = get_db()
    dataset = Dataset()
    db_dataset = db.cursor().execute("select * from datasets where name=?",(name,)).fetchone()
    close_db(db)
    if db_dataset is None:
        return None
    (dataset.id, dataset.name, dataset.train_images_count, dataset.test_images_count, dataset.img_width, dataset.img_height, dataset.dir_path, dataset.labels)=db_dataset
    return dataset

def get_model(id):
    db = get_db()
    model = Model()
    db_model = db.cursor().execute("select * from models where id=?",(id,)).fetchone()
    model.dataset_name = db.cursor().execute("select name from datasets where id=?",(db_model[1],)).fetchone()[0]
    close_db(db)
    if db_model is None:
        return None
    (model.id, _, model.epochs_learnt, model.epochs_to_learn, model.dir_path)=db_model
    return model

def add_epochs_to_learn(model_id, epochs):
    db = get_db()
    current_epochs = db.cursor().execute("select epochs_to_learn from models where id=?",(model_id,)).fetchone()[0]
    current_epochs += epochs
    db.cursor().execute("update models set epochs_to_learn=? where id=?", (current_epochs,model_id))
    db.commit()
    db.close()

def increment_learnt_epochs(model_id, value=1):
    db = get_db()
    current_epochs = db.cursor().execute("select epochs_learnt from models where id=?", (model_id,)).fetchone()[0]
    current_epochs += value
    db.cursor().execute("update models set epochs_learnt=? where id=?", (current_epochs,model_id))
    db.commit()
    db.close()