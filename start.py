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
    # print('test')
    # buff1 = MOVE_PROC.stdout.read(1)
    # # buff2 = VIDEO_PROC.stdout.read(1)
    # if len(buff1) > 0:
    #     sys.stdout.write(buff1)
    #     # sys.stdout.write(buff2)
    #     sys.stdout.flush()
    # print('test')
    # stdout, stderr = MOVE_PROC.communicate()
    # print(stdout, stderr)
    time.sleep(1)