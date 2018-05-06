import cv2 as cv
import time
import subprocess as sp
import atexit

class VideoStream:
    def __init__(self):
        height = 480
        width = 320
        fps = 50
        # bytesPerFrame = width * height

        # videoCmd = "raspividyuv -w "+str(width)+" -h "+str(height)+" --output - --timeout 0 --framerate "+str(fps)+" --luma --nopreview"
        # videoCmd = videoCmd.split() # Popen requires that each parameter is a separate string
        # # print(videoCmd)
        
        # cameraProcess = sp.Popen(videoCmd, stdout=sp.PIPE)
        # atexit.register(cameraProcess.terminate)
        # rawStream = cameraProcess.stdout.read(bytesPerFrame)

        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.cv.CV_CAP_PROP_FRAME_WIDTH, 480)
        self.cap.set(cv.cv.CV_CAP_PROP_FRAME_HEIGHT, 320)
        # self.cap.set(5, framerate)
        self.cap.set(cv.cv.CV_CAP_PROP_FPS, fps)

        self.cv_width = self.cap.get(cv.cv.CV_CAP_PROP_FRAME_WIDTH)
        self.cv_height = self.cap.get(cv.cv.CV_CAP_PROP_FRAME_HEIGHT)

        time.sleep(2)

    def __del__(self):
        self.cap.release()
        cv.destroyAllWindows()

    def get_image(self, frame):
        ret, jpeg = cv.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_frame(self):
        ret, frame = self.cap.read()

        # frame = cv.flip(frame, 1)

        h = int(self.cv_height  / 2)
        w = int(self.cv_width  / 2)

        cv.line(frame, (0, h), (480, h), (0, 255, 0), 1)
        cv.line(frame, (w, 0), (w, 320), (0, 255, 0), 1)

        cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
        cv.putText(frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        # fps = self.cap.get(cv.cv.CV_CAP_PROP_FPS)
        # cv.putText(frame, 'FPS: {}'.format(fps), (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

        return self.get_image(frame)
        # return frame


    def run(self):
        while(True):
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # frame = cv.flip(frame, 1)

            h = int(self.cv_height  / 2)
            w = int(self.cv_width  / 2)

            cv.line(frame, (0, h), (480, h), (0, 255, 0), 1)
            cv.line(frame, (w, 0), (w, 320), (0, 255, 0), 1)

            cv_text = '{}x{}'.format(self.cv_width, self.cv_height)
            cv.putText(frame, cv_text, (5, 10), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

            # fps = self.cap.get(cv.cv.CV_CAP_PROP_FPS)
            # cv.putText(frame, 'FPS: {}'.format(fps), (5, 20), cv.FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0), 1)

            cv.imshow('frame', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break