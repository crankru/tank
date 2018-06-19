import cv2 as cv
import time
from threading import Thread
import atexit

from picamera import PiCamera
from picamera.array import PiRGBArray


class VideoStream:
    def __init__(self):
        # mode = 
        height = 480
        width = 320
        resolution = (height, width)
        fps = 25

        self.init_camera(resolution)

        # self.stream = cv.VideoCapture(0)
        # self.stream.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, resolution[0])
        # self.stream.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, resolution[1])
        # self.cv_width = self.stream.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
        # self.cv_height = self.stream.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)

        self.cv_width = self.camera.resolution[0]
        self.cv_height = self.camera.resolution[1]

        self.stopped = False
        self.frame = None
        self.thread = None
        # self.ret, 

        # self.rm = rm # RobotMove class

    def __del__(self):
        self.stream.release()
        cv.destroyAllWindows()

        self.stop()

    def init_camera(self, resolution):
        try:
            self.camera = PiCamera()
        except Exception:
            print('Camera initialization error')
            return None

        self.camera.resolution = resolution
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True)


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
        # self.ret, self.frame = self.stream.read()

        # frame = cv.flip(frame, 1)
        # speedLeft, speedRight = self.rm.getSpeed()

        h = int(self.cv_height  / 2)
        w = int(self.cv_width  / 2)

        cv.line(self.frame, (0, h), (480, h), (0, 255, 0), 1)
        cv.line(self.frame, (w, 0), (w, 320), (0, 255, 0), 1)

        cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
        cv.putText(self.frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        # fps = self.cap.get(cv.cv.CV_CAP_PROP_FPS)
        # cv.putText(frame, 'FPS: {}'.format(fps), (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        # cv_speed_text = 'Speed: L{} R{}'.format(speedLeft, speedRight)
        # cv.putText(self.frame, cv_speed_text, (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        # return self.get_image(frame)
        # return frame

    def get_status(self):
        return not self.stopped

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True

        self.stream.close()
        self.rawCapture.close()
        self.camera.close()

    def start(self):
        if not self.thread:
            self.thread = Thread(target=self.update, args=()).start()

        # t.start()
        time.sleep(2)
        return self

    def update(self):
        # while True:
        #     if self.stopped:
        #         return

        #     # (self.ret, self.frame) = self.stream.read()
        #     self.get_frame()
        #     time.sleep(0)

        for f in self.stream:
            self.frame = f.array
            # self.modify_frame()
            self.rawCapture.truncate(0)

            # time.sleep(0)

            if self.stopped:
                return

    def get_stream(self):
        while True:
            # frame = self.get_frame()
            image = self.get_image()
            # time.sleep(0.01)
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n{}\r\n\r\n'.format(image))

    # def run(self):
    #     while(True):
    #         # Capture frame-by-frame
    #         ret, frame = self.stream.read()
    #         # frame = cv.flip(frame, 1)

    #         h = int(self.cv_height  / 2)
    #         w = int(self.cv_width  / 2)

    #         cv.line(frame, (0, h), (480, h), (0, 255, 0), 1)
    #         cv.line(frame, (w, 0), (w, 320), (0, 255, 0), 1)

    #         cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
    #         cv.putText(frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

    #         # fps = self.stream.get(cv.cv.CV_CAP_PROP_FPS)
    #         # cv.putText(frame, 'FPS: {}'.format(fps), (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

    #         cv.imshow('frame', frame)

    #         if cv.waitKey(1) & 0xFF == ord('q'):
    #             break