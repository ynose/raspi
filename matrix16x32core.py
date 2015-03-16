#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from datetime import datetime as dt
#import smbus
#import threading

#delay = 0.000001
delay = 0.0001

# GPIO定義
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

# 16x32のスクリーンを定義    
screen = [[0 for x in xrange(32)] for y in xrange(16)]

# GPIOのセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(red1_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green1_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blue1_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(red2_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(green2_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(blue2_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(clock_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(a_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(b_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(c_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(latch_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(oe_pin, GPIO.OUT, initial=GPIO.LOW)

def bits_from_int(x):
    a_bit = x & 1
    b_bit = x & 2
    c_bit = x & 4
    return (a_bit, b_bit, c_bit)

def set_row(row):
    #time.sleep(delay)
    a_bit, b_bit, c_bit = bits_from_int(row)
    GPIO.output(a_pin, a_bit)
    GPIO.output(b_pin, b_bit)
    GPIO.output(c_pin, c_bit)
    #time.sleep(delay)

def set_color_top(color):
    #time.sleep(delay)
    red, green, blue = bits_from_int(color)
    GPIO.output(red1_pin, red)
    GPIO.output(green1_pin, green)
    GPIO.output(blue1_pin, blue)
    #time.sleep(delay)
 
def set_color_bottom(color):
    #time.sleep(delay)
    red, green, blue = bits_from_int(color)
    GPIO.output(red2_pin, red)
    GPIO.output(green2_pin, green)
    GPIO.output(blue2_pin, blue)
    #time.sleep(delay)

def clock():
    GPIO.output(clock_pin, 1)
    GPIO.output(clock_pin, 0)
    return
 
def latch():
    GPIO.output(latch_pin, 1)
    GPIO.output(latch_pin, 0)
    return

def set_pixel(x, y, color):
     screen[y][x] = color

# LEDの表示リフレッシュ
def refresh():
    # 上下８行ずつに分けて出力する
    for row in range(8):
        GPIO.output(oe_pin, 1)
        set_color_top(0)
        set_row(row)
        for col in range(32):
            set_color_top(screen[row][col])
            set_color_bottom(screen[row+8][col])
            clock()
        #GPIO.output(oe_pin, 0)
        latch()
        GPIO.output(oe_pin, 0)
        time.sleep(delay)

        # Matrixのbitをコンソールに表示
#         print "MatrixLED.refresh"
#         for row in range(len(screen)):
#             print screen[row]


class Display:
    def set_pixels(self, left, top, pixel):
        for y in range(len(pixel)):
            for x in range(len(pixel[y])):
                set_pixel(left + x, top + y, pixel[y][x])
        left += len(pixel[0])
        return left

    # 天気予報の表示
    def display_weather(self, left, top, weather):
        bitmap = BitmapWeather()
        
        pixel = bitmap.bit_of_weather(weather)
        left = self.set_pixels(left, top, pixel)
    
        pixel = bitmap.bit_of_weather(weather+1)
        left = self.set_pixels(left, top, pixel)

        pixel = bitmap.bit_of_weather(weather+2)
        left = self.set_pixels(left, top, pixel)
    

    # 日付の表示
    def display_date(self, left, top, datetime):
#        print datetime.strftime('%y.%m.%d')
        
        month = datetime.strftime('%m')     # mmの2桁
        day = datetime.strftime('%d')       # ddの2桁
        weekday = datetime.isoweekday()

        bitmap = BitmapNumber()

        # m
        if month[0:1] != '0':
            pixel = bitmap.bit_of_number(month[0:1])
        else:
            pixel = bitmap.bit_of_blank()
        left = self.set_pixels(left, top, pixel)

        # m
        pixel = bitmap.bit_of_number(month[1:2])
        left = self.set_pixels(left, top, pixel)

        # .
        pixel = bitmap.bit_of_dot()
        left = self.set_pixels(left, top, pixel)

        # d
        if day[0:1] != '0':
            pixel = bitmap.bit_of_number(day[0:1])
        else:
            pixel = bitmap.bit_of_blank()
        left = self.set_pixels(left, top, pixel)

        # d
        pixel = bitmap.bit_of_number(day[1:2])
        left = self.set_pixels(left, top, pixel)

        # weekday
        bitmap = BitmapWeekday()

        pixel = bitmap.bit_of_weekday(weekday)
        left = self.set_pixels(left, top, pixel)


    # 時刻の表示
    def display_time(self, left, top, datetime):
#        print datetime.strftime('%H:%M:%S')
        
        hour = datetime.strftime('%H')      # HHの2桁
        minute = datetime.strftime('%M')    # MMの2桁
        second = datetime.strftime('%S')    # SSの2桁

        bitmap = BitmapNumber()

        # H
        if hour[0:1] != '0':
            pixel = bitmap.bit_of_number(hour[0:1])
        else:
            pixel = bitmap.bit_of_blank()
        left = self.set_pixels(left, top, pixel)

        # H
        pixel = bitmap.bit_of_number(hour[1:2])
        left = self.set_pixels(left, top, pixel)

        # :
 #       if int(second) % 2 == 0:
        pixel = bitmap.bit_of_colon()
 #       else:
 #           pixel = bitmap.bit_of_blank_half()
        left = self.set_pixels(left, top, pixel)

        # M
        pixel = bitmap.bit_of_number(minute[0:1])
        left = self.set_pixels(left, top, pixel)

        # M
        pixel = bitmap.bit_of_number(minute[1:2])
        left = self.set_pixels(left, top, pixel)

        # :
#        if int(second) % 2 == 0:
        pixel = bitmap.bit_of_colon()
