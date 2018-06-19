from flask import Flask, render_template, Response, jsonify, request
# from flask_socketio import SocketIO, emit

from config import *
from project.video import VideoStream
import time

app = Flask(__name__)

print('Start video stream...')
VS = VideoStream()
VS.start()
time.sleep(2)

@app.route('/video_feed')
def video_feed():
    global VS
    return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=False, port=5500)