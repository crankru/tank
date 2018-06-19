from flask import Flask
from flask_socketio import SocketIO
import config

import eventlet
eventlet.monkey_patch()

# from gevent import monkey
# # see: https://github.com/miguelgrinberg/Flask-SocketIO/issues/65
# monkey.patch_all()

app = Flask(__name__)
app.config.from_object(config)
socketio = SocketIO(app, async_mode='eventlet') # "threading", "eventlet" or "gevent"

from views import *