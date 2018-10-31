from flask import Flask, request, jsonify, g
from flask_cors import CORS, cross_origin

from src.controllers.dataset_controller import DatasetController
from src.controllers.trained_model_controller import trained_ModelController
from src.controllers.model_controller import ModelController
from src.exceptions.invalid_usage import InvalidUsage

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@cross_origin()
@app.route('/model', methods=['POST'])
def put_model():
    body = request.get_json()
    return ModelController.put_model(body)


@cross_origin()
@app.route('/model/<int:model_no>', methods=['GET'])
def get_model_info(model_no):
    return ModelController.get_model_info(model_no)


@cross_origin()
@app.route('/model/<int:model_no>', methods=['DELETE'])
def delete_model(model_no):
    return ModelController.delete_model(model_no)


@cross_origin()
@app.route('/model', methods=['GET'])
def get_models():
    return ModelController.get_models()


@cross_origin()
@app.route('/trained_model', methods=['GET'])
def get_trained_models():
    return trained_ModelController.get_trained_models()


@cross_origin()
@app.route('/trained_model', methods=['POST'])
def train_trained_model():
    body = request.get_json()
    return trained_ModelController.train_trained_model(body), 200


@cross_origin()
@app.route('/trained_model/<int:trained_model_no>', methods=['GET'])
def get_trained_model_info(trained_model_no):
    return trained_ModelController.get_trained_model_info(trained_model_no)

@cross_origin()
@app.route('/trained_model/<int:trained_model_no>/file/<filename>', methods=['GET'])
def get_trained_trained_model(trained_model_no, filename):
    return trained_ModelController.get_trained_trained_model(trained_model_no, filename)


@cross_origin()
@app.route('/data')
def get_datasets():
    return DatasetController.get_datasets()


@app.route('/data/<dataset_id>/bitmaps/<int:image_no>')
def get_bitmap(dataset_id, image_no):
    dataset = request.args['imageset']
    is_train_dataset = dataset=="train" 
    return DatasetController.get_bitmap(dataset_id, image_no,is_train_dataset)


@app.route('/data/<dataset_id>/label/<int:image_no>')
def get_label(dataset_id, image_no):
    dataset = request.args['imageset']
    is_train_dataset = dataset=="train" 
    return DatasetController.get_label(dataset_id, image_no, is_train_dataset) 


@app.route('/data/<int:dataset_id>/')
def get_dataset_info(dataset_id):
    return DatasetController.get_dataset_info(dataset_id)


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
