import time
from ServoPi import Servo
servo = Servo(0x40)
servo.set_low_limit(0.6)
servo.set_high_limit(2.4)
servo.set_frequency(50)
while True:
    position = int(input('Position:'))
    servo.move(1, position,180)
