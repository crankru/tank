from flask import Blueprint
bp = Blueprint('move', __name__)

from flask import render_template, Response, jsonify, request
from flask_socketio import emit

from project import socketio, config
# from project import create_app, socketio, config
from project import socketio
from project.move.move import RobotMove
# from project.video.video import VideoStream

import time
import subprocess
import atexit
import os
import re

RM = RobotMove()

@socketio.on('connect', namespace=config.SOCKET_NAMESPACE)
def connection():
    emit('connection', {'data': 'connected'})

# @socketio.on('disconnect', namespace='/socket')
# def disconnect():
#     print('WS disconnected')

@socketio.on('move', namespace=config.SOCKET_NAMESPACE)
def move(message):
    # print(message)
    action = message.get('action')
    x = int(message.get('x', 0))
    y = int(message.get('y', 0))
    speed = int(message.get('speed', 0))
    radian = float(message.get('angle', 0))
    direction = message.get('direction', {})

    if action == 'stop':
        RM.stop()
        # print('stop')
    elif action == 'move':
        # print(x, y)
        # RM.setX(x)
        # RM.setY(y)
        RM.setSpeedAndRadian(speed, radian, direction)

    else:
        print('Error: Unknown action "{}"'.format(action))
        emit('move', {'res': False, 'data': 'Unknown action'})

    emit('move', {'res': True, 'data': 'OK', 'params': {'x': x, 'y': y}})

@socketio.on('temperature', namespace=config.SOCKET_NAMESPACE)
def temperature(message):
    # from vcgencmd import Vcgencmd
    # vcgm = Vcgencmd()
    # print(vcgm.measure_temp())
    # tmp = os.popen("vcgencmd measure_temp").readline()
    tmp = os.popen("vcgencmd measure_temp").readline()
    r = re.search(r'temp=([0-9\.]+)', tmp)
    
    if r and r.group(1):
        emit('temperature', {'temperature': r.group(1)})