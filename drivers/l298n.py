import RPi.GPIO as GPIO
import time

class DCMotor:
    FORWARD = 1
    BACKWARD = 2

    PWM_FREQ = 1000

    speed = None
    direction = None

    def __init__(self, forward_pin, backward_pin):
        # self.forward = GPIO.PWM(forward_pin, 100)
        # self.backward = GPIO.PWN(backward_pin, 100)
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self._setup_pin(forward_pin)
        self._setup_pin(backward_pin)

    def _setup_pin(self, pin):
        state = GPIO.gpio_function(pin)
        # print(state, GPIO.OUT)
        if state != GPIO.OUT or True:
            print('Set out pin:', pin)
            GPIO.setup(pin, GPIO.OUT)

        GPIO.output(pin, GPIO.LOW)

    def _output(self, pin, value):
        if value is True:
            GPIO.output(pin, GPIO.HIGH)
        elif value is False:
            GPIO.output(pin, GPIO.LOW)
        else:
            print('Cann`t set unknown value `{}` to pin `{}`'.format(value, pin))


    def run(self, direction):
        
        if direction == self.FORWARD:
            self.direction = self.FORWARD
            # GPIO.output(self.backward_pin, GPIO.LOW)
            self._output(self.backward_pin, False)
            # self._output(self.forward_pin, True)

            # GPIO.output(self.forward_pin, GPIO.HIGH)
            p = GPIO.PWM(self.forward_pin, self.PWM_FREQ)
            p.ChangeDutyCycle(self.speed)
            # p.start(self.speed)

        elif direction == self.BACKWARD:
            self.direction = self.BACKWARD
            # GPIO.output(self.forward_pin, GPIO.LOW)
            self._output(self.forward_pin, False)
            # self._output(self.backward_pin, True)

            # GPIO.output(self.backward_pin, GPIO.HIGH)
            p = GPIO.PWM(self.backward_pin, self.PWM_FREQ)
            p.ChangeDutyCycle(self.speed)
            # p.start(self.speed)

        else:
            print('Error: unknown direction')

    def stop(self):
        GPIO.output(self.backward_pin, GPIO.LOW)
        GPIO.output(self.backward_pin, GPIO.LOW)
        self.direction = None

    def setSpeed(self, speed):
        if speed != self.speed:
            self.speed = speed

    def __del__(self):
        self.stop()


class MotorDriver:
    motors = dict()

    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    def addMotor(self, index, forward_pin, backward_pin):
        self.motors[index] = DCMotor(forward_pin, backward_pin)
        return self.motors[index]

    def getMotor(self, index):
        return self.motors.get(index)

if __name__ == '__main__':
    driver = MotorDriver()
    left_motor = driver.addMotor(1, 17, 27)
    right_motor = driver.addMotor(2, 22, 10)

    left_motor.setSpeed(100)

    left_motor.run(DCMotor.FORWARD)
    time.sleep(.5)

    left_motor.run(DCMotor.BACKWARD)
    time.sleep(.5)

    left_motor.stop()