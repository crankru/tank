from flask import Flask
from flask_socketio import SocketIO
from flask import Blueprint
# from Queue import Queue

from project import config

if not config.SEPARATE_STREAM_PROCESS:
    import eventlet
    eventlet.monkey_patch()

    # from gevent import monkey
    # # see: https://github.com/miguelgrinberg/Flask-SocketIO/issues/65
    # monkey.patch_all()

# app.queue = Queue()

socketio = SocketIO(async_mode='eventlet')
# socketio = SocketIO(app, async_mode='eventlet') # "threading", "eventlet" or "gevent"

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    import project.client
    import project.move
    app.register_blueprint(client.bp)
    app.register_blueprint(move.bp)

    socketio.init_app(app)
    return app