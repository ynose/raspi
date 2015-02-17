#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import RPi.GPIO as GPIO
import threading
import time
import socket
 
ledport = (14, 15, 18, 23)
segport = (4, 17, 27, 22, 23, 24, 25, 7)
digit = ((1, 1, 1, 1, 1, 1, 0),     # 0
         (0, 1, 1, 0, 0, 0, 0),     # 1
         (1, 1, 0, 1, 1, 0, 1),     # 2
         (1, 1, 1, 1, 0, 0, 1),     # 3
         (0, 1, 1, 0, 0, 1, 1),     # 4
         (1, 0, 1, 1, 0, 1, 1),     # 5
         (1, 0, 1, 1, 1, 1, 1),     # 6
         (1, 1, 1, 0, 0, 0, 0),     # 7
         (1, 1, 1, 1, 1, 1, 1),     # 8
         (1, 1, 1, 1, 0, 1, 1),     # 9
         (0, 0, 0, 0, 0, 0, 0),     # Blank
         (0, 0, 0, 0, 0, 0, 1))     # Minus
 
class DynamicLed:
    def __init__(self):
        for n in range(8):
            GPIO.setup(segport[n], GPIO.OUT)
            GPIO.output(segport[n], False)
#        for n in range(4):
#            GPIO.setup(ledport[n], GPIO.OUT)
#            GPIO.output(ledport[n], True)
    def set_digit(self, no, num):
        dot = num & 0x80
        num = num & 0x7F
#        if(no == 0):
#            GPIO.output(ledport[3], True)
#        else:
#            GPIO.output(ledport[no - 1], True)
        for n in range(7):
            print segport[n]
            GPIO.output(segport[n], digit[num][n])
        GPIO.output(segport[7], dot)
#        GPIO.output(ledport[no], False)
 
rlock = threading.RLock()
 
class LedThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ss = DynamicLed()
        self.dig = [0, 0, 0, 0]
        self.running = True
    def run(self):
        while self.running:
            rlock.acquire()
#            for n in range(0, 4):
#                self.ss.set_digit(n, self.dig[n])
            self.ss.set_digit(0, self.dig[0])
            time.sleep(0.005)
            rlock.release()
    def stop(self):
        self.running = False
    def set(self, a, b, c, d):
        rlock.acquire()
        self.dig[0] = a
        self.dig[1] = b
        self.dig[2] = c
        self.dig[3] = d
        rlock.release()
    def set_num(self, num, width=0, dot=-1):
        str = '{0:>.{width}f}'.format(num, width=width)
        dp = 0;
        pos = 3;
        rlock.acquire()
        for n in range(len(str) - 1, -1, -1):
            if str[n] == '.':
                dp = 0x80
            elif str[n] == '-':
                self.dig[pos] = 11  # MINUS
                pos = pos - 1
            else:
                self.dig[pos] = int(str[n]) | dp
                dp = 0
                pos = pos - 1
            if pos < 0:
                break
        for n in range(0, pos + 1):
            self.dig[n] = 10    # BLANK
        if dot >= 0:
            self.dig[dot] = self.dig[dot] | 0x80
        rlock.release()
 
if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # get ip address
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.connect(('google.com', 0)) # dummy connect
#     ip = sock.getsockname()[0]
#     sock.close()
#     array = ip.rsplit('.')
    # led thread start
    led = LedThread()
    led.start();
    try:
        while True:
            led.set_num(1, dot=3)
            time.sleep(1)
#             led.set_num(int(array[0]), dot=3)
#             time.sleep(1)
#             led.set_num(int(array[1]), dot=3)
#             time.sleep(1)
#             led.set_num(int(array[2]), dot=3)
#             time.sleep(1)
#             led.set_num(int(array[3]))
#             time.sleep(1)
    except KeyboardInterrupt:
        print '\nbreak'
    led.stop()
    led.join()
    GPIO.cleanup()
