from project.video.base_camera import BaseCamera

import io
import time
from picamera import PiCamera
from picamera.array import PiRGBArray

class Camera(BaseCamera):

    @staticmethod
    def frames():
        resolution = BaseCamera.resolution
        framerate = BaseCamera.fps

        try:
            camera = PiCamera(resolution=resolution, framerate=framerate)
        except Exception:
            print('Camera initialization error')
            return False
            
        else:
            rawCapture = PiRGBArray(camera, size=resolution)
            stream = camera.capture_continuous(rawCapture, format='bgr', use_video_port=True)
            time.sleep(2)

        for f in stream:
            yield(f.array)
            rawCapture.truncate(0)
            time.sleep(0)