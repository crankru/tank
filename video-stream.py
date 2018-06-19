from flask import Flask, render_template, Response, jsonify, request

from project.video import VideoStream
import time

app = Flask(__name__)

@app.before_first_request
def start_video():
    global VS
    VS = VideoStream()
    VS.start()

@app.route('/video_feed')
def video_feed():
    # global VS
    return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=False, port=5500)