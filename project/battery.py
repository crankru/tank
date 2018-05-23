import serial

class BatteryControl:
    def __init__(self):
        self.port = serial.Serial(
            # '/dev/ttyAMA0', 
            '/dev/ttyS0',
            baudrate=115200, 
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            write_timeout=5
        )

        self.max_voltage = 8.5
        self.min_voltage = 6

    def __del__(self):
        self.port.close()

    def write(self, data):
        return self.port.write(data)

    def read(self):
        cnt = self.port.inWaiting()
        res = self.port.read(cnt)
        return res

    def getBatteryPerc(self):
        pass

    def getVoltage(self):
        self.port.write('Off')
        print(self.port.read(8))

if __name__ == '__main__':
    import time
    bc = BatteryControl()
    # print(bc.port.readline())

    print('Start test')
    print('Serial open: {}'.format(bc.port.is_open))

    bc.write(b'Get\n')
    # time.sleep(0.3)
    print('RES: {}'.format(bc.read()))
    bc.write(b'On\n')
    print('RES: {}'.format(bc.read()))
    bc.write(b'Off\r\n')
    print('RES: {}'.format(bc.read()))
    bc.write(b'Start\n')
    print('RES: {}'.format(bc.read()))
    bc.write(b'Stop\n')
    print('RES: {}'.format(bc.read()))
    print('RES: {}'.format(bc.port.read(10)))

    # print('RES: {}'.format(bc.port.readline()))