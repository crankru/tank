import cv2 as cv
import time
from threading import Thread
import atexit

class VideoStream:
    def __init__(self, rm):
        height = 480
        width = 320
        fps = 25
        time.sleep(2)

        self.stream = cv.VideoCapture(0)
        self.stream.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 480)
        self.stream.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 320)
        # self.stream.set(5, framerate)
        # self.stream.set(cv.cv.CV_CAP_PROP_FPS, fps)

        self.cv_width = self.stream.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
        self.cv_height = self.stream.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)

        self.stopped = False
        # self.ret, self.frame = None

        self.rm = rm # RobotMove class

    def __del__(self):
        self.stream.release()
        cv.destroyAllWindows()

    def get_image(self):
        ret, jpeg = cv.imencode('.jpg', self.frame)
        return jpeg.tobytes()

    def get_frame(self):
        self.ret, self.frame = self.stream.read()

        # frame = cv.flip(frame, 1)
        speedLeft, speedRight = self.rm.getSpeed()

        h = int(self.cv_height  / 2)
        w = int(self.cv_width  / 2)

        cv.line(self.frame, (0, h), (480, h), (0, 255, 0), 1)
        cv.line(self.frame, (w, 0), (w, 320), (0, 255, 0), 1)

        cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
        cv.putText(self.frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        # fps = self.cap.get(cv.cv.CV_CAP_PROP_FPS)
        # cv.putText(frame, 'FPS: {}'.format(fps), (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)
        cv_speed_text = 'Speed: L{} R{}'.format(speedLeft, speedRight)
        cv.putText(self.frame, cv_speed_text, (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        # return self.get_image(frame)
        # return frame

    def get_fps(start_time, frame_count):
        pass

    def stop(self):
        self.stopped = True

    def start(self):
        t = Thread(target=self.update, args=())
        t.start()

    def update(self):
        while True:
            if self.stopped:
                return

            # (self.ret, self.frame) = self.stream.read()
            self.get_frame()

    def get_stream(self):
        while True:
            # frame = self.get_frame()
            frame = self.get_image()
            yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n{}\r\n\r\n'.format(frame))

    def run(self):
        while(True):
            # Capture frame-by-frame
            ret, frame = self.stream.read()
            # frame = cv.flip(frame, 1)

            h = int(self.cv_height  / 2)
            w = int(self.cv_width  / 2)

            cv.line(frame, (0, h), (480, h), (0, 255, 0), 1)
            cv.line(frame, (w, 0), (w, 320), (0, 255, 0), 1)

            cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
            cv.putText(frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

            # fps = self.stream.get(cv.cv.CV_CAP_PROP_FPS)
            # cv.putText(frame, 'FPS: {}'.format(fps), (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

            cv.imshow('frame', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break