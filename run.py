from project import app, socketio, config

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, threaded=config.DEBUG)
    socketio.run(app, host='0.0.0.0', debug=config.DEBUG)