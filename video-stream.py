from flask import Flask, Response

from project import config
from project.video.video import VideoStream
import time

app = Flask(__name__)

@app.before_first_request
def start_video():
    global VS
    VS = VideoStream()
    VS.start()

@app.route('/video_feed')
def video_feed():
    return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=config.DEBUG, threaded=False, port=config.SEPARATE_STREAM_PORT)