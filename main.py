"""Main module of the API."""
import io
import uuid
from datetime import datetime
from os import environ, listdir
from os.path import abspath, dirname, isfile, join

import numpy as np
import PIL.Image as Image
from celery import Celery
from celery.utils.log import get_task_logger
from datauri import DataURI
from datauri.exceptions import InvalidCharset, InvalidDataURI, InvalidMimeType
from dotenv import load_dotenv
from flask import Flask, current_app, jsonify, make_response, request, session, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, disconnect, emit, join_room, leave_room
from requests import post

from api.config import celeryconfig, tfconfig
from api.constant import IMG_FORMATS, LOCAL_STORAGE, MODEL_STORAGE, RPS_OPTIONS
from api.core import models, rock_paper_scissor
from api.core.datasets import create_dataset
from api.core.images import check_image_format, save_capture

basedir = abspath(dirname(dirname(__file__)))
load_dotenv(join(basedir, ".env"))

app = Flask(__name__)
app.clients = {}
CORS(app)
app.config["SECRET_KEY"] = environ.get("FLASK_SECRET_KEY")

DEBUG_MODE = environ.get("DEBUG") == "true"

socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Celery
celery = Celery(app.name)
celery.config_from_object(celeryconfig)
celery.conf.update(app.config)


@celery.task()
def train_task(room, url):
    """Background task that runs a long function with progress reports."""
    celery_logger = get_task_logger(__name__)

    celery_logger.info("Creating dataset ...")

    meta = {
        "current": 0,
        "total": tfconfig.EPOCHS,
        "status": "Creating dataset ...",
        "room": room,
        "time": datetime.now().strftime("%H:%M:%S"),
    }
    post(url, json=meta)

    train_dataset, validation_dataset = create_dataset(LOCAL_STORAGE)
    celery_logger.info("Done.")

    celery_logger.info("Start training ...")
    try:
        history = rock_paper_scissor.model.fit(
            train_dataset,
            validation_data=validation_dataset,
            epochs=tfconfig.EPOCHS,
            callbacks=[models.CustomCallback(url, room)],
        )

        # Fine tuning:
        rock_paper_scissor.base_model.trainable = True
        rock_paper_scissor.fine_tune_compile()
        fine_tune_history = rock_paper_scissor.model.fit(
            train_dataset,
            validation_data=validation_dataset,
            initial_epoch=history.epoch[-1],
            epochs=tfconfig.EPOCHS + tfconfig.FINE_TUNE_EPOCHS,
            callbacks=[models.CustomCallback(url, room)],
        )
    except Exception as e:
        celery_logger.error(e)
    else:
        celery_logger.info("Done ...")
        celery_logger.info("Saving the model ...")
        try:
            rock_paper_scissor.model.save(f"{MODEL_STORAGE}/rps_model.h5")
        except Exception as e:
            celery_logger.error(e)
        else:
            celery_logger.info("Done ...")

        # TODO use acc and loss to make a plot
        acc = history.history["accuracy"] + fine_tune_history.history["accuracy"]
        loss = history.history["loss"] + fine_tune_history.history["loss"]

        print(acc, loss)


@app.route("/clients", methods=["GET"])
def clients():
    """Clients route: list all clients keys."""
    return make_response(jsonify({"clients": list(app.clients.keys())}))


@app.route("/storage", methods=["POST"])
def storage():
    """Get information regarding the local storage."""
    # Find all images in local storage, and group them by label
    STORAGE_TRACKER = dict()
    for index, label in RPS_OPTIONS.items():
        onlyfiles = [
            f
            for f in listdir(f"{LOCAL_STORAGE}/{label}/")
            if isfile(join(f"{LOCAL_STORAGE}/{label}/", f)) and f[-4:] in IMG_FORMATS
        ]
        STORAGE_TRACKER[index] = onlyfiles

    return make_response(jsonify({"storage": STORAGE_TRACKER}))


@app.route("/train", methods=["POST"])
def train():
    """Respond with the current time, and will trigget a celery task."""
    userid = request.json["user_id"]
    room = f"uid-{userid}"

    train_task.delay(room, url_for("status", _external=True, _method="POST"))

    return make_response(
        jsonify({"status": f"Started at {datetime.now().strftime('%H:%M:%S')}"})
    )


@app.route("/predict", methods=["POST"])
def predict():
    """Respond with the inferred label."""
    data_uri = request.json["data_uri"]

    if data_uri:
        uri = DataURI(data_uri)
        image = Image.open(io.BytesIO(uri.data))

        # Get probabilities for each class
        class_probabilities = rock_paper_scissor(image)
        app.logger.debug(f"Inference, class probabilities: {class_probabilities}")

        return make_response(
            jsonify(
                {
                    "probability": str(round(np.max(class_probabilities), 2)),
                    "label": str(class_probabilities.argmax()),
                }
            )
        )
    else:
        return make_response(jsonify({}))


@app.route("/capture", methods=["POST"])
def capture():
    """Triggered every time a picture was taken in the browser."""
    data_uri = request.json["data_uri"]
    screenshot_format = request.json["screenshot_format"]
    selected = request.json["selected"]

    # Extract data from URI
    try:
        uri = DataURI(data_uri)
    except (InvalidDataURI, InvalidCharset, InvalidMimeType) as e:
        app.logger.error(e)

    is_valid, causes = check_image_format(uri, screenshot_format, selected)

    if is_valid:
        causes.append(f"Ok, '{uri.mimetype}' received.")
        app.logger.debug("Valid image received, saving ...")
        did_save, img_path = save_capture(uri, selected)
        if did_save:
            app.logger.debug(
                "Successfully saved '%s' in '%s'", RPS_OPTIONS[selected], img_path
            )
        else:
            app.logger.debug(
                "Unable to save '%s' in '%s'", RPS_OPTIONS[selected], img_path
            )

    return make_response(jsonify({"valid_capture": is_valid, "ack": causes}))


@app.route("/status", methods=["POST"])
def status():
    """Route to check the status of a task through web sockets."""
    room = request.json["room"]
    emit("status", request.json, room=room, namespace="/")

    return jsonify({})


@socketio.on("connect")
def events_connect():
    """Route to notify a new user has connected, and assign an ID."""
    userid = str(uuid.uuid4())
    session["userid"] = userid
    current_app.clients[userid] = request.namespace
    app.logger.info("Client connected! Assigned user id %s.", userid)
    room = f"uid-{userid}"
    join_room(room)
    emit("connected", {"user_id": userid})


@socketio.on("disconnect request")
def disconnect_request():
    """Route to notify that certain user has requested to disconnect."""
    emit("status", {"status": "Disconnected!"})
    disconnect()


@socketio.on("disconnect")
def events_disconnect():
    """Route to notify that certain user has been disconnected."""
    del current_app.clients[session["userid"]]
    room = f"uid-{session['userid']}"
    leave_room(room)
    app.logger.info("Client %s disconnected.", session["userid"])


if __name__ == "__main__":
    socketio.run(app, debug=DEBUG_MODE)
