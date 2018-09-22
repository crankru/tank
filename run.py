# import ptvsd

# ptvsd.enable_attach(secret='12345', address=('192.168.1.123', 3000))
# # ptvsd.enable_attach(address = ('192.168.1.123', 3000))
# ptvsd.wait_for_attach()

from project import app, socketio, config

if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True, threaded=config.DEBUG)
    socketio.run(app, host='0.0.0.0', debug=config.DEBUG)