#        else:
#            pixel = bitmap.bit_of_blank_half()
        left = self.set_pixels(left, top, pixel)

        # S
        pixel = bitmap.bit_of_number(second[0:1])
        left = self.set_pixels(left, top, pixel)

        # S
        pixel = bitmap.bit_of_number(second[1:2])
        left = self.set_pixels(left, top, pixel)

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

        self.bitmap[2] = ((1,1,0,0),
                          (0,0,1,0),
                          (0,1,0,0),
                          (1,0,0,0),
                          (1,1,1,0))

        self.bitmap[3] = ((1,1,0,0),
                          (0,0,1,0),
                          (1,1,0,0),
                          (0,0,1,0),
                          (1,1,0,0))

        self.bitmap[4] = ((0,1,0,0),
                          (1,1,0,0),
                          (1,1,1,0),
                          (0,1,0,0),
                          (0,1,0,0))

        self.bitmap[5] = ((1,1,1,0),
                          (1,0,0,0),
                          (1,1,0,0),
                          (0,0,1,0),
                          (1,1,0,0))

        self.bitmap[6] = ((0,1,1,0),
                          (1,0,0,0),
                          (1,1,1,0),
                          (1,0,1,0),
                          (0,1,0,0))

        self.bitmap[7] = ((1,1,1,0),
                          (0,0,1,0),
                          (0,1,0,0),
                          (0,1,0,0),
                          (0,1,0,0))

        self.bitmap[8] = ((1,1,1,0),
                          (1,0,1,0),
                          (0,1,0,0),
                          (1,0,1,0),
                          (1,1,1,0))

        self.bitmap[9] = ((0,1,0,0),
                          (1,0,1,0),
                          (1,1,1,0),
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

    def bit_of_blank_half(self):
        return ((0,0),
                (0,0),
                (0,0),
                (0,0),
                (0,0))

    def bit_of_dot(self):
        return ((0,0),
                (0,0),
                (0,0),
                (0,0),
                (1,0))

    def bit_of_colon(self):
        return ((0,0),
                (1,0),
                (0,0),
                (1,0),
                (0,0))

# 曜日のビットマップ定義クラス
class BitmapWeekday:
    def __init__(self):
        self.bitmap = [1 for x in range(8)] # 0で初期化された配列を作る

        self.bitmap[1] = ((0,1,1,1,1),
                          (0,1,0,0,1),
                          (0,1,1,1,1),
                          (0,1,0,0,1),
                          (1,0,0,1,1))

        self.bitmap[2] = ((0,0,1,0,0),
                          (1,0,1,0,1),
                          (1,0,1,0,1),
                          (0,0,1,0,0),
                          (1,1,0,1,1))

        self.bitmap[3] = ((0,0,1,0,0),
                          (1,1,1,0,1),
                          (0,1,1,1,0),
                          (1,0,1,0,1),
                          (0,1,1,0,0))

        self.bitmap[4] = ((0,0,1,0,0),
                          (1,1,1,1,1),
                          (0,1,1,1,0),
                          (1,0,1,0,1),
                          (0,0,1,0,0))

        self.bitmap[5] = ((0,0,1,0,0),
                          (0,1,1,1,0),
                          (1,0,1,0,1),
                          (0,1,1,1,0),
                          (1,1,1,1,1))

        self.bitmap[6] = ((0,0,1,0,0),
                          (0,0,1,0,0),
                          (0,1,1,1,0),
                          (0,0,1,0,0),
                          (1,1,1,1,1))

        self.bitmap[7] = ((0,1,1,1,1),
                          (0,1,0,0,1),
                          (0,1,1,1,1),
                          (0,1,0,0,1),
                          (0,1,1,1,1))

    def bit_of_weekday(self, no):
        return self.bitmap[int(no)]


# 天気のビットマップ定義クラス
class BitmapWeather:
    def __init__(self):
        self.bitmap = [0 for x in range(3)] # 0で初期化された配列を作る

        self.bitmap[0] = ((0,0,0,0,1,0,0,0),
                          (0,0,1,0,1,0,1,0),
                          (0,0,0,1,1,1,0,0), 
                          (0,1,1,1,1,1,1,1),
                          (0,0,0,1,1,1,0,0),
                          (0,0,1,0,1,0,1,0), 
                          (0,0,0,0,1,0,0,0))

        self.bitmap[1] = ((0,0,0,0,1,0,0,0),
                          (0,0,1,1,1,1,1,0),
                          (0,1,1,1,1,1,1,1), 
                          (0,1,1,1,1,1,1,1),
                          (0,0,0,0,1,0,0,0),
                          (0,0,1,0,1,0,0,0), 
                          (0,0,0,1,1,0,0,0))

        self.bitmap[2] = ((0,0,0,0,0,0,0,0),
                          (0,0,0,1,1,0,0,0),
                          (0,0,1,0,0,1,0,0), 
                          (0,1,0,0,1,1,1,0),
                          (0,1,0,1,0,0,1,1),
                          (0,1,0,0,0,0,0,1), 
                          (0,0,1,1,1,1,1,0))

    def bit_of_weather(self, no):
        return self.bitmap[int(no)]


if __name__ == "__main__":

    # LEDの表示をスタート
    display = Display()
    try:
        # 天気を表示
        display.display_weather(0, 0, 0)
        
        # 日付を表示
        datetime = dt.today()
        display.display_date(0, 11, datetime)
        while True:
            #if datetime.strftime('%S') != dt.today().strftime('%S'):
            #   # 日付も変わっていたら更新する
            if datetime.strftime('%d') != dt.today().strftime('%d'):
                display.display_date(0, 11, datetime)

                # 1秒ごとに時刻表示を更新する
                #display.display_time(2, 10, datetime)
                
                datetime = dt.today()
                
            # リフレッシュ
            refresh()

    except KeyboardInterrupt:
        print '\nKeyboard Interrupt'

    GPIO.cleanup()
