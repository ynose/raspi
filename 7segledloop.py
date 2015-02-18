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

GPIO.setup(8, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH)

try:
    while True:
        GPIO.output(4,  GPIO.HIGH)  # A
        GPIO.output(17, GPIO.HIGH)  # B
        GPIO.output(27, GPIO.HIGH)  # C
        GPIO.output(23, GPIO.LOW)  # E
        GPIO.output(24, GPIO.LOW)  # F
        GPIO.output(8, GPIO.LOW)    # Switch    10-ON
        GPIO.output(11, GPIO.HIGH)    # Switch
        sleep(0.01)
        
        GPIO.output(4,  GPIO.LOW)  # A
        GPIO.output(17, GPIO.LOW)  # B
        GPIO.output(27, GPIO.LOW)  # C
        GPIO.output(23, GPIO.HIGH)  # E
        GPIO.output(24, GPIO.HIGH)  # F
        GPIO.output(8, GPIO.HIGH)   # Switch    1-ON
        GPIO.output(11, GPIO.LOW)   # Switch
        sleep(0.01)

except KeyboardInterrupt:
    pass

GPIO.cleanup()

