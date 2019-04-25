from flask import Blueprint
bp = Blueprint('video', __name__)

from flask import Response, request

# from project import create_app, config
from project import config, socketio
# from project.video.video import VideoStream

import time
import os
# import re

import cv2
import numpy as np
# from picamera import PiCamera
from picamera.array import PiRGBArray

import io
import threading
import picamera


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def __init__(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            # while self.frame is None:
            #     time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        # self.initialize()
        # fh = open('tmp/test.jpg', 'rb')
        # self.frame = fh.read()
        # fh.close()
        if self.frame:
            return self.frame
        else:
            return b''

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            camera.resolution = (320, 240)

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


@bp.before_app_first_request 
def init():
    CAMERA = Camera()
    print('Init func')

def gen(camera):
    while True:
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + camera.get_frame() + b'\r\n')


if not config.SEPARATE_STREAM_PROCESS:
    @bp.route('/video_feed')
    def video_feed():
        # VS = VideoStream()
        # VS.start()
        # return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
        # return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')
        return Response(gen(CAMERA), mimetype='multipart/x-mixed-replace; boundary=frame')