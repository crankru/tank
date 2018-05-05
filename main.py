from driver.Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from RobotMove import RobotMove
from config import * # BLYNK_AUTH and etc

import BlynkLib
import time
import atexit

mh = Raspi_MotorHAT(addr=0x6F)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
	mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

# create a default object, no changes to I2C address or frequency
# mh = Raspi_MotorHAT(addr=0x6F)

# Initialize Blynk
blynk = BlynkLib.Blynk(BLYNK_AUTH)

RM = RobotMove()

@blynk.VIRTUAL_WRITE(0)
def my_write_handler(value):
    # print('Current V0 value: {}'.format(value))
    RM.setX(value)

@blynk.VIRTUAL_WRITE(1)
def my_write_handler(value):
    # print('Current V1 value: {}'.format(value))
    RM.setY(value)

blynk.run()
