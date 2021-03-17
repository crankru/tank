from flask import Blueprint
bp = Blueprint('move', __name__)

from flask import render_template, Response, jsonify, request
from flask_socketio import emit

from project import socketio, config
# from project import create_app, socketio, config
from project import socketio
from project.move.move import RobotMove
from project.servo import ServoControl
from project.battery import BatteryControl
# from project.video.video import VideoStream

import time
import subprocess
import atexit
import os
import re

RM = RobotMove()
# SC = ServoControl()
# BATTERY = BatteryControl()

# app = create_app()

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

@socketio.on('servo', namespace=config.SOCKET_NAMESPACE)
def servo(message):
    action = message.get('action')
    x = int(message.get('x', 0))
    y = int(message.get('y', 0))
    # print(x, y)

    if action ==  'stop':
        SC.stop()
    elif action == 'move':
        SC.move(x, y)
    elif action == 'center':
        SC.center()
        emit('servo', {'res': True, 'action': 'center'})
    else:
        print('Error: Unknown action "{}"'.format(action))
        emit('servo', {'res': False, 'data': 'Unknown action'})

    emit('servo', {'res': True})

@socketio.on('camera', namespace=config.SOCKET_NAMESPACE)
def camera(message):
    print('camera msg: ', message)

    if message.get('action') == 'take_photo':
        VS.take_photo()
    elif message.get('active') == True:
        print('Start video stream')
        VS.start()
    else:
        print('Stop video stream')
        VS.stop()

    status = VS.get_status()
    emit('camera', {'res': True, 'status': status})

# @socketio.on('battery', namespace=config.SOCKET_NAMESPACE)
# def battery(message):
#     BATTERY.update_data()
#     emit('battery', {'res': True, 'data': BATTERY.get_data()})

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