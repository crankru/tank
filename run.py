# from flask_socketio import SocketIO
# import ptvsd
# ptvsd.enable_attach(secret='12345', address=('192.168.1.123', 3000))
# # ptvsd.enable_attach(address = ('192.168.1.123', 3000))
# ptvsd.wait_for_attach()
# from project.views import *

from project import create_app, socketio

app = create_app()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')