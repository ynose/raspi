#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import threading
import time
import socket

# カソード・コモンの7セグLEDに接続されているGPIO番号を定義
# 7セグLEDのセグメントabcdefg+dpのアノードに接続されているGPIO番号
seg_gpio = (4, 17, 27, 22, 10, 9, 11, 7)
# 10の位、1の位の7セグLEDのカソードに接続されているGPIO番号
led_gpio = (14, 15) #, 18, 23)

# 7セグLEDに数字を表現するために点灯させるセグメント(a〜g)の対応表
num_segs = ((1, 1, 1, 1, 1, 1, 0),  # 0
            (0, 1, 1, 0, 0, 0, 0),  # 1
            (1, 1, 0, 1, 1, 0, 1),  # 2
            (1, 1, 1, 1, 0, 0, 1),  # 3
            (0, 1, 1, 0, 0, 1, 1),  # 4
            (1, 0, 1, 1, 0, 1, 1),  # 5
            (1, 0, 1, 1, 1, 1, 1),  # 6
            (1, 1, 1, 0, 0, 0, 0),  # 7
            (1, 1, 1, 1, 1, 1, 1),  # 8
            (1, 1, 1, 1, 0, 1, 1),  # 9
            (0, 0, 0, 0, 0, 0, 0),  # 10(ブランク)
            (0, 0, 0, 0, 0, 0, 1))  # 11(マイナス)

class DynamicLed:
    def __init__(self):
        # 7セグLEDのアノードをLOWに初期化
        for gpio in seg_gpio:
            GPIO.setup(gpio, GPIO.OUT, initial=GPIO.LOW)
        # 7セグLEDのカソードをHIGHに初期化
        for gpio in led_gpio:
            GPIO.setup(gpio, GPIO.OUT, initial=GPIO.HIGH)
    def set_number(self, led, num):
        dot = num & 0x80
        num = num & 0x7F
        
        # 点灯する桁をON
        if(led == 0):
            GPIO.output(led_gpio[1], GPIO.HIGH)
        else:
            GPIO.output(led_gpio[led - 1], GPIO.HIGH)
        # 点灯するセグメントのON/OFF
        for seg in range(7):
            GPIO.output(seg_gpio[seg], num_segs[num][seg])
        GPIO.output(seg_gpio[7], dot)
        # 点灯した桁をOFF
        GPIO.output(led_gpio[led], GPIO.LOW)

rlock = threading.RLock()

class LedThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.ss = DynamicLed()
        self.dig = [0, 0]
        self.running = True
    def run(self):
        while self.running:
            rlock.acquire()
            # 2つのLEDに数字を表示する
            for led in range(0, 2):
                self.ss.set_number(led, self.dig[led])
                time.sleep(0.005)
            rlock.release()
    def stop(self):
        self.running = False
    def set(self, a, b): #, c, d):
        rlock.acquire()
        self.dig[0] = a
        self.dig[1] = b
        #self.dig[2] = c
        #self.dig[3] = d
        rlock.release()
    def display_number(self, number, width=0, dot=-1):
        str = '{0:>.{width}f}'.format(number, width=width)
        dp = 0;
        pos = 1;
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
    GPIO.setmode(GPIO.BCM)  # GPIO番号で指定
    GPIO.setwarnings(False)
    # get ip address
    #sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.connect(('google.com', 0)) # dummy connect
    #ip = sock.getsockname()[0]
    #sock.close()
    #array = ip.rsplit('.')
    # led thread start
    
    # LEDの表示をスタート
    led = LedThread()
    led.start();
    try:
        for number in range(0, 2):
            print(number)
            led.display_number(number)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print '\nbreak'
    led.stop()
    led.join()
    GPIO.cleanup()
