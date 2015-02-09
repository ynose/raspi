import RPi.GPIO as GPIO
from time import sleep

def my_callback(channel):
    global ledstate
    if channel==24:
        ledstate = not ledstate
        if ledstate == GPIO.HIGH:
            GPIO.output(25, GPIO.HIGH)
        else:
            GPIO.output(25, GPIO.LOW)
        print ledstate

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(24, GPIO.IN,  pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(24, GPIO.RISING, callback=my_callback, bouncetime=200)

ledstate = GPIO.LOW

try:
    while True:
        sleep(0.01)

except Keyboardinterrupt:
    pass

GPIO.cleanup()

