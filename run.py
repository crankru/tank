# from flask import Flask, render_template, Response, jsonify, request
# from flask_socketio import SocketIO, emit
# # from Queue import Queue

# import config
# from project.video import VideoStream
# from project.move import RobotMove
# from project.servo import ServoControl
# # from project.battery import BatteryControl

# import time

# app = Flask(__name__)
# app.config.from_object(config)
# # app.queue = Queue()


# RM = RobotMove()
# SC = ServoControl()
# # BATTERY = BatteryControl()

# socketio = SocketIO(app, async_mode='eventlet') # "threading", "eventlet" or "gevent"

from project import app, socketio, config

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, threaded=config.DEBUG)
    socketio.run(app, host='0.0.0.0', debug=config.DEBUG)