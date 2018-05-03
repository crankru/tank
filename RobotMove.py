from driver.Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

class RobotMove:
    def __init__(self):
        self.mh = Raspi_MotorHAT(addr=0x6F)
        self.motorRight = self.mh.getMotor(2)
        self.motorLeft = self.mh.getMotor(1)

        self.maxSpeed = 255
        self.minSpeed = 30

        self.zeroPosition = self._y = self._x = 0
        self.maxPosition = 100

        self.reversTurnValue = 70

    def setX(self, value):
        # print('X: {}'.format(value))
        self._x = int(value)
        self.updateMode()

    def setY(self, value):
        # print('Y: {}'.format(value))
        self._y = int(value)
        self.updateMode()

    def calcSpeed(self, value):
        if value == 0:
            return 0

        perc = float(abs(value)) / float(self.maxPosition)
        speed = int(self.maxSpeed * perc)
        # print(float(abs(value)) / float(self.maxPosition))
        # print(perc, speed)
        if speed < self.minSpeed:
            speed = self.minSpeed
        return speed

    def stop(self):
        # print('STOP')
        self.motorLeft.run(Raspi_MotorHAT.RELEASE)
        self.motorRight.run(Raspi_MotorHAT.RELEASE)

    def run(self):
        speedLeft = self.calcSpeed(self._y)
        speedRight = self.calcSpeed(self._y)
        turnPerc = 1 - (float(abs(self._x)) / float(self.maxPosition))
        # print(turnPerc)

        # move
        if self._y > self.zeroPosition:
            # print('Forvard')
            self.motorRight.run(Raspi_MotorHAT.FORWARD)
            self.motorLeft.run(Raspi_MotorHAT.FORWARD)
        elif self._y < self.zeroPosition:
            # print('Backward')
            self.motorRight.run(Raspi_MotorHAT.BACKWARD)
            self.motorLeft.run(Raspi_MotorHAT.BACKWARD)

        # turn
        if abs(self._x) >= self.reversTurnValue:
            if self._x > 0:
                if self._y > 0:
                    self.motorRight.run(Raspi_MotorHAT.BACKWARD)
                else:
                    self.motorRight.run(Raspi_MotorHAT.FORWARD)
            else:
                if self._y > 0:
                    self.motorLeft.run(Raspi_MotorHAT.BACKWARD)
                else:
                    self.motorLeft.run(Raspi_MotorHAT.FORWARD)

        elif self._x > self.zeroPosition:
            # print('right')
            speedRight = int(speedRight * turnPerc)
        elif self._x < self.zeroPosition:
            # print('left')
            speedLeft = int(speedLeft * turnPerc)

        self.motorLeft.setSpeed(speedLeft)
        self.motorRight.setSpeed(speedRight)

    def updateMode(self):
        if self._x == self.zeroPosition and self._y == self.zeroPosition:
            self.stop()
        else:
            self.run()