from flask import Flask, render_template, Response, jsonify, request
from flask_socketio import SocketIO, emit

from VideoStream import VideoStream
from RobotMove import RobotMove
from config import *

import time

app = Flask(__name__)
app.config['SECRET_KEY'] = SOCKET_SECRET
socketio = SocketIO(app)

@app.before_first_request
def strat_video_stream():
    global VS, RM
    RM = RobotMove()

    print('Start video stream...')
    VS = VideoStream(RM)
    VS.start()
    time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html', mtime=time.time())      

@app.route('/video_feed')
def video_feed():
    global VS
    return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response('', mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect', namespace='/socket')
def action():
    emit('my response', {'data': 'WS connected'})

# @socketio.on('disconnect', namespace='/socket')
# def test_disconnect():
#     print('WS disconnected')

@socketio.on('action', namespace='/socket')
def action(message):
    action = message.get('action')
    x = int(message.get('x', 0))
    y = int(message.get('y', 0))

    if action == 'stop':
        RM.stop()
        # print('stop')
    elif action == 'move':
        # print(x, y)
        RM.setX(x)
        RM.setY(y)
        # pass

    else:
        print('Error: Unknown action "{}"'.format(action))
        emit('my response', {'res': False, 'data': 'Unknown action'})

    emit('my response', {'res': True, 'data': 'OK', 'params': {'x': x, 'y': y}})

@socketio.on('camera_control', namespace='/socket')
def camera_control(message):
    pass

@app.route('/test')
def test():
    return render_template('test.html')

# @app.route('/action')
# def action():
#     action = request.args.get('action')

#     if action == 'stop':
#         RM.stop()
#     elif action == 'move':
#         x = int(request.args.get('x', 0))
#         y = int(request.args.get('y', 0))
#         # print(x, y)

#         RM.setX(x)
#         RM.setY(y)

#     else:
#         print('Error: Unknown action "{}"'.format(action))

#     return jsonify({'res': True})

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, threaded=True)
    socketio.run(app, host='0.0.0.0', debug=True)