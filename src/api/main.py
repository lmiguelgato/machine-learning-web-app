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
from datauri import DataURI
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
from flask.logging import create_logger
from flask_socketio import (
    SocketIO,
    emit,
    disconnect,
    join_room,
    leave_room
)
from flask_cors import CORS

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

# Redis
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

logger = create_logger(app)


@celery.task()
def long_task(room, url):
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
    long_task.delay(room, url_for('status', _external=True, _method='POST'))
    return make_response(
        jsonify(
            {'status': f"Started at {datetime.now().strftime('%H:%M:%S')}"}
            )
        )


@app.route('/capture', methods=['POST'])
def capture():
    """This route is triggered every time a picture was taken in the browser
    """
    data_uri = request.json['data_uri']
    uri = DataURI(data_uri)

    screenshot_format = request.json['screenshot_format']
    tx_data_type, tx_data_format = screenshot_format.split('/')
    rx_data_type, rx_data_format = uri.mimetype.split('/')

    assert tx_data_type == rx_data_type, \
        f"File type mismatch. Expected {tx_data_type}, got {rx_data_type}."
    assert tx_data_format == rx_data_format, \
        f"File format mismatch. Expected {tx_data_format}, got {rx_data_format}."

    selected = request.json['selected']

    if selected not in RPS_OPTIONS:
        ack = f"Unexpected '{selected}' option."
    elif rx_data_type == 'image':
        image = Image.open(io.BytesIO(uri.data))
        save_path = f"{LOCAL_STORAGE}/{RPS_OPTIONS[selected]}"
        image.save(f"{save_path}/capture_{datetime.now().strftime('%H-%M-%S')}.{rx_data_format}")
        ack = f"'{uri.mimetype}' received. Ok."
    else:
        ack = f"Unexpected '{uri.mimetype}' received."

    return make_response(
        jsonify({
            'ack': ack,
            'selected': selected
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
    logger.info('Client connected! Assigned user id %s.', userid)
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
    logger.info('Client %s disconnected.', session['userid'])


if __name__ == '__main__':
    socketio.run(app, debug=True)
