"""Main module of the API
"""
import io
import uuid
from datetime import datetime
from requests import post

from os import listdir
from os.path import isfile, join

from datauri import DataURI
from datauri.exceptions import (
    InvalidDataURI,
    InvalidCharset,
    InvalidMimeType
    )

import numpy as np

import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory

import PIL.Image as Image

from flask import (
    Flask,
    make_response,
    request,
    session,
    url_for,
    jsonify,
    current_app
    )
from flask_socketio import (
    emit,
    disconnect,
    join_room,
    leave_room
)
from flask_cors import CORS

from flask_socketio import SocketIO

from api.core import models
from api.config import celeryconfig, tfconfig
from api.constant import (
    LOCAL_STORAGE,
    RPS_OPTIONS,
    IMG_FORMATS,
    MODEL_STORAGE
)

from celery import Celery
from celery.utils.log import get_task_logger


app = Flask(__name__)
app.clients = {}
CORS(app)
app.config['SECRET_KEY'] = 'top-secret!'

socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Celery
celery = Celery(app.name)
celery.config_from_object(celeryconfig)
celery.conf.update(app.config)


def create_dataset(from_path):
    """Create a dataset from a directory with images."""
    train_dataset = image_dataset_from_directory(
        from_path,
        validation_split=0.2,
        subset="training",
        seed=tfconfig.RANDOM_SEED,
        batch_size=tfconfig.BATCH_SIZE,
        image_size=tfconfig.IMG_SIZE
        )

    validation_dataset = image_dataset_from_directory(
        from_path,
        validation_split=0.2,
        subset="validation",
        seed=tfconfig.RANDOM_SEED,
        batch_size=tfconfig.BATCH_SIZE,
        image_size=tfconfig.IMG_SIZE
        )

    train_dataset = train_dataset.cache().shuffle(10, tfconfig.RANDOM_SEED)
    train_dataset = train_dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    validation_dataset = validation_dataset.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    return train_dataset, validation_dataset


@celery.task()
def train_task(room, url):
    """Background task that runs a long function with progress reports."""

    celery_logger = get_task_logger(__name__)

    celery_logger.info("Creating dataset ...")

    meta = {
            'current': 0,
            'total': tfconfig.EPOCHS,
            'status': 'Creating dataset ...',
            'room': room,
            'time': datetime.now().strftime('%H:%M:%S')
            }
    post(url, json=meta)

    train_dataset, validation_dataset = create_dataset(LOCAL_STORAGE)
    celery_logger.info("Done.")

    celery_logger.info("Start training ...")
    try:
        history = models.three_classes_classifier.fit(
            train_dataset,
            validation_data=validation_dataset,
            epochs=tfconfig.EPOCHS,
            callbacks=[models.CustomCallback(url, room, celery_logger)]
            )
    except Exception as e:
        celery_logger.error(e)
    else:
        celery_logger.info("Done ...")
    

        celery_logger.info("Saving the model ...")
        try:
            models.three_classes_classifier.save(f'{MODEL_STORAGE}/rps_model.h5')
        except Exception as e:
            celery_logger.error(e)
        else:
            celery_logger.info("Done ...")

        # TODO use acc and loss to make a plot
        acc = history.history['sparse_categorical_accuracy']
        loss = history.history['loss']

        print(acc, loss)


@app.route('/clients', methods=['GET'])
def clients():
    """Clients route: list all clients keys
    """
    return make_response(jsonify({'clients': list(app.clients.keys())}))


@app.route('/storage', methods=['POST'])
def storage():
    """Get information regarding the local storage
    """

    # Find all images in local storage, and group them by label
    STORAGE_TRACKER = dict()
    for index, label in RPS_OPTIONS.items():
        onlyfiles = [
            f for f in listdir(f"{LOCAL_STORAGE}/{label}/")
            if isfile(join(f"{LOCAL_STORAGE}/{label}/", f)) and f[-4:] in IMG_FORMATS
            ]
        STORAGE_TRACKER[index] = onlyfiles

    return make_response(jsonify(
        {
            'storage': STORAGE_TRACKER
        })
        )


@app.route('/train', methods=['POST'])
def train():
    """This task will respond with the current time, and will trigget a celery task
    """
    userid = request.json['user_id']
    room = f'uid-{userid}'

    train_task.delay(room, url_for('status', _external=True, _method='POST'))

    return make_response(
        jsonify(
            {
                'status': f"Started at {datetime.now().strftime('%H:%M:%S')}"
            }
            )
        )


@celery.task()
def predict_task(room, url, data_uri):    # TODO: implement this
    """Get probabilities of each class, given an input image

    Args:
        room (str): room of the current user
        url (str): URL where the status of this task will be posted
        data_uri (str): image to be classified in data URI format

    Returns:
        dict: serializable object passed as response
    """

    uri = DataURI(data_uri)
    image = Image.open(io.BytesIO(uri.data))

    # Get probabilities for each class
    tensor_image = tf.keras.preprocessing.image.img_to_array(image)
    tensor_image_resized = tf.image.resize(tensor_image, [160, 160])
    class_probabilities = models.three_classes_classifier.predict(
        tensor_image_resized[tf.newaxis, ...]
        )

    meta = {'current': 100,
            'total': 100,
            'status': 'Done.',
            'room': room,
            'class_probabilities': class_probabilities,
            'time': datetime.now().strftime('%H:%M:%S'),
            }
    post(url, json=meta)

    return meta


@app.route('/predict', methods=['POST'])
def predict():
    """This task will respond with the infered label
    """
    data_uri = request.json['data_uri']

    uri = DataURI(data_uri)
    image = Image.open(io.BytesIO(uri.data))

    # Get probabilities for each class
    tensor_image = tf.keras.preprocessing.image.img_to_array(image)
    tensor_image_resized = tf.image.resize(tensor_image, [160, 160])
    class_probabilities = models.three_classes_classifier.predict(
        tensor_image_resized[tf.newaxis, ...]
        )

    return make_response(jsonify({
        'probability': str(round(np.max(class_probabilities), 2)),
        'label': str(class_probabilities.argmax())
    }))


def check_image_format(uri, screenshot_format, selected):
    """Extract data from URI and check format and type of data received

    Args:
        data_uri (str): image in data URI format
        screenshot_format (str): data type and format
        selected: index of the options selected on the UI

    Returns:
        (bool, list of str): is data valid?, cause(s)
    """

    # Check format and type of data received
    tx_data_type, tx_data_format = screenshot_format.split('/')
    rx_data_type, rx_data_format = uri.mimetype.split('/')

    causes = []
    is_valid = True

    if tx_data_type != rx_data_type:
        is_valid = False
        causes.append(f"File type mismatch. Expected {tx_data_type}, got {rx_data_type}.")

    if tx_data_format != rx_data_format:
        is_valid = False
        causes.append(f"File format mismatch. Expected {tx_data_format}, got {rx_data_format}.")

    if rx_data_type != 'image':
        is_valid = False
        causes.append(f"Unexpected '{uri.mimetype}' received.")

    if selected not in RPS_OPTIONS:
        is_valid = False
        causes.append(f"Unexpected '{selected}' option.")

    return (is_valid, causes)


def save_capture(uri, selected):
    """Saves an image in data URI format, into the folder corresponding to the selected option

    Args:
        uri (data URI): image in data URI format
        selected (str): option selected

    Returns:
        bool, str: able to save image?, path to image
    """

    save_path = f"{LOCAL_STORAGE}/{RPS_OPTIONS[selected]}/"
    save_path += f"capture_{datetime.now().strftime('%Y-%m-%d_%H:%M:%S:%f')}"
    save_path += f".{uri.mimetype.split('/')[1]}"

    try:
        image = Image.open(io.BytesIO(uri.data))
        image.save(save_path)
    except Exception as e:
        app.logger.error(e)
        return False, save_path

    return True, save_path


@app.route('/capture', methods=['POST'])
def capture():
    """This route is triggered every time a picture was taken in the browser
    """
    data_uri = request.json['data_uri']
    screenshot_format = request.json['screenshot_format']
    selected = request.json['selected']

    # Extract data from URI
    try:
        uri = DataURI(data_uri)
    except (InvalidDataURI, InvalidCharset, InvalidMimeType) as e:
        app.logger.error(e)

    is_valid, causes = check_image_format(uri, screenshot_format, selected)

    if is_valid:
        causes.append(f"Ok, '{uri.mimetype}' received.")
        app.logger.debug('Valid image received, saving ...')
        did_save, img_path = save_capture(uri, selected)
        if did_save:
            app.logger.debug("Successfully saved '%s' in '%s'", RPS_OPTIONS[selected], img_path)
        else:
            app.logger.debug("Unable to save '%s' in '%s'", RPS_OPTIONS[selected], img_path)

    return make_response(
        jsonify({
            'valid_capture': is_valid,
            'ack': causes
            })
        )


@app.route('/status', methods=['POST'])
def status():
    """Route to check the status of a task through web sockets
    """
    room = request.json['room']
    emit('status', request.json, room=room, namespace='/')

    return jsonify({})


@socketio.on('connect')
def events_connect():
    """Route to notify a new user has connected, and assign an ID
    """
    userid = str(uuid.uuid4())
    session['userid'] = userid
    current_app.clients[userid] = request.namespace
    app.logger.info('Client connected! Assigned user id %s.', userid)
    room = f'uid-{userid}'
    join_room(room)
    emit('connected', {'user_id': userid})


@socketio.on('disconnect request')
def disconnect_request():
    """Route to notify that certain user has requested to disconnect
    """
    emit('status', {'status': 'Disconnected!'})
    disconnect()


@socketio.on('disconnect')
def events_disconnect():
    """Route to notify that certain user has been disconnected
    """
    del current_app.clients[session['userid']]
    room = f"uid-{session['userid']}"
    leave_room(room)
    app.logger.info('Client %s disconnected.', session['userid'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
