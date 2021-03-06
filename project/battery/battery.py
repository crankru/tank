# from ina219 import INA219, DeviceRangeError
# from project import config

class BatteryControl:
    def __init__(self, address=None):
        SHUNT_OHMS = 0.1
        self.ina = INA219(SHUNT_OHMS, address=address)
        self.ina.configure()

        self.voltage = None #Bus coltage V
        self.current = None #Bus current mA
        self.power = None #Power mW
        self.shunt_voltage = None #Shunt voltage mV

    def update_data(self):
        try:
            self.voltage = self.ina.voltage()
            self.current = self.ina.current()
            self.power = self.ina.power()
            self.shunt_voltage = self.ina.shunt_voltage()
        except DeviceRangeError as e:
            print(e)

    def get_data(self):
        return {
            'voltage': self.voltage,
            'current': self.current,
            'power': self.power,
            'shunt_voltage': self.shunt_voltage,
        }

    def print(self):
        print("Bus Voltage: %.3f V" % self.ina.voltage())
        try:
            print("Bus Current: %.3f mA" % self.ina.current())
            print("Power: %.3f mW" % self.ina.power())
            print("Shunt voltage: %.3f mV" % self.ina.shunt_voltage())
        except DeviceRangeError as e:
            # Current out of device range with specified shunt resister
            print(e)

if __name__== '__main__':
    bc = BatteryControl(0x40)
    bc.print()

    # import board
    # from adafruit_ina219 import ADCResolution, BusVoltageRange, INA219
    
    # i2c_bus = board.I2C()
    # print(i2c_bus.__dict__)
    # ina219 = INA219(i2c_bus)
    
    # print("ina219 test")
    
    # # display some of the advanced field (just to test)
    # print("Config register:")
    # print("  bus_voltage_range:    0x%1X" % ina219.bus_voltage_range)
    # print("  gain:                 0x%1X" % ina219.gain)
    # print("  bus_adc_resolution:   0x%1X" % ina219.bus_adc_resolution)
    # print("  shunt_adc_resolution: 0x%1X" % ina219.shunt_adc_resolution)
    # print("  mode:                 0x%1X" % ina219.mode)
    # print("")


# import serial

# class BatteryControl:
#     def __init__(self):
#         self.port = serial.Serial(
#             # '/dev/ttyAMA0', 
#             '/dev/ttyS0',
#             baudrate=115200, 
#             timeout=1,
#             parity=serial.PARITY_NONE,
#             stopbits=serial.STOPBITS_ONE,
#             bytesize=serial.EIGHTBITS,
#             write_timeout=5
#         )

#         self.max_voltage = 8.5
#         self.min_voltage = 6

#     def __del__(self):
#         self.port.close()

#     def write(self, data):
#         return self.port.write(data)

#     def read(self):
#         cnt = self.port.inWaiting()
#         res = self.port.read(cnt)
#         return res

#     def getBatteryPerc(self):
#         pass

#     def getVoltage(self):
#         self.port.write('Off')
#         print(self.port.read(8))

# if __name__ == '__main__':
#     import time
#     bc = BatteryControl()
#     # print(bc.port.readline())

#     print('Start test')
#     print('Serial open: {}'.format(bc.port.is_open))

#     bc.write(b'Get\n')
#     # time.sleep(0.3)
#     print('RES: {}'.format(bc.read()))
#     bc.write(b'On\n')
#     print('RES: {}'.format(bc.read()))
#     bc.write(b'Off\r\n')
#     print('RES: {}'.format(bc.read()))
#     bc.write(b'Start\n')
#     print('RES: {}'.format(bc.read()))
#     bc.write(b'Stop\n')
#     print('RES: {}'.format(bc.read()))
#     print('RES: {}'.format(bc.port.read(10)))

#     # print('RES: {}'.format(bc.port.readline()))