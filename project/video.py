import cv2 as cv
import time
from threading import Thread
import atexit

from picamera import PiCamera
from picamera.array import PiRGBArray


class VideoStream:
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

        cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
        cv.putText(self.frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

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
    
# import threading

# try:
#     from greenlet import getcurrent as get_ident
# except ImportError:
#     try:
#         from thread import get_ident
#     except ImportError:
#         from _thread import get_ident

# class CameraEvent():
#     def __init__(self):
#         self.events = {}

#     def wait(self):
#         ident = get_ident()
#         if ident not in self.events:
#             self.events[ident] = [threading.Event(), time.time()]
        
#         return self.events[ident][0].wait()

#     def set(self):
#         now = time.time()
#         remove = None
#         for ident, event in self.events.items():
#             if not event[0].isSet():
#                 event[0].set()
#                 event[1] = now
#             else:
#                 if now - event[1] > 5:
#                     remove = ident

#         if remove:
#             del self.events[remove]

#     def clear(self):
#         self.events[get_ident()][0].clear()

# class VideoThread(Thread):
#     thread = None
#     frame = None
#     last_access = 0
#     event = CameraEvent()

#     def __init__(self):
#         if VideoThread.thread is None:
#             VideoThread.last_access = time.time()

#             VideoThread.thread = threading.Thread(target=self._thread)
#             VideoThread.thread.start()

#             while self.get_frame() is None:
#                 time.sleep(0)

#     def get_frame(self):
#         VideoThread.last_access = time.time()
#         VideoThread.event.wait()
#         VideoThread.event.clear()

#         return VideoThread.frame

#     @staticmethod
#     def frames():
#         raise RuntimeError('Must be implemented by subclasses.')

#     @classmethod
#     def _thread(cls):
#         print('Starting camera thread.')
#         frames_iterator = cls.frames()
#         for frame in frames_iterator:
#             VideoThread.frame = frame
#             VideoThread.event.set()
#             time.sleep(0)

#             # if time.time() - VideoThread.last_access > 10:
#             #     frames_iterator.close()
#             #     print('Stopping camera thread due inactivity.')
#             #     break

#         VideoThread.thread = None

        
# import io
# import picamera

# class Camera(VideoThread):
#     @staticmethod
#     def frames():
#         # with picamera.PiCamera as camera:
#         camera = PiCamera()

#         time.sleep(2)    
#         stream = io.BytesIO()

#         resolution = (420, 380)
#         camera.resolution = resolution
#         # camera.framerate = 32
#         # rawCapture = PiRGBArray(camera, size=resolution)
#         # stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)

#         for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
#             stream.seek(0)
#             yield stream.read()

#             stream.seek(0)
#             stream.truncate()