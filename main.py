import json
import os
from flask import Flask, send_file, send_from_directory, request, jsonify
import tensorflow as tf
from flask_cors import CORS, cross_origin
from io import BytesIO

from datasets_map import datasets_map, get_dataset_class
from exceptions import InvalidUsage
from keras_model_creator import KerasModelBuilder

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model_no = 100


@cross_origin()
@app.route('/model', methods=['POST'])
def put_model():
    global model_no
    model_no += 1
    data = request.get_json()
    # builder = KerasModelBuilder()
    # for layer in data['layers']:
    #     builder.add_layer(layer)
    os.makedirs(str.format("./{}", model_no), exist_ok=True)
    print(os.path.dirname("."))
    with open(str.format('./{}/input.json', model_no), 'w+')as f:
        json.dump(data, f)
    return str(model_no)


@cross_origin()
@app.route('/model/<model_no>/train', methods=['POST'])
def train_model(model_no):
    with open(str.format('./{}/input.json', model_no), 'r+')as f:
        data = json.load(f)
    if "dataset" not in data.keys():
        raise InvalidUsage("no dataset specified in request")
    get_dataset_class(data['dataset'])
    dataset_class = datasets_map[data["dataset"]]
    builder = KerasModelBuilder(dataset=dataset_class())
    for layer in data['layers']:
        builder.add_layer(layer)
    builder.build("./" + model_no)

    return "lorem ipsum"


@cross_origin()
@app.route('/model/<model_no>/<filename>', methods=['GET'])
def get_model(model_no, filename):
    return send_from_directory('./' + model_no, filename)


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
