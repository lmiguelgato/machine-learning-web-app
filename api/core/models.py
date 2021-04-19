"""Machine learning models and routines
"""
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D

from datetime import datetime
from requests import post

from ..config import tfconfig


""" --- MobileNet model ---
    Reference:
    MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications
    https://arxiv.org/abs/1704.04861
"""

# Each Keras Application expects a specific kind of input preprocessing:
preprocess_input = tf.keras.applications.mobilenet.preprocess_input


rescale = tf.keras.layers.experimental.preprocessing.Rescaling(1./127.5, offset=-1)
data_augmentation = tf.keras.Sequential([
  tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal'),
  tf.keras.layers.experimental.preprocessing.RandomRotation(0.2),
])

mobile_net = tf.keras.applications.MobileNet(
    input_shape=tfconfig.IMG_SIZE + (3,),
    include_top=False,  # whether to include the fully-connected layer at the top of the network
    alpha=1.0,  # a.k.a. width multiplier, it controls the width of the network
    depth_multiplier=1  # a.k.a. resolution multiplier, it controls the depth of the network
    )
mobile_net.trainable = False

# TODO: define a class instead
inputs = tf.keras.Input(shape=tfconfig.IMG_SIZE + (3,))
x = data_augmentation(inputs)
x = preprocess_input(x)
x = mobile_net(x, training=False)
x = GlobalAveragePooling2D()(x)
x = Dropout(0.2)(x)
outputs = Dense(3, activation='softmax')(x)

three_classes_classifier = tf.keras.Model(inputs, outputs)

# Compile the model
three_classes_classifier.compile(
    optimizer=tf.keras.optimizers.Adam(lr=tfconfig.LEARNING_RATE),
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=[tf.keras.metrics.SparseCategoricalAccuracy()]
    )


class CustomCallback(keras.callbacks.Callback):
    """Define a simple custom callback that logs steps in training and prediction
    """
    def __init__(self, url, room, logger=None):
        self.logger = logger
        self.url = url
        self.room = room

    def on_train_begin(self, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info("Starting training; got log keys: {}".format(keys))

        meta = {
                'current': 0,
                'total': tfconfig.EPOCHS,
                'status': 'Starting training ...',
                'room': self.room,
                'time': datetime.now().strftime('%H:%M:%S')
                }
        post(self.url, json=meta)

        print("Starting training; got log keys: {}".format(keys))

    def on_train_end(self, logs=None):
        keys = list(logs.keys())
        print("Stop training; got log keys: {}".format(keys))

    def on_epoch_begin(self, epoch, logs=None):
        keys = list(logs.keys())
        print("Start epoch {} of training; got log keys: {}".format(epoch, keys))

    def on_epoch_end(self, epoch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info("Start epoch {} of training; got log keys: {}".format(epoch, keys))

        msg = f"Epoch {epoch+1}/{tfconfig.EPOCHS} - "
        msg += f"Loss: {logs['loss']:.2}"
        msg += f", Accuracy: {logs['sparse_categorical_accuracy']:.2}"
        msg += f" - Val. loss: {logs['val_loss']:.2}"
        msg += f", Val. accuracy: {logs['val_sparse_categorical_accuracy']:.2}"

        meta = {
                'current': epoch+1,
                'total': tfconfig.EPOCHS,
                'status': msg,
                'room': self.room,
                'time': datetime.now().strftime('%H:%M:%S')
                }
        post(self.url, json=meta)

        print("End epoch {} of training; got log keys: {}".format(epoch, keys))

    def on_test_begin(self, logs=None):
        keys = list(logs.keys())
        print("Start testing; got log keys: {}".format(keys))

    def on_test_end(self, logs=None):
        keys = list(logs.keys())
        print("Stop testing; got log keys: {}".format(keys))

    def on_predict_begin(self, logs=None):
        keys = list(logs.keys())
        print("Start predicting; got log keys: {}".format(keys))

    def on_predict_end(self, logs=None):
        keys = list(logs.keys())
        print("Stop predicting; got log keys: {}".format(keys))

    def on_train_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())
        print("...Training: start of batch {}; got log keys: {}".format(batch, keys))

    def on_train_batch_end(self, batch, logs=None):
        keys = list(logs.keys())
        print("...Training: end of batch {}; got log keys: {}".format(batch, keys))

    def on_test_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())
        print("...Evaluating: start of batch {}; got log keys: {}".format(batch, keys))

    def on_test_batch_end(self, batch, logs=None):
        keys = list(logs.keys())
        print("...Evaluating: end of batch {}; got log keys: {}".format(batch, keys))

    def on_predict_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())
        print("...Predicting: start of batch {}; got log keys: {}".format(batch, keys))

    def on_predict_batch_end(self, batch, logs=None):
        keys = list(logs.keys())
        print("...Predicting: end of batch {}; got log keys: {}".format(batch, keys))
