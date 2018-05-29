from flask import Flask, render_template, Response, jsonify, request
# from flask_socketio import SocketIO, emit

from config import *
from project.video import VideoStream
# from project.move import RobotMove
# from project.servo import ServoControl
# from project.battery import BatteryControl

import time

app = Flask(__name__)

@app.before_first_request
def strat_video_stream():
    global VS
    print('Start video stream...')
    # VS = VideoStream(RM)
    VS = VideoStream()
    VS.start()
    time.sleep(2)

@app.route('/video_feed')
def video_feed():
    global VS
    return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response('', mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True, port=5500)