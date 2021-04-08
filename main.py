"""Main module of the API
"""
import os
import io
import random
import time
import uuid
from datetime import datetime

from requests import post
from celery import Celery
from api.config import celeryconfig
from datauri import DataURI
from datauri.exceptions import (
    InvalidDataURI,
    InvalidCharset,
    InvalidMimeType
    )
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
    SocketIO,
    emit,
    disconnect,
    join_room,
    leave_room
)
from flask_cors import CORS

import tensorflow as tf
from api.core import models

LOCAL_STORAGE = './data'

RPS_OPTIONS = {
    '0': 'rock',
    '1': 'paper',
    '2': 'scissor'
}

# Create folders to store images if not existing
try:
    for v in RPS_OPTIONS.values():
        os.makedirs(LOCAL_STORAGE + '/' + v, exist_ok=True)
except FileExistsError:
    pass

app = Flask(__name__)
app.clients = {}
CORS(app)
app.config['SECRET_KEY'] = 'top-secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Celery
celery = Celery(app.name)
celery.config_from_object(celeryconfig)
celery.conf.update(app.config)


@celery.task()
def training_task(room, url):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting', 'Running', 'Updating', 'Loading', 'Checking']
    adjective = ['latest', 'optimized', 'lightweight', 'efficient', 'core']
    noun = ['neural network', 'backpropagation', 'gradient descent', 'regularization', 'weights']
    message = ''
    total = random.randint(10, 50)

    for i in range(total):
        if not message or random.random() < 0.25:
            message = "{0} {1} {2} ...".format(random.choice(verb),
                                               random.choice(adjective),
                                               random.choice(noun))

        meta = {'current': i,
                'total': total,
                'status': message,
                'room': room
                }

        post(url, json=meta)
        time.sleep(0.5)

    meta = {'current': 100,
            'total': 100,
            'status': 'Done.',
            'room': room,
            'time': datetime.now().strftime('%H:%M:%S'),
            }
    post(url, json=meta)
    return meta


@app.route('/clients', methods=['GET'])
def clients():
    """Clients route: list all clients keys
    """
    return make_response(jsonify({'clients': list(app.clients.keys())}))


@app.route('/job', methods=['POST'])
def longtask():
    """This task will respond with the current time, and will trigget a celery task
    """
    userid = request.json['user_id']
    room = f'uid-{userid}'
    training_task.delay(room, url_for('status', _external=True, _method='POST'))
    return make_response(
        jsonify(
            {'status': f"Started at {datetime.now().strftime('%H:%M:%S')}"}
            )
        )


@celery.task()
def predict_task(room, url, _image):
    """Get probabilities of each class, given an input image

    Args:
        room (str): room of the current user
        url (str): URL where the status of this task will be posted
        image (PIL.JpegImagePlugin.JpegImageFile): image to be classified

    Returns:
        dict: serializable object passed as response
    """

    uri = DataURI(_image)
    image = Image.open(io.BytesIO(uri))

    # Get embedding from DL model
    x = tf.keras.preprocessing.image.img_to_array(image)
    x = tf.image.resize(x, [160, 160])
    x = models.three_classes_classifier.predict(x[tf.newaxis, ...])

    meta = {'current': 100,
            'total': 100,
            'status': 'Done.',
            'room': room,
            'time': datetime.now().strftime('%H:%M:%S'),
            }
    post(url, json=meta)

    return meta


def check_image_format(data_uri, screenshot_format, selected):
    """Extract data from URI and check format and type of data received

    Args:
        data_uri (str): image in data URI format
        screenshot_format (str): data type and format

    Returns:
        (bool, list of str): is data valid?, cause(s)
    """

    # Extract data from URI
    try:
        uri = DataURI(data_uri)
    except (InvalidDataURI, InvalidCharset, InvalidMimeType) as e:
        app.logger.error(e)

    # Check format and type of data received
    tx_data_type, tx_data_format = screenshot_format.split('/')
    rx_data_type, rx_data_format = uri.mimetype.split('/')

    causes = []
    valid = True

    if tx_data_type != rx_data_type:
        valid = False
        causes.append(f"File type mismatch. Expected {tx_data_type}, got {rx_data_type}.")

    if tx_data_format != rx_data_format:
        valid = False
        causes.append(f"File format mismatch. Expected {tx_data_format}, got {rx_data_format}.")

    if rx_data_type != 'image':
        valid = False
        causes.append(f"Unexpected '{uri.mimetype}' received.")

    if selected not in RPS_OPTIONS:
        valid = False
        causes.append(f"Unexpected '{selected}' option.")

    if valid:
        app.logger.debug('Valid image received, saving ...')
        image = Image.open(io.BytesIO(uri.data))
        save_path = f"{LOCAL_STORAGE}/{RPS_OPTIONS[selected]}"
        image.save(f"{save_path}/capture_{datetime.now().strftime('%H-%M-%S')}.{rx_data_format}")
        causes.append(f"'{uri.mimetype}' received. Ok.")

    return (valid, causes)


@app.route('/capture', methods=['POST'])
def capture():
    """This route is triggered every time a picture was taken in the browser
    """
    # userid = request.json['user_id']
    # room = f'uid-{userid}'
    room = 'room'
    data_uri = request.json['data_uri']
    screenshot_format = request.json['screenshot_format']
    selected = request.json['selected']

    is_valid, causes = check_image_format(data_uri, screenshot_format, selected)

    if is_valid:
        predict_task.delay(room, url_for('status', _external=True, _method='POST'), data_uri)

    return make_response(
        jsonify({
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
