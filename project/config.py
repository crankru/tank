DEBUG = True
MOTOR_DRIVER = 'l298n'
SECRET_KEY = 'sdf7s9d86f9BSFD879Sd76f9s8d76fm46mn45'
SOCKET_NAMESPACE = '/robot'

INIT_MOVE = True

INIT_SERVO = True
SERVO_DRIVER_ADDR = 0x70

INIT_VIDEO = False

INIT_BATTERY = False
INA219_ADDR = 0x40

INIT_MOVE = True
INIT_SERVO = False
INIT_VIDEO = False

# video streaming in separate process
SEPARATE_STREAM_PROCESS = False
SEPARATE_STREAM_PORT = 5500
SEPARATE_STREAM_HOST = '192.168.1.123'
# SEPARATE_STREAM_HOST = '10.5.5.1'