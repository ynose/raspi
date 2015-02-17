import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(17, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)

try:
    while True:
        GPIO.output(4,  GPIO.HIGH)  # A
        GPIO.output(17, GPIO.HIGH)  # B
        GPIO.output(27, GPIO.HIGH)  # C
#        GPIO.output(22, GPIO.HIGH)  # D
#         GPIO.output(23, GPIO.HIGH)  # E
#         GPIO.output(24, GPIO.HIGH)  # F
#         GPIO.output(25, GPIO.HIGH)  # G
#        GPIO.output(7,  GPIO.HIGH)  # DP
        sleep(0.5)

except KeyboardInterrupt:
    pass

GPIO.cleanup()

