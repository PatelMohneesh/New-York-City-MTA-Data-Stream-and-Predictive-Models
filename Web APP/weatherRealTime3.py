import json
import time
from datetime import datetime
from urllib.request import urlopen

api = 'KEY'
url = "http://api.wunderground.com/api/" + api + "/conditions/q/NY/New_York_City.json"

def formatData(data):
    keys = ['temp_c', 'temp_f', 'weather']
    observations = data.get('current_observation')
    cleanData = {x: observations[x] for x in keys if x in observations}
    return cleanData

def classifyWeather(cleanData):
    formattedData = {}
    weather = cleanData.get("weather")
    rain = 0
    snow = 0
    if (weather == "Light Rain"):
        rain = 1
    elif (weather == "Rain"):
        rain = 1
    elif (weather == "Heavy Rain"):
        rain = 1
    elif (weather == "Light Snow"):
        snow = 1
    elif (weather == "Snow"):
        snow = 1
    elif (weather == "Heavy Snow"):
        snow = 1
    formattedData["rain"] = rain
    formattedData["snow"] = snow
    formattedData["tempi"] = cleanData.get("temp_f")
    formattedData["tempm"] = cleanData.get("temp_c")
    return formattedData

def getCurrentWeather():
    response = urlopen(url).read().decode('utf8')
    data = json.loads(response)
    cleanData = formatData(data)
    formattedData = classifyWeather(cleanData)
    return formattedData
