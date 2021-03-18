from flask import Blueprint
bp = Blueprint('servo', __name__)

# from flask import render_template, Response, jsonify, request
from flask_socketio import emit

from project import socketio, config
from .servo import ServoControl

# import time
# import subprocess
# import atexit
# import os
# import re

SC = ServoControl(config.SERVO_DRIVER_ADDR)

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