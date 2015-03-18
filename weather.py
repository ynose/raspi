#coding:utf-8

import sys
import urllib
import json

import threading
import time
import datetime


def getWeather():
    json_str = livedoor_weather_api()
    livedoor_weather_json(json_str)
    

def livedoor_weather_api():
    print " === start sub thread (livedoor_weather_api) === "
    
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=120010'

    #print url + params
    response = urllib.urlopen(url)
    return response.read()
    
def livedoor_weather_json(s):
    print " === start sub thread (livedoor_weather_json) === "

    item_list = json.loads(s)
    
    # 場所名
    print urllib.unquote(item_list["title"].encode('utf8'))
    # 今日[0]
    forecasts_today = item_list["forecasts"][0]
    print urllib.unquote(forecasts_today['dateLabel'].encode('utf8') + forecasts_today['date'].encode('utf8'))
    print urllib.unquote(forecasts_today['telop'].encode('utf8'))
    # 最高気温
    temperature_max = "--"
    if forecasts_today['temperature']['max'] is not None:
        temperature_max = urllib.unquote(forecasts_today['temperature']['max']['celsius'].encode('utf8'))

    # 最低気温
    temperature_min = "--"
    if forecasts_today['temperature']['min'] is not None:
        temperature_min = urllib.unquote(forecasts_today['temperature']['min']['celsius'].encode('utf8'))

    print urllib.unquote(temperature_max + "/" + temperature_min) + "℃"

    print ""
        
    # 明日[1]
    forecasts_tomorrow = item_list["forecasts"][1]
    print urllib.unquote(forecasts_tomorrow['dateLabel'].encode('utf8') + forecasts_tomorrow['date'].encode('utf8'))
    print urllib.unquote(forecasts_tomorrow['telop'].encode('utf8'))
    # 最高気温
    temperature_max = "--"
    if forecasts_tomorrow['temperature']['max'] is not None:
        temperature_max = urllib.unquote(forecasts_tomorrow['temperature']['max']['celsius'].encode('utf8'))

    # 最低気温
    temperature_min = "--"
    if forecasts_tomorrow['temperature']['min'] is not None:
        temperature_min = urllib.unquote(forecasts_tomorrow['temperature']['min']['celsius'].encode('utf8'))
        
    print urllib.unquote(temperature_max + "/" + temperature_min) + "℃"

if __name__ == '__main__':
    th = threading.Thread(target=getWeather)
    th.setDaemon(True)  # Trueでメインスレッドが終了したらサブスレッドも終了させる
    th.start()    
    
    try:
        print " === start main thread (main) === "
        while True:
            time.sleep(1)
            print "main thread : " + str(datetime.datetime.today())
        print " === end main thread (main) === "
    except KeyboardInterrupt:
        pass

