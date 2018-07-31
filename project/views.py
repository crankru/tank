from flask import render_template, Response, jsonify, request
from flask_socketio import emit

from project import app, socketio
from project import config
from project.move import RobotMove
from project.servo import ServoControl
from project.battery import BatteryControl

import time
import subprocess
import atexit

RM = RobotMove()
SC = ServoControl()
BATTERY = BatteryControl()


@app.before_first_request
def strat_video_stream():
    if app.config['SEPARATE_STREAM_PROCESS']:
        # print('Start video stream process...')
        # video_process = subprocess.Popen('python video-stream.py', shell=True, stdout=subprocess.PIPE)

        # def stop_video(process):
        #     print('Stop video stream process...')
        #     process.terminate()

        # atexit.register(stop_video, process=video_process)
        pass
    else:
        from project.video.video import VideoStream
        global VS
        VS = VideoStream()
        VS.start()

if not app.config['SEPARATE_STREAM_PROCESS']:
    @app.route('/video_feed')
    def video_feed():
        return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
        # return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # send camera status
    if not app.config['SEPARATE_STREAM_PROCESS']:
        cam_status = VS.get_status()
        # print('cam status', cam_status)
        socketio.emit('camera', {'status': cam_status}, namespace=config.SOCKET_NAMESPACE)

    servo = {
        'yMin': 300,
        'yMax': 520,
        'xMin': 150,
        'xMax': 500,
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

### Socket actions

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

    if message.get('active') == True:
        print('Start video stream')
        VS.start()
    else:
        print('Stop video stream')
        VS.stop()

    status = VS.get_status()
    emit('camera', {'res': True, 'status': status})

@socketio.on('battery', namespace=config.SOCKET_NAMESPACE)
def battery(message):
    BATTERY.update_data()
    emit('battery', {'res': True, 'data': BATTERY.get_data()})