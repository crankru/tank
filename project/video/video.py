import cv2 as cv
import time
from threading import Thread

from picamera import PiCamera
from picamera.array import PiRGBArray

# from project.video.base_camera import BaseCamera
from project.video.driver_picamera import Camera


class VideoStream():
    stopped = False

    def __init__(self):
        # mode = 
        # resolution = (640, 480)
        resolution = (320, 240)
        fps = 25

        self.driver = Camera(resolution=resolution, fps=fps)

        self.cv_width = resolution[0]
        self.cv_height = resolution[1]

    def __del__(self):
        self.stop()

    def get_image(self):
        frame = self.driver.get_frame()
        # frame = self.modify_frame(frame)
        if frame:
            ret, jpeg = cv.imencode('.jpg', frame)
            return jpeg.tobytes()
        else:
            # print('Huipizda!')
            return b''

    def take_photo(self):
        img = self.get_image()

    def modify_frame(self, frame):
        h = int(self.cv_height  / 2)
        w = int(self.cv_width  / 2)

        cv.line(frame, (0, h), (480, h), (0, 255, 0), 1)
        cv.line(frame, (w, 0), (w, 320), (0, 255, 0), 1)

        # cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
        # cv.putText(self.frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

    def get_status(self):
        return not self.stopped

    def stop(self):
        self.driver.stop()

    def start(self):
        self.driver.start()

    def get_stream(self):
        while True:
            image = self.get_image()
            time.sleep(0)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n\r\n')
    