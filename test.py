import subprocess
import atexit
import signal
import sys
import time

print('START')

MOVE_PROC = subprocess.Popen(['python3', 'run.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
VIDEO_PROC = subprocess.Popen(['python3', 'video-stream.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# def stop_handler(signum, frame):
#     print('EXIT')
#     MOVE_PROC.terminate()
#     VIDEO_PROC.terminate()
#     sys.exit(1)

def kill_process(MOVE_PROC, VIDEO_PROC):
    print('EXIT')
    MOVE_PROC.terminate()
    VIDEO_PROC.terminate()

atexit.register(kill_process, MOVE_PROC, VIDEO_PROC)
# signal.signal(signal.SIGTERM, stop_handler)

while True:
    time.sleep(1)