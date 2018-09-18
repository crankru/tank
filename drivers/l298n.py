import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD)

# GPIO.setup(forward1, GPIO.OUT)
# f1 = GPIO.PWM(forward1, 100)
# f1.ChangeDutyCycle(30)

# time.sleep(.5)
# GPIO.output(forward1, GPIO.LOW)

# GPIO.cleanup()

class DCMotor:
    speed = 0

    def __init__(self, forward_pin, backward_pin):
        # self.forward = GPIO.PWM(forward_pin, 100)
        # self.backward = GPIO.PWN(backward_pin, 100)
        self._setup_pin(forward_pin)

    def _setup_pin(self, pin):
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)

    def run(self):
        pass

    def stop(self):
        pass

    def setSpeed(self, speed):
        self.speed = speed

    def __del__(self):
        pass


class MotorDriver:
    motors = dict()

    def addMotor(self, index, forward_pin, backward_pin):
        self.motors[index] = DCMotor(forward_pin, backward_pin)
        return self.motors[index]

    def getMotor(self, index):
        return self.motors.get(index)

if __name__ == '__main__':
    driver = MotorDriver()
    left_motor = driver.addMotor(1, 4, 17)
    # right_motor = driver.addMotor(27, 22)