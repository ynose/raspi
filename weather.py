#coding:utf-8

import sys
import urllib
import json

import threading
import time
import datetime



def getWeather():
    today_date, today_telop, today_temperature_max, today_temperature_min, tomorrow_date, tomorrow_telop, tomorrow_temperature_max, tomorrow_temperature_min = getWeatherData()

    print "today   ：%s %s/%s℃" % (today_telop, today_temperature_max, today_temperature_min)
    
    print "tomorrow：%s %s/%s℃" % (tomorrow_telop, tomorrow_temperature_max, tomorrow_temperature_min)


def getWeatherData():
    json_str = get_weather_json()

    return parse_json(json_str)


def get_weather_json():
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?city=120010'
    print " === urlopen %s ===" % url

    response = urllib.urlopen(url)
    return response.read()


def parse_json(s):
    print " === parse json === "

    item_list = json.loads(s)
    
    # 場所名
    # print urllib.unquote(item_list["title"].encode('utf8'))

    # 今日[0]
    forecasts_today = item_list["forecasts"][0]

    # 日付
    today_date = urllib.unquote(forecasts_today['dateLabel'].encode('utf8') + forecasts_today['date'].encode('utf8'))

    # 天気
    today_telop = urllib.unquote(forecasts_today['telop'].encode('utf8'))

    
    # 最高気温
    today_temperature_max = "--"
    if forecasts_today['temperature']['max'] is not None:
        today_temperature_max = urllib.unquote(forecasts_today['temperature']['max']['celsius'].encode('utf8'))

    # 最低気温
    today_temperature_min = "--"
    if forecasts_today['temperature']['min'] is not None:
        today_temperature_min = urllib.unquote(forecasts_today['temperature']['min']['celsius'].encode('utf8'))


        
    # 明日[1]
    forecasts_tomorrow = item_list["forecasts"][1]

    # 日付
    tomorrow_date = urllib.unquote(forecasts_tomorrow['dateLabel'].encode('utf8') + forecasts_tomorrow['date'].encode('utf8'))

    # 天気
    tomorrow_telop = urllib.unquote(forecasts_tomorrow['telop'].encode('utf8'))


    # 最高気温
    tomorrow_temperature_max = "--"
    if forecasts_tomorrow['temperature']['max'] is not None:
        tomorrow_temperature_max = urllib.unquote(forecasts_tomorrow['temperature']['max']['celsius'].encode('utf8'))

    # 最低気温
    tomorrow_temperature_min = "--"
    if forecasts_tomorrow['temperature']['min'] is not None:
        tomorrow_temperature_min = urllib.unquote(forecasts_tomorrow['temperature']['min']['celsius'].encode('utf8'))
        

    return (today_date, today_telop, today_temperature_max, today_temperature_min, tomorrow_date, tomorrow_telop, tomorrow_temperature_max, tomorrow_temperature_min)


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

