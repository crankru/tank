from flask import Blueprint
from flask_socketio import emit

from project import socketio, config
from .battery import BatteryControl

bp = Blueprint('battery', __name__)

# import time
# import subprocess
# import atexit
# import os
# import re

try:
    BATTERY = BatteryControl(config.INA219_ADDR)
except Exception as e:
    print(f'ERROR: {e}')

@socketio.on('battery', namespace=config.SOCKET_NAMESPACE)
def battery(message):
    if 'BATTERY' in globals():
        BATTERY.update_data()
        print('BATTERY', BATTERY.get_data())
        # emit('battery', {'res': True, 'data': BATTERY.get_data()})