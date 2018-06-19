from flask import render_template, Response, jsonify, request
from flask_socketio import emit

from project import app, socketio
import config

from video import VideoStream
from move import RobotMove
from servo import ServoControl

import time

RM = RobotMove()
SC = ServoControl()
# # BATTERY = BatteryControl()

@app.before_first_request
def strat_video_stream():
    global VS
    VS = VideoStream()
    VS.start()

@app.route('/')
def index():
    # global VS

    # send camera status
    if VS:
        cam_status = VS.get_status()
        # print('cam status', cam_status)
        socketio.emit('camera', {'status': cam_status}, namespace=config.SOCKET_NAMESPACE)

    return render_template('index.html', mtime=time.time(), socket_namespace=config.SOCKET_NAMESPACE)      

@app.route('/video_feed')
def video_feed():
    global VS
    return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response('', mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def test():
    return render_template('test.html')


### Socket actions

@socketio.on('connect', namespace=config.SOCKET_NAMESPACE)
def action():
    emit('connection', {'data': 'WS connected'})

# @socketio.on('disconnect', namespace='/socket')
# def test_disconnect():
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

@socketio.on('camera', namespace=config.SOCKET_NAMESPACE)
def camera(message):
    global VS
    print('camera msg: ', message)

    if message.get('active') == True:
        print('Start video stream')
        VS.start()
    else:
        print('Stop video stream')
        VS.stop()

    status = VS.get_status()
    emit('camera', {'res': True, 'status': status})