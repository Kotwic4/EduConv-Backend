import json
import os
import sqlite3
from io import BytesIO

import tensorflow as tf
from flask import Flask, send_file, send_from_directory, request, jsonify, g
from flask_cors import CORS, cross_origin

from datasets_map import datasets_map, check_if_dataset_class_exists
from db_models import Dataset, Model, Scheme
from exceptions import InvalidUsage
from keras_model_creator import KerasModelBuilder

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model_no = 100


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect("db.sqlite")
    return g.sqlite_db

@cross_origin()
@app.route('/scheme', methods=['POST'])
def put_scheme():
    data = request.get_json()
    new_scheme=Scheme()
    new_scheme.scheme_json = json.dumps(data)
    new_scheme.save()
    return new_scheme.toJSON()

@cross_origin()
@app.route('/scheme/<int:scheme_no>', methods=['GET'])
def get_scheme_info(scheme_no):
    scheme = Scheme.select().where(Scheme.id==scheme_no).get()
    if scheme is None:
        raise InvalidUsage("Scheme not found")
    return scheme.toJSON()

@cross_origin()
@app.route('/scheme', methods=['GET'])
def get_schemes():
    schemes = Scheme.select()
    if len(schemes)==0:
        return "[]"
    return "["+",".join([scheme.toJSON() for scheme in schemes])+"]"

@cross_origin()
@app.route('/model', methods=['GET'])
def get_models():
    models = Model.select()
    for model in models:
        print(model.toJSON())
    return "["+",".join([model.toJSON() for model in models])+"]"


@cross_origin()
@app.route('/model', methods=['POST'])
def train_model():
    request_data = request.get_json()
    scheme_id = request_data["scheme_id"]
    del request_data["scheme_id"]
    model = Model()
    model.scheme = Scheme.select().where(Scheme.id==scheme_id).get()
    model.save()
    dataset = Dataset.select().where(Dataset.name==request_data["dataset"]).get()
    model.dir_path = "models/"+str(model.get_id())
    model.dataset = dataset
    model.save()
    data=json.loads(model.scheme.scheme_json)
    if "dataset" not in request_data.keys():
        raise InvalidUsage("no dataset specified in request")
    check_if_dataset_class_exists(request_data['dataset'])
    dataset_class = datasets_map[request_data["dataset"]]
    del request_data['dataset']
    builder = KerasModelBuilder(dataset=dataset_class(), model_id=scheme_id, **request_data)
    data['layers'][0]['args']['input_shape'] = [dataset.img_width,dataset.img_height,dataset.img_depth]
    data['layers'][-1]['args']['units'] = len(json.loads(dataset.labels))
    print(data['layers'])
    for layer in data['layers']:
        builder.add_layer(layer)
    builder.build(model.dir_path)
    return model.toJSON()

@cross_origin()
@app.route('/model/<int:model_no>', methods=['GET'])
def get_model_info(model_no):
    model = Model.select().where(Model.id==model_no).get()
    if model is None:
        raise InvalidUsage("no dataset specified in request found in database")
    return model.toJSON()

@cross_origin()
@app.route('/model/<int:model_no>/file/<filename>', methods=['GET'])
def get_trained_model(model_no, filename):
    dir_path = Model.select().where(Model.id==model_no).get().dir_path
    return send_from_directory(dir_path, filename)



@cross_origin()
@app.route('/data')
def get_datasets():
    return json.dumps(list(datasets_map.keys()))

@app.route('/data/<dataset_id>/bitmaps/<int:image_no>')
def get_bitmap(dataset_id, image_no):
    dataset_id = Dataset.select().where(Dataset.id == dataset_id).get()
    dataset_class = check_if_dataset_class_exists(dataset_id.name) #TODO: change a way of getting dataset classes
    image = dataset_class.get_bitmap(image_no)
    byte_io = BytesIO()
    image.save(byte_io, 'bmp')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/bmp')

@app.route('/data/<int:dataset_id>/')
def get_dataset_info(dataset_id):
    dataset = Dataset.select().where(Dataset.id==dataset_id).get()
    if dataset is not None:
        return dataset.toJSON()
    raise InvalidUsage("no dataset specified in request found in database")


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()
