"""Initialize API module
"""
import os
from os import listdir
from os.path import isfile, join

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from celery import Celery

from .constant import (
    LOCAL_STORAGE,
    STORAGE_TRACKER,
    RPS_OPTIONS
    )
from .config import celeryconfig


app = Flask(__name__)
app.clients = {}
CORS(app)
app.config['SECRET_KEY'] = 'top-secret!'

socketio = SocketIO(app, cors_allowed_origins="*")

# Initialize Celery
celery = Celery(app.name)
celery.config_from_object(celeryconfig)
celery.conf.update(app.config)

# Create folders to store images if not existing
try:
    for v in RPS_OPTIONS.values():
        os.makedirs(LOCAL_STORAGE + '/' + v, exist_ok=True)
except FileExistsError:
    pass

# Find all images in local storage, and group them by label
for label in RPS_OPTIONS.values():
    onlyfiles = [
        f for f in listdir(f"{LOCAL_STORAGE}/{label}/")
        if isfile(join(f"{LOCAL_STORAGE}/{label}/", f))     # TODO: ignore non-image files
        ]
    STORAGE_TRACKER[label] = onlyfiles
