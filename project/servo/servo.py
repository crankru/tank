from drivers.Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from drivers.Raspi_PWM_Servo_Driver import PWM

import time

class ServoControl:
    def __init__(self, address=0x70):
        # self.pwm = PWM(0x6F)
        self.pwm = PWM(address)
        self.pwm.setPWMFreq(50) # 60

        self.x = self.centerX = 350 #400
        self.y = self.centerY = 500 #500

        # self.maxPosition = 50
        # self.minPulse = 150  # Min pulse length out of 4096
        # self.maxPulse = 550  # Max pulse length out of 4096

        # self.center()

    def __del__(self):
        self.pwm.setAllPWM(0, 0)

    def setX(self, x):
        self.x = int(x)
        self.pwm.setPWM(0, 0, int(x))
        # print('X:', type(self.x), x)

    def setY(self, y):
        self.y = int(y)
        self.pwm.setPWM(1, 0, int(y))
        # print('Y:', type(self.y), y)

    def move(self, x, y):
        # speedX = self.calcSpeed(x)
        # speedY = self.calcSpeed(y)
        # print(x, y)

        if x != self.x:
            self.setX(x)

        if y != self.y:    
            self.setY(y)
        
        # self.pwm.setPWM(0, 0, speedX)
        # self.pwm.setPWM(1, 0, speedY)

    def stop(self):
        # print('I dont know how to stop servo :(')
        self.pwm.setAllPWM(0, 0)

    def center(self):
        self.pwm.setPWM(0, 0, self.centerX)
        # time.sleep(1)
        self.pwm.setPWM(1, 0, self.centerY)

    # def calcSpeed(self, value):
    #     if value == 0:
    #         return 0

    #     perc = float(abs(value)) / float(self.maxPosition)
    #     speed = int(self.maxPulse * perc)
    #     # print(float(abs(value)) / float(self.maxPosition))
    #     # print(value, perc, speed)
    #     if speed < self.minPulse:
    #         speed = self.minPulse
    #     return speed