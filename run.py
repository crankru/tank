from flask import Flask, render_template, Response, jsonify, request
from flask_socketio import SocketIO, emit

from config import *
from project.video import VideoStream
from project.move import RobotMove
from project.servo import ServoControl
# from project.battery import BatteryControl

import time

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = 'threading' #None

app = Flask(__name__)
# secret key from config.py
app.config['SECRET_KEY'] = SOCKET_SECRET
socketio = SocketIO(app, async_mode=async_mode)

RM = RobotMove()
SC = ServoControl()
# BATTERY = BatteryControl()

@app.before_first_request
def strat_video_stream():
    global VS
    print('Start video stream...')
    # VS = VideoStream(RM)
    VS = VideoStream()
    VS.start()
    time.sleep(2)

@app.route('/')
def index():
    # global VS

    # send camera status
    # cam_status = VS.get_status()
    # print('cam status', cam_status)
    # socketio.emit('camera', {'status': cam_status}, namespace=SOCKET_NAMESPACE)

    return render_template('index.html', mtime=time.time(), socket_namespace=SOCKET_NAMESPACE)      

@app.route('/video_feed')
def video_feed():
    global VS
    return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response('', mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return render_template('test.html')

#
# Socket actions
#

@socketio.on('connect', namespace=SOCKET_NAMESPACE)
def action():
    emit('connection', {'data': 'WS connected'})

# @socketio.on('disconnect', namespace='/socket')
# def test_disconnect():
#     print('WS disconnected')

# TODO update control algoritm
@socketio.on('move', namespace=SOCKET_NAMESPACE)
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

@socketio.on('servo', namespace=SOCKET_NAMESPACE)
def servo(message):
    action = message.get('action')
    x = int(message.get('x', 0))
    y = int(message.get('y', 0))

    if action ==  'stop':
        SC.stop(0)
        SC.stop(1)
    elif action == 'move':
        SC.move(x, y)
    elif action == 'center':
        SC.center()
    else:
        print('Error: Unknown action "{}"'.format(action))
        emit('servo', {'res': False, 'data': 'Unknown action'})

    emit('servo', {'res': True})

@socketio.on('camera', namespace=SOCKET_NAMESPACE)
def camera(message):
    print(message)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, threaded=True)
    socketio.run(app, host='0.0.0.0', debug=True)