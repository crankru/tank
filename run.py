from flask import Flask, render_template, Response, jsonify, request
from VideoStream import VideoStream
from RobotMove import RobotMove

import time

app = Flask(__name__)

@app.before_first_request
def strat_video_stream():
    global VS, RM
    RM = RobotMove()

    print('Start video stream...')
    VS = VideoStream(RM)
    VS.start()
    time.sleep(2)

@app.route('/')
def index():
    return render_template('index.html')      

@app.route('/video_feed')
def video_feed():
    global VS
    return Response(VS.get_stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response('', mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/action')
def action():
    action = request.args.get('action')

    if action == 'stop':
        RM.stop()
    elif action == 'move':
        x = int(request.args.get('x', 0))
        y = int(request.args.get('y', 0))
        # print(x, y)

        RM.setX(x)
        RM.setY(y)

    else:
        print('Error: Unknown action "{}"'.format(action))

    return jsonify({'res': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)