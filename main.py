from flask import Flask, request, jsonify, g
from flask_cors import CORS, cross_origin

from src.controllers.dataset_controller import DatasetController
from src.controllers.model_controller import ModelController
from src.controllers.scheme_controller import SchemeController
from src.exceptions.invalid_usage import InvalidUsage

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@cross_origin()
@app.route('/scheme', methods=['POST'])
def put_scheme():
    body = request.get_json()
    return SchemeController.put_scheme(body)


@cross_origin()
@app.route('/scheme/<int:scheme_no>', methods=['GET'])
def get_scheme_info(scheme_no):
    return SchemeController.get_scheme_info(scheme_no)


@cross_origin()
@app.route('/scheme/<int:scheme_no>', methods=['DELETE'])
def delete_scheme(scheme_no):
    return SchemeController.delete_scheme(scheme_no)


@cross_origin()
@app.route('/scheme', methods=['GET'])
def get_schemes():
    return SchemeController.get_schemes()


@cross_origin()
@app.route('/model', methods=['GET'])
def get_models():
    return ModelController.get_models()


@cross_origin()
@app.route('/model', methods=['POST'])
def train_model():
    body = request.get_json()
    return ModelController.train_model(body)


@cross_origin()
@app.route('/model/<int:model_no>', methods=['GET'])
def get_model_info(model_no):
    return ModelController.get_model_info(model_no)


@cross_origin()
@app.route('/model/<int:model_no>', methods=['DELETE'])
def delete_model(model_no):
    return ModelController.delete_model(model_no)


@cross_origin()
@app.route('/model/<int:model_no>/file/<filename>', methods=['GET'])
def get_trained_model(model_no, filename):
    return ModelController.get_trained_model(model_no, filename)


@cross_origin()
@app.route('/data')
def get_datasets():
    return DatasetController.get_datasets()


@app.route('/data/<dataset_id>/bitmaps/<int:image_no>')
def get_bitmap(dataset_id, image_no):
    return DatasetController.get_bitmap(dataset_id, image_no)


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
