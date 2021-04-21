"""Machine learning models and routines."""
from datetime import datetime

from numpy import ndarray

from PIL.JpegImagePlugin import JpegImageFile

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D

from requests import post

from ..config import tfconfig


""" --- MobileNet model ---
    Reference (https://arxiv.org/abs/1704.04861):
    MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications"""


class RockPaperScissor():

    """Class to create a model to classify Rock/Paper/Scissor images."""
    def __init__(self, input_shape: tuple = (160, 160)) -> None:
        """Constructor for the RockPaperScissor class.

        Args:
            input_shape (tuple, optional): Image size. Defaults to (160, 160).
        """
        self.input_shape = input_shape

        preprocessing_layer = tf.keras.applications.mobilenet.preprocess_input

        # MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications
        # https://arxiv.org/abs/1704.04861
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

    def description(self) -> None:
        """Print summary of the model."""
        self.model.summary()


class CustomCallback(keras.callbacks.Callback):

    """Define a simple custom callback that logs steps in training and prediction."""
    def __init__(self, url, room, logger=None):
        """Constructor for custom callback.

        Args:
            url (str): URL where callback messages will be posted.
            room (str): Room identifier for websocket.
            logger (Logger, optional): Logger object from 'logging'package, or from a derived
            class. Defaults to None.
        """
        super().__init__()
        self.logger = logger
        self.url = url
        self.room = room

    def on_train_begin(self, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"Starting training; got log keys: {keys}")

        meta = {
                'current': 0,
                'total': tfconfig.EPOCHS,
                'status': 'Starting training ...',
                'room': self.room,
                'time': datetime.now().strftime('%H:%M:%S')
                }
        post(self.url, json=meta)

    def on_train_end(self, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"Stop training; got log keys: {keys}")

    def on_epoch_begin(self, epoch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"Start epoch {epoch} of training; got log keys: {keys}")

    def on_epoch_end(self, epoch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"End epoch {epoch} of training; got log keys: {keys}")

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

    def on_test_begin(self, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"Start testing; got log keys: {keys}")

    def on_test_end(self, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"Stop testing; got log keys: {keys}")

    def on_predict_begin(self, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"Start predicting; got log keys: {keys}")

    def on_predict_end(self, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"Stop predicting; got log keys: {keys}")

    def on_train_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"...Training: start of batch {batch}; got log keys: {keys}")

    def on_train_batch_end(self, batch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"...Training: end of batch {batch}; got log keys: {keys}")

    def on_test_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"...Evaluating: start of batch {batch}; got log keys: {keys}")

    def on_test_batch_end(self, batch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"...Evaluating: end of batch {batch}; got log keys: {keys}")

    def on_predict_batch_begin(self, batch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"...Predicting: start of batch {batch}; got log keys: {keys}")

    def on_predict_batch_end(self, batch, logs=None):
        keys = list(logs.keys())

        if self.logger:
            self.logger.info(f"...Predicting: end of batch {batch}; got log keys: {keys}")
