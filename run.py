from flask import Flask, render_template, Response, jsonify, request
from VideoStream import VideoStream
from RobotMove import RobotMove

app = Flask(__name__)
RM = RobotMove()

@app.route('/')
def index():
    return render_template('index.html')

def gen(vs):
    while True:
        frame = vs.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n{}\r\n\r\n'.format(frame))

@app.route('/video_feed')
def video_feed():
    # vs = VideoStream()
    # return Response(gen(vs), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response('', mimetype='multipart/x-mixed-replace; boundary=frame')

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

    res = {'res': True}
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)