from drivers.Raspi_PWM_Servo_Driver import PWM
import time

pwm = PWM(0x19)
pwm.setPWMFreq(50)

while(True):
    pwm.setPWM(0, 1, 300)
    pwm.setPWM(1, 1, 500)
    time.sleep(2)

    pwm.setPWM(0, 1, 500)
    pwm.setPWM(1, 1, 300)
    time.sleep(2)

    # break
    # val = int(input('Enter value: '))
    # print(val)
    # pwm.setPWM(0, 0, val)

pwm.setAllPWM(0, 0)
