import os
import ntpath
from tempfile import NamedTemporaryFile

from flask import Flask, send_file, send_from_directory
import tensorflow as tf

from image_util import generate_8bit_bitmap

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

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
        image = generate_8bit_bitmap(28,28,mnist.test.images[image_id])
        fileObj = NamedTemporaryFile(dir='./',suffix='bmp')
        image.save(fileObj,'bmp')
        return send_from_directory(os.path.dirname(fileObj.name),ntpath.basename(fileObj.name),mimetype="image/bmp")
    return "There is no such dataset in the database"
