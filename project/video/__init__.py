from flask import Blueprint
bp = Blueprint('video', __name__)

from flask import render_template, Response, request

# from project import create_app, config
from project import config, socketio
from project.video.video import VideoStream

import time
import subprocess
import atexit
import os
import re

import cv2
import numpy as np
from picamera import PiCamera
from picamera.array import PiRGBArray

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        # self.video = cv2.VideoCapture(0)
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
        resolution = (320, 240)
        camera = PiCamera(resolution=resolution)
        rawCapture = PiRGBArray(camera, size=resolution)
        self.video = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
        time.sleep(2)

    def __del__(self):
        self.video.release()

    def get_frame(self):        
        for f in stream:
            yield(f.array)
            rawCapture.truncate(0)
            time.sleep(0)

    def get_image(self):
        frame = self.get_frame()
        # frame = self.modify_frame(frame)
        # print(type(frame))
        if type(frame) == np.ndarray:
            ret, jpeg = cv.imencode('.jpg', frame)
            # print(jpeg.tobytes())
            return jpeg.tobytes()
        else:
            # print('Huipizda!')
            return b''

def gen():
    camera = VideoCamera()

    while True:
        frame = camera.get_image()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# if not config.SEPARATE_STREAM_PROCESS:
#     @bp.route('/video_feed')
#     def video_feed():
#         # VS = VideoStream()
#         # VS.start()
#         # return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
#         return Response(gen(),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')