import cv2 as cv
import time
from threading import Thread

from picamera import PiCamera
from picamera.array import PiRGBArray

from project.video.base_camera import BaseCamera
from project.video.driver_picamera import Camera


class VideoStream():
    stopped = False
    frame = None
    thread = None

    def __init__(self):
        # mode = 
        # resolution = (640, 480)
        resolution = (320, 240)
        fps = 25

        self.init_camera(resolution)

    def __del__(self):
        self.stop()

    def init_camera(self, resolution):
        try:
            self.camera = PiCamera()
        except Exception:
            print('Camera initialization error')
            return None
        else:
            self.camera.resolution = resolution
            self.camera.framerate = 32
            self.rawCapture = PiRGBArray(self.camera, size=resolution)
            self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True)
            self.cv_width = self.camera.resolution[0]
            self.cv_height = self.camera.resolution[1]


    def get_image(self):
        # if self.frame:
        #     ret, jpeg = cv.imencode('.jpg', self.frame)
        #     return jpeg.tobytes()
        # else:
        #     return None

        ret, jpeg = cv.imencode('.jpg', self.frame)
        return jpeg.tobytes()

    def take_photo(self):
        img = self.get_image()

    def modify_frame(self):
        h = int(self.cv_height  / 2)
        w = int(self.cv_width  / 2)

        cv.line(self.frame, (0, h), (480, h), (0, 255, 0), 1)
        cv.line(self.frame, (w, 0), (w, 320), (0, 255, 0), 1)

        # cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
        # cv.putText(self.frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

    def get_status(self):
        return not self.stopped

    # def read(self):
    #     return self.frame

    def stop(self):
        self.stopped = True

        self.stream.close()
        self.rawCapture.close()
        self.camera.close()

    def start(self):
        if not self.thread:
            self.thread = Thread(target=self.update)
            self.thread.start()

        # t.start()
        time.sleep(2)
        # return self

    def update(self):
        for f in self.stream:
            self.frame = f.array
            # self.modify_frame()
            self.rawCapture.truncate(0)
            time.sleep(0)

            if self.stopped:
                return

    def get_stream(self):
        while True:
            # frame = self.get_frame()
            image = self.get_image()
            time.sleep(0)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n{}\r\n\r\n'.format(image))
    