#!/usr/bin/env python
# -*- coding: utf-8 -*-

#import RPi.GPIO as GPIO
import threading
import time
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

    def bits_from_int(x):
        a_bit = x & 1
        b_bit = x & 2
        c_bit = x & 4
        return (a_bit, b_bit, c_bit)

    def set_row(row):
#        #time.sleep(delay)
        a_bit, b_bit, c_bit = bits_from_int(row)
#        GPIO.output(a_pin, a_bit)
#        GPIO.output(b_pin, b_bit)
#        GPIO.output(c_pin, c_bit)
#        #time.sleep(delay)

    def set_color_top(color):
#        #time.sleep(delay)
        red, green, blue = bits_from_int(color)
#        GPIO.output(red1_pin, red)
#        GPIO.output(green1_pin, green)
#        GPIO.output(blue1_pin, blue)
#        #time.sleep(delay)
     
    def set_color_bottom(color):
#        #time.sleep(delay)
        red, green, blue = bits_from_int(color)
#        GPIO.output(red2_pin, red)
#        GPIO.output(green2_pin, green)
#        GPIO.output(blue2_pin, blue)
#        #time.sleep(delay)

    def clock():
#        GPIO.output(clock_pin, 1)
#        GPIO.output(clock_pin, 0)
        print "clock"
     
    def latch():
#        GPIO.output(latch_pin, 1)
#        GPIO.output(latch_pin, 0)
        print "latch"

    def set_pixel(self, x, y, color):
        self.screen[y][x] = color

    # LEDの表示リフレッシュ
    def refresh():
        # 上下８行ずつに分けて出力する
        for row in range(8):
#            GPIO.output(oe_pin, 1)
            set_color_top(0)
            set_row(row)
            #time.sleep(delay)
            for col in range(32):
                set_color_top(screen[row][col])
                set_color_bottom(screen[row+8][col])
                clock()
            #GPIO.output(oe_pin, 0)
            latch()
#            GPIO.output(oe_pin, 0)
            time.sleep(delay)

# LED表示スレッド
rlock = threading.RLock()
class LedThread(threading.Thread):
    def __init__(self):
        print "LedThread.init"
        threading.Thread.__init__(self)

        self.led = MatrixLED()
        self.running = True

    def run(self):
        print "LedThread.run"

        while self.running:
            rlock.acquire()

            self.led.refresh
#            time.sleep(0.005)
            rlock.release
            
    def stop(self):
        self.running = False
        print "stop"

    def display_date(self, month, day):
        # 日付mm.ddの表示
        rlock.acquire()

        bitmap = BitmapNumber()

        left = 0
        top = 11
        
        offset = (left, top)
        number = bitmap.bit_of_number(month)
        left += len(number) - 1
        for y in range(len(number)):
            for x in range(len(number[y])):
                self.led.set_pixel(offset[0] + x, offset[1] + y, number[y][x])

        offset = (left, top)
        number = bitmap.bit_of_number(month)
        left += len(number) - 1
        for y in range(len(number)):
            for x in range(len(number[y])):
                self.led.set_pixel(offset[0] + x, offset[1] + y, number[y][x])

        offset = (left, 15)
        left += 2
        self.led.set_pixel(offset[0] + 0, offset[1] + 0, 1)

        offset = (left, top)
        number = bitmap.bit_of_number(day)
        left += len(number) - 1
        for y in range(len(number)):
            for x in range(len(number[y])):
                self.led.set_pixel(offset[0] + x, offset[1] + y, number[y][x])

        offset = (left, top)
        number = bitmap.bit_of_number(day)
        left += len(number) - 1
        for y in range(len(number)):
            for x in range(len(number[y])):
                self.led.set_pixel(offset[0] + x, offset[1] + y, number[y][x])

        rlock.release()

        # Matrixのbitをコンソールに表示
        print "LedThread.display_date"
        screen = self.led.screen
        for row in range(len(screen)):
            print screen[row]

class Display
    def __init__(self):
        print "Display.init"

        self.led = MatrixLED()

    def display_date(self, month, day):
        # 日付mm.ddの表示
        rlock.acquire()

        bitmap = BitmapNumber()

        left = 0
        top = 11
        
        offset = (left, top)
        number = bitmap.bit_of_number(month)
        left += len(number) - 1
        for y in range(len(number)):
            for x in range(len(number[y])):
                self.led.set_pixel(offset[0] + x, offset[1] + y, number[y][x])

        offset = (left, top)
        number = bitmap.bit_of_number(month)
        left += len(number) - 1
        for y in range(len(number)):
            for x in range(len(number[y])):
                self.led.set_pixel(offset[0] + x, offset[1] + y, number[y][x])

        offset = (left, 15)
        left += 2
        self.led.set_pixel(offset[0] + 0, offset[1] + 0, 1)

        offset = (left, top)
        number = bitmap.bit_of_number(day)
        left += len(number) - 1
        for y in range(len(number)):
            for x in range(len(number[y])):
                self.led.set_pixel(offset[0] + x, offset[1] + y, number[y][x])

        offset = (left, top)
        number = bitmap.bit_of_number(day)
        left += len(number) - 1
        for y in range(len(number)):
            for x in range(len(number[y])):
                self.led.set_pixel(offset[0] + x, offset[1] + y, number[y][x])

        rlock.release()

        # Matrixのbitをコンソールに表示
        print "LedThread.display_date"
        screen = self.led.screen
        for row in range(len(screen)):
            print screen[row]

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

    def bit_of_number(self, no):
        return self.bitmap[no]


if __name__ == "__main__":

    # LEDの表示をスタート
    led = MatrixLED()
    try:
        while True:
            led.display_date(0, 1)

    except KeyboardInterrupt:
        print '\nKeyboard Interrupt'

    led.stop()
    led.join()

#    GPIO.cleanup()
