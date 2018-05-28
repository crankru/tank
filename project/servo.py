from driver.Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from driver.Raspi_PWM_Servo_Driver import PWM

class ServoControl:
    def __init__(self):
        self.pwm = PWM(0x6F)
        self.pwm.setPWMFreq(60) 

        self.maxPosition = 50
        self.minSpeed = 20  # Min pulse length out of 4096
        self.maxSpeed = 150  # Max pulse length out of 4096

    def __del__(self):
        self.pwm.setAllPWM(0, 0)

    def move(self, x, y):
        speedX = self.calcSpeed(x)
        speedY = self.calcSpeed(y)

        print(speedX, speedY)

        self.pwm.setPWM(0, 0, speedX)
        # self.pwm.setPWM(1, 0, speedY)

    def stop(self, channel):
        self.pwm.setPWM(channel, 0, 0)

    def calcSpeed(self, value):
        if value == 0:
            return 0

        perc = float(abs(value)) / float(self.maxPosition)
        speed = int(self.maxSpeed * perc)
        # print(float(abs(value)) / float(self.maxPosition))
        # print(value, perc, speed)
        if speed < self.minSpeed:
            speed = self.minSpeed
        return speed