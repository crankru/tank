from drivers.Raspi_PWM_Servo_Driver import PWM
import time

pwm = PWM(0x41)
pwm.setPWMFreq(50)

while(True):
    pwm.setPWM(0, 0, 150)
    time.sleep(1)

    pwm.setPWM(0, 0, 600)
    time.sleep(1)
    break

pwm.setAllPWM(0, 0)
