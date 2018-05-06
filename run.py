from flask import Flask, render_template, Response
from VideoStream import VideoStream

app = Flask(__name__)

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
    return Response('test')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)