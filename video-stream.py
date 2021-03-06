from flask import Flask, Response

# from project import config
# from project.video.video import VideoStream
import time

app = Flask(__name__)

import io
import threading
import picamera


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            # camera.hflip = True
            # camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break

        cls.thread = None

# @app.before_first_request
# def start_video():
#     global VS
#     VS = VideoStream()
#     VS.start()

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    # return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=config.DEBUG, threaded=True, port=config.SEPARATE_STREAM_PORT)
    app.run(host='0.0.0.0', debug=True, port=5500, threaded=True)