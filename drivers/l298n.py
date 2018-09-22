import RPi.GPIO as GPIO
import time
import asyncio
import threading

class DCMotor:
    FORWARD = 1
    BACKWARD = 2

    PWM_FREQ = 100

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

    def _impulse(self, pin, freq):
        pin.start(freq)
        # time.sleep(.1)
        # await asyncio.sleep(.1)

    def _loop(self, direction, pin):
        print('Start loop', direction, pin)
        while self.direction:
        # while self.direction == direction:            
        # while True:
            if self.direction == self.FORWARD:
                self._impulse(self.fPwm, self.speed)
            elif self.direction == self.BACKWARD:
                self._impulse(self.bPwm, self.speed)
            else:
                print('Error: unknown direction type')

            time.sleep(.1)

        print('End loop', self.direction, direction)

    def run(self, direction):
        # print(self.speed)
        # if direction != self.direction and self.thread:
        #     # print('STOP THREAD')
        #     # if self.thread.is_alive():
        #     #     self.thread.stop()
        #     self.thread = None
        
        if direction == self.FORWARD:
            self.direction = self.FORWARD
            self._output(self.backward_pin, False)
            # self._output(self.forward_pin, True)

            # self._loop(self.FORWARD, self.fPwm)
            if not self.thread:
                self.thread = threading.Thread(target=self._loop, args=(self.FORWARD, self.fPwm))
                self.thread.start()

        elif direction == self.BACKWARD:
            self.direction = self.BACKWARD
            self._output(self.forward_pin, False)
            # self._output(self.backward_pin, True)

            # self._loop(self.BACKWARD, self.bPwm)
            if not self.thread:
                self.thread = threading.Thread(target=self._loop, args=(self.BACKWARD, self.bPwm))
                self.thread.start()

        else:
            print('Error: unknown direction')

    def stop(self):
        self.direction = None
        GPIO.output(self.backward_pin, GPIO.LOW)
        GPIO.output(self.backward_pin, GPIO.LOW)

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
    right_motor = driver.addMotor(2, 22, 13)

    left_motor.stop()
    right_motor.stop()

    left_motor.setSpeed(30)
    right_motor.setSpeed(30)

    left_motor.run(DCMotor.FORWARD)
    right_motor.run(DCMotor.FORWARD)
    time.sleep(2)

    # for s in range(20, 100):
    #     left_motor.setSpeed(s)
    #     right_motor.setSpeed(s)

    left_motor.run(DCMotor.BACKWARD)
    right_motor.run(DCMotor.BACKWARD)
    time.sleep(2)

    left_motor.stop()
    right_motor.stop()