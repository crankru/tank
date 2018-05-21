import serial

class BatteryControl:
    def __init__(self):
        self.port = serial.Serial(
            '/dev/ttyAMA0', 
            baudrate=115200, 
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=1,
            bytesize=8,
            write_timeout=5
        )

        self.max_voltage = 8.5
        self.min_voltage = 6

    def __del__(self):
        self.port.close()

    def write(self, data):
        self.port.write(data)

    def read(self):
        return self.port.readline()

    def getBatteryPerc(self):
        pass

    def getVoltage(self):
        self.port.write('Off')
        print(self.port.read(8))

if __name__ == '__main__':
    import time
    bc = BatteryControl()
    # print(bc.port.readline())
    
    while True:
        print(bc.port.readline())
        print('read')
        time.sleep(1)
        bc.port.write(b'\r\n')
        print('write1')
        bc.port.write(b'Get\r\n')
        print('write2')
