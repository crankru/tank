from flask import Flask
from flask_socketio import SocketIO
from flask import Blueprint
# from Queue import Queue

from project import config

# if config.INIT_MOVE:
#     from project.move.move import RobotMove

# if config.INIT_SERVO:
#     from project.servo import ServoControl

# from project.battery import BatteryControl

# if config.INIT_VIDEO:
#     from project.video.video import VideoStream

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
    app.register_blueprint(client.bp)

    if app.config['INIT_MOVE']:
        import project.move
        app.register_blueprint(move.bp)

    if app.config['INIT_SERVO']:
        import project.servo
        app.register_blueprint(servo.bp)
    
    if app.config['INIT_VIDEO']:
        import project.video
        app.register_blueprint(video.bp)

    if app.config['INIT_BATTERY']:
        import project.battery
        app.register_blueprint(battery.bp)

    socketio.init_app(app)
    return app