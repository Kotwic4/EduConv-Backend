import json
import os
import sqlite3

from flask import Flask, send_file, send_from_directory, request, jsonify, g
import tensorflow as tf
from flask_cors import CORS, cross_origin
from io import BytesIO

from datasets_map import datasets_map, get_dataset_class
from db_helper import get_dataset, get_model
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
@app.route('/model', methods=['POST'])
def put_model():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    dataset_id = cursor.execute("select id from datasets where name=?",(data["dataset"],)).fetchall()[0][0]
    cursor.execute("INSERT INTO models(dataset_id) values (?)",(dataset_id,))
    model_id = cursor.lastrowid
    dir_path = str.format("models/{}", model_id)
    cursor.execute("UPDATE models set dir_path=? where id=?",(dir_path,model_id))
    db.commit()
    os.makedirs(dir_path, exist_ok=True)
    with open(str.format('{}/input.json',dir_path), 'w+')as f:
        json.dump(data, f)
    return str(model_id)


@cross_origin()
@app.route('/model/<model_no>/train', methods=['POST'])
def train_model(model_no):
    request_data = request.get_json()
    dir_path = get_db().cursor().execute("select dir_path from models where id=?",(model_no,)).fetchall()[0][0]
    with open(str.format('{}/input.json', dir_path), 'r+')as f:
        data = json.load(f)
    if "dataset" not in data.keys():
        raise InvalidUsage("no dataset specified in request")
    get_dataset_class(data['dataset'])
    dataset_class = datasets_map[data["dataset"]]
    builder = KerasModelBuilder(dataset=dataset_class(),model_id=model_no, **request_data)
    for layer in data['layers']:
        builder.add_layer(layer)
    builder.build(dir_path)

    return "{}"

@cross_origin()
@app.route('/model/info/<int:model_no>', methods=['GET'])
def get_model_info(model_no):
    model = get_model(model_no)
    if model is None:
        raise InvalidUsage("no dataset specified in request found in database")
    return str(model)

@cross_origin()
@app.route('/model/<int:model_no>/<filename>', methods=['GET'])
def get_trained_model(model_no, filename):
    dir_path = get_db().cursor().execute("select dir_path from models where id=?", (model_no,)).fetchall()[0][0]
    return send_from_directory(dir_path, filename)


@cross_origin()
@app.route('/data/<filename>')
def hello_world(filename):
    return send_from_directory('./saved_model', filename)


@cross_origin()
@app.route('/data')
def get_datasets():
    return json.dumps(list(datasets_map.keys()))


@app.route('/data/<dataset>/<int:image_id>')
def get_image_json(dataset, image_id):
    if dataset == 'mnist':
        mnist = tf.contrib.learn.datasets.load_dataset("mnist")
        label = str(mnist.test.labels[image_id])
        image_str = '[' + ",".join(str(elem) for elem in mnist.test.images[image_id]) + ']'
        return str({"image": image_str, "label": label})
    return "There is no such dataset in the database"

@app.route('/data/<string:datasetname>/info')
def get_dataset_info(datasetname):
    dataset = get_dataset(datasetname)
    if dataset is not None:
        return str(dataset)
    raise InvalidUsage("no dataset specified in request found in database")


@app.route('/data/<dataset>/bitmaps/<int:image_no>')
def get_bitmap(dataset, image_no):
    dataset_class = get_dataset_class(dataset)
    image = dataset_class.get_bitmap(image_no)
    byte_io = BytesIO()
    image.save(byte_io, 'bmp')
    byte_io.seek(0)
    return send_file(byte_io, mimetype='image/bmp')


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
