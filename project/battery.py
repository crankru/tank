import serial

class BatteryControl:
    def __init__(self):
        self.port = serial.Serial(
            '/dev/ttyAMA0', 
            baudrate=115200, 
            timeout=1,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )

        self.max_voltage = 8
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
        pass