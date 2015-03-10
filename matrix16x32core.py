#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO
import threading
import time
from datetime import datetime as dt
#import smbus

delay = 0.000001

red1_pin = 17
green1_pin = 18
blue1_pin = 22
red2_pin = 23
green2_pin = 24
blue2_pin = 25
clock_pin = 3
a_pin = 7
b_pin = 8
c_pin = 9
latch_pin = 4
oe_pin = 2

# MatrixLED物理制御クラス
class MatrixLED:
    def __init__(self):
        # 16x32のスクリーンを定義    
        self.screen = [[0 for x in xrange(32)] for y in xrange(16)]
        print "MatrixLED.init"

        # GPIOのセットアップ
#        GPIO.setmode(GPIO.BCM)
#        GPIO.setwarnings(False)

#        GPIO.setup(red1_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(green1_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(blue1_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(red2_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(green2_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(blue2_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(clock_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(a_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(b_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(c_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(latch_pin, GPIO.OUT, initial=GPIO.LOW)
#        GPIO.setup(oe_pin, GPIO.OUT, initial=GPIO.LOW)

    def screen():
        return self.sereen

    def bits_from_int(self, x):
        a_bit = x & 1
        b_bit = x & 2
        c_bit = x & 4
        return (a_bit, b_bit, c_bit)

    def set_row(self, row):
#        #time.sleep(delay)
        a_bit, b_bit, c_bit = self.bits_from_int(row)
#        GPIO.output(a_pin, a_bit)
#        GPIO.output(b_pin, b_bit)
#        GPIO.output(c_pin, c_bit)
#        #time.sleep(delay)

    def set_color_top(self, color):
#        #time.sleep(delay)
        red, green, blue = self.bits_from_int(color)
#        GPIO.output(red1_pin, red)
#        GPIO.output(green1_pin, green)
#        GPIO.output(blue1_pin, blue)
#        #time.sleep(delay)
     
    def set_color_bottom(self, color):
#        #time.sleep(delay)
        red, green, blue = self.bits_from_int(color)
#        GPIO.output(red2_pin, red)
#        GPIO.output(green2_pin, green)
#        GPIO.output(blue2_pin, blue)
#        #time.sleep(delay)

    def clock(self):
#        GPIO.output(clock_pin, 1)
#        GPIO.output(clock_pin, 0)
        return
     
    def latch(self):
#        GPIO.output(latch_pin, 1)
#        GPIO.output(latch_pin, 0)
        return

    def set_pixel(self, x, y, color):
        self.screen[y][x] = color

    # LEDの表示リフレッシュ
    def refresh(self):
        # 上下８行ずつに分けて出力する
        for row in range(8):
#            GPIO.output(oe_pin, 1)
            self.set_color_top(0)
            self.set_row(row)
            #time.sleep(delay)
            for col in range(32):
                self.set_color_top(self.screen[row][col])
                self.set_color_bottom(self.screen[row+8][col])
                self.clock()
            #GPIO.output(oe_pin, 0)
            self.latch()
#            GPIO.output(oe_pin, 0)
            time.sleep(delay)

        # Matrixのbitをコンソールに表示
        print "MatrixLED.refresh"
        for row in range(len(self.screen)):
            print self.screen[row]


class Display:
    def __init__(self):
        print "Display.init"

        self.led = MatrixLED()

    def refresh(self):
        self.led.refresh()

    def display_date(self, datetime):
        # 日付mm.ddの表示
        print datetime.strftime('%m.%d')
        month = datetime.strftime('%m')     # mmの2桁
        day = datetime.strftime('%d')       # ddの2桁

        bitmap = BitmapNumber()

        left = 0
        top = 11
        
        # m
        if month[0:1] != '0':
            pixel = bitmap.bit_of_number(month[0:1])
        else:
            pixel = bitmap.bit_of_blank()
        for y in range(len(pixel)):
            for x in range(len(pixel[y])):
                self.led.set_pixel(left + x, top + y, pixel[y][x])
        left += len(pixel) - 1

        # m
        pixel = bitmap.bit_of_number(month[1:2])
        for y in range(len(pixel)):
            for x in range(len(pixel[y])):
                self.led.set_pixel(left + x, top + y, pixel[y][x])
        left += len(pixel) - 1

        # .
        self.led.set_pixel(left, 15, 1)
        left += 2

        # d
        if day[0:1] != '0':
            pixel = bitmap.bit_of_number(day[0:1])
        else:
            pixel = bitmap.bit_of_blank()
        for y in range(len(pixel)):
            for x in range(len(pixel[y])):
                self.led.set_pixel(left + x, top + y, pixel[y][x])
        left += len(pixel) - 1

        # d
        pixel = bitmap.bit_of_number(day[1:2])
        for y in range(len(pixel)):
            for x in range(len(pixel[y])):
                self.led.set_pixel(left + x, top + y, pixel[y][x])
        left += len(pixel) - 1


# 数字のビットマップ定義クラス
class BitmapNumber:
    def __init__(self):
        self.bitmap = [0 for x in range(10)] # 0で初期化された配列を作る

        self.bitmap[0] = ((0,1,0,0),
                          (1,0,1,0),
                          (1,0,1,0),
                          (1,0,1,0),
                          (0,1,0,0))

        self.bitmap[1] = ((0,1,0,0),
                          (1,1,0,0),
                          (0,1,0,0),
                          (0,1,0,0),
                          (1,1,1,0))

        self.bitmap[3] = ((1,1,0,0),
                          (0,0,1,0),
                          (1,1,0,0),
                          (0,0,1,0),
                          (1,1,0,0))

    def bit_of_number(self, no):
        return self.bitmap[int(no)]

    def bit_of_blank(self):
        return ((0,0,0,0),
                (0,0,0,0),
                (0,0,0,0),
                (0,0,0,0),
                (0,0,0,0))

if __name__ == "__main__":

    # LEDの表示をスタート
    display = Display()
    try:
        while True:
            display.display_date(dt.now())
            display.refresh()

    except KeyboardInterrupt:
        print '\nKeyboard Interrupt'

#    GPIO.cleanup()
