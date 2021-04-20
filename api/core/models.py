"""Machine learning models and routines
"""
from datetime import datetime

from numpy import ndarray

from PIL.JpegImagePlugin import JpegImageFile

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

from requests import post

from ..config import tfconfig


""" --- MobileNet model ---
    Reference:
    MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications
    https://arxiv.org/abs/1704.04861
"""


class RockPaperScissor():
    def __init__(self, input_shape: tuple = (160, 160)) -> None:
        self.input_shape = input_shape

        preprocessing_layer = tf.keras.applications.mobilenet.preprocess_input

        base_model = tf.keras.applications.MobileNet(
            input_shape=self.input_shape + (3,),
            include_top=False,  # whether to include the fully-connected layer at the top of the DNN
            alpha=1.0,  # a.k.a. width multiplier, it controls the width of the network
            depth_multiplier=1  # a.k.a. resolution multiplier, it controls the depth of the network
            )
        base_model.trainable = False

        # Define the architecture through the TF functional API
        self.inputs = tf.keras.Input(shape=self.input_shape + (3,))
        x = preprocessing_layer(self.inputs)
        x = base_model(x, training=False)
        x = GlobalAveragePooling2D()(x)
        x = Dense(100, activation='relu')(x)
        self.outputs = Dense(3, activation='softmax')(x)

        self.model = tf.keras.Model(self.inputs, self.outputs)

        self.model.compile(
            optimizer=tf.keras.optimizers.Adam(lr=tfconfig.LEARNING_RATE),
            loss='categorical_crossentropy',
            metrics=['accuracy']
            )

    def __call__(self, image: JpegImageFile) -> ndarray:
        # Get probabilities for each class
        tensor_image = tf.keras.preprocessing.image.img_to_array(image)
        tensor_image_resized = tf.image.resize(tensor_image, self.input_shape)
        return self.model.predict(tensor_image_resized[tf.newaxis, ...])


class CustomCallback(keras.callbacks.Callback):
    """Define a simple custom callback that logs steps in training and prediction
    """
    def __init__(self, url, room, logger=None):
        super().__init__()
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
        msg += f", Accuracy: {logs['accuracy']:.2}"
        msg += f" - Val. loss: {logs['val_loss']:.2}"
        msg += f", Val. accuracy: {logs['val_accuracy']:.2}"

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
