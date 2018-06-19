from flask import Flask
from flask_socketio import SocketIO
import config

app = Flask(__name__)
app.config.from_object(config)
socketio = SocketIO(app, async_mode='eventlet') # "threading", "eventlet" or "gevent"

from views import *