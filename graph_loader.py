import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

from fully_connected_feed import fill_feed_dict, placeholder_inputs

class TMP:
    batch_size = 100
def main(_):
    export_dir = '/home/albert/inz/EduConv-Backend/saved_model/'
    with tf.Session(graph=tf.Graph()) as sess:
        tf.saved_model.loader.load(sess, ["train"], export_dir)
        data_sets = input_data.read_data_sets('/home/albert/inz/EduConv-Backend/mnist/input_data', False)
        images_placeholder, labels_placeholder = placeholder_inputs(100)
        feed_dict = fill_feed_dict(data_sets.train,
                                   images_placeholder,
                                   labels_placeholder)
        print("feed_dict",feed_dict)
        print(sess.run(sess.graph.get_operation_by_name("loss"), feed_dict=feed_dict))


tf.app.run(main=main)
