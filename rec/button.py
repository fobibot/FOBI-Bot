import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
PressStatus = False
while True:
    input_state = GPIO.input(14)
    if input_state == False:
        while True:
            input_state = GPIO.input(14)
            print('GetIn')
            if input_state == True:
                break
        print('GetOut')
        time.sleep(0.2)
