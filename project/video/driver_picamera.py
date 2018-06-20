from project.video.base_camera import BaseCamera

import io
import picamera

# class Camera(BaseCamera):
class Camera():
    @staticmethod
    def frames():
        # with picamera.PiCamera as camera:
        camera = PiCamera()
        time.sleep(2)    
        stream = io.BytesIO()

        resolution = (320, 240)
        camera.resolution = resolution
        # camera.framerate = 32
        # rawCapture = PiRGBArray(camera, size=resolution)
        # stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)

        for _ in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
            stream.seek(0)
            yield stream.read()

            stream.seek(0)
            stream.truncate()