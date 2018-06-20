from flask import Flask
from flask_socketio import SocketIO
# from Queue import Queue

import eventlet
eventlet.monkey_patch()

# from gevent import monkey
# # see: https://github.com/miguelgrinberg/Flask-SocketIO/issues/65
# monkey.patch_all()

from project import config

app = Flask(__name__)
app.config.from_object(config)
# app.queue = Queue()

socketio = SocketIO(app, async_mode='eventlet') # "threading", "eventlet" or "gevent"

from project.views import *