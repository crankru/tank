import RPi.GPIO as GPIO
import time
# import asyncio
# import threading

class DCMotor:
    FORWARD = 1
    BACKWARD = 2
    STOP = 4

    PWM_FREQ = 1000

    speed = None
    direction = None
    thread = None

    def __init__(self, forward_pin, backward_pin):
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin
        self._setup_pin(forward_pin)
        self._setup_pin(backward_pin)

        self.fPwm = GPIO.PWM(self.forward_pin, self.PWM_FREQ)
        self.bPwm = GPIO.PWM(self.backward_pin, self.PWM_FREQ)

    def _setup_pin(self, pin):
        state = GPIO.gpio_function(pin)
        # print(state, GPIO.OUT)
        if state != GPIO.OUT or True: # вот с этой херней надо разобраться
            # print('Set out pin:', pin)
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
            # self._output(self.backward_pin, False)
            self.bPwm.stop()
            self.fPwm.start(self.speed)
            # self._output(self.forward_pin, True)

        elif direction == self.BACKWARD:
            self.direction = self.BACKWARD
            # self._output(self.forward_pin, False)
            self.fPwm.stop()
            self.bPwm.start(self.speed)
            # self._output(self.backward_pin, True)

        elif direction == self.STOP or direction == None:
            self.stop()

        else:
            self.stop()
            print('Error: can`t run to direction', direction)

    def stop(self):
        self.direction = None
        self.fPwm.stop()
        self.bPwm.stop()
        # GPIO.output(self.backward_pin, GPIO.LOW)
        # GPIO.output(self.backward_pin, GPIO.LOW)

    def setSpeed(self, speed):
        if speed != self.speed:
            self.speed = speed
            if speed == 0:
                self.stop()
            elif self.direction == self.FORWARD:
                self.fPwm.ChangeDutyCycle(self.speed)
            elif self.direction == self.BACKWARD:
                self.fPwm.ChangeDutyCycle(self.speed)
            else:
                print('Error: can`t change speed to direction', self.direction)

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
    left_motor = driver.addMotor(1, 12, 13)
    right_motor = driver.addMotor(2, 18, 19)

    left_motor.stop()
    right_motor.stop()

    left_motor.setSpeed(30)
    right_motor.setSpeed(30)

    left_motor.run(DCMotor.FORWARD)
    right_motor.run(DCMotor.FORWARD)
    time.sleep(2)

    for s in range(20, 100):
        left_motor.setSpeed(s)
        right_motor.setSpeed(s)
        time.sleep(.1)

    left_motor.run(DCMotor.BACKWARD)
    right_motor.run(DCMotor.BACKWARD)
    time.sleep(2)

    left_motor.stop()
    right_motor.stop()

    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(12, GPIO.OUT)
    # p = GPIO.PWM(12, 100)
    # p.start(30)
    # time.sleep(5)
    # p.stop()
