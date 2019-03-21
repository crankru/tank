from flask import Blueprint
bp = Blueprint('client', __name__)

from flask import render_template, Response, request

# from project import create_app, config
from project import config, socketio
from project.move.move import RobotMove
from project.servo import ServoControl
from project.battery import BatteryControl
from project.video.video import VideoStream

import time
import subprocess
import atexit
import os
import re

RM = RobotMove()
SC = ServoControl()
# BATTERY = BatteryControl()

# app = create_app()

if not config.SEPARATE_STREAM_PROCESS:
    @bp.route('/video_feed')
    def video_feed():
        return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@bp.route('/')
def index():
    # send camera status
    if not config.SEPARATE_STREAM_PROCESS:
        cam_status = VS.get_status()
        # print('cam status', cam_status)
        socketio.emit('camera', {'status': cam_status}, namespace=config.SOCKET_NAMESPACE)

    servo = {
        'yMin': 300,
        'yMax': 550,
        'xMin': 150,
        'xMax': 550,
    }

    return render_template(
        'index.html', 
        mtime=time.time(), 
        socket_namespace=config.SOCKET_NAMESPACE,
        servo=servo
    )

# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield (b'--frame\r\n'
#             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')