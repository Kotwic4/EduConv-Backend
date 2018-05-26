import json
import os
import ntpath
from tempfile import NamedTemporaryFile
from flask import Flask, send_file, send_from_directory, request
import tensorflow as tf
from flask_cors import CORS, cross_origin
from image_util import generate_8bit_gray_bitmap
from keras_model_creator import KerasModelBuilder

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
model_no=100
@cross_origin()
@app.route('/model',methods=['POST'])
def put_model():
    global model_no
    model_no+=1
    data = request.get_json()
    builder = KerasModelBuilder()
    for layer in data['layers']:
        builder.add_layer(layer)
    os.makedirs(str.format("./{}",model_no),exist_ok=True)
    print(os.path.dirname("."))
    with open(str.format('./{}/input.json',model_no),'w+')as f:
        json.dump(data,f)
    return str(model_no)

@cross_origin()
@app.route('/model/<model_no>/train',methods=['POST'])
def train_model(model_no):

    with open(str.format('./{}/input.json', model_no), 'r+')as f:
        data = json.load(f)
    builder = KerasModelBuilder()
    for layer in data['layers']:
        builder.add_layer(layer)
    builder.build("./"+model_no)

    return "lorem ipsum"

@cross_origin()
@app.route('/model/<model_no>/<filename>',methods=['GET'])
def get_model(model_no,filename):
    return send_from_directory('./'+model_no, filename)


@cross_origin()
@app.route('/data/<filename>')
def hello_world(filename):
    return send_from_directory('./saved_model',filename)

@app.route('/data/<dataset>/<int:image_id>')
def get_image_json(dataset, image_id):
    if dataset=='mnist':
        mnist = tf.contrib.learn.datasets.load_dataset("mnist")
        label = str(mnist.test.labels[image_id])
        image_str = '['+",".join(str(elem) for elem in mnist.test.images[image_id])+']'
        return str({"image":image_str,"label":label})
    return "There is no such dataset in the database"

@app.route('/data/<dataset>/bitmaps/<int:image_id>')
def get_bitmap(dataset,image_id):
    if dataset=='mnist':
        mnist = tf.contrib.learn.datasets.load_dataset("mnist")
        image = generate_8bit_gray_bitmap(28, 28, mnist.test.images[image_id])
        fileObj = NamedTemporaryFile(dir='./',suffix='bmp')
        image.save(fileObj,'bmp')
        return send_from_directory(os.path.dirname(fileObj.name),ntpath.basename(fileObj.name),mimetype="image/bmp")
    return "There is no such dataset in the database"

