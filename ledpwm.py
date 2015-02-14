#!/usr/bin/env python
# _*_ coding: utf-8 _*_

import RPi.GPIO as GPIO
import spidev
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)
p = GPIO.PWM(25, 50)  #GPIO=25, 周波数50Hz
p.start(0)


CE=0

spi = spidev.SpiDev()
spi.open(0,CE)

try:
    while True:
        retspi = spi.xfer2([0x68,0x00])
        value = (retspi[0]*256+retspi[1]) & 0x3ff
        print value
        duty = value*100/1024
        p.ChangeDutyCycle(duty)
        sleep(1)

except KeyboardInterrupt:
  pass

p.stop()
GIPO.claenup()