from datetime import datetime
import requests
import os
API_URL = ('http://api.openweathermap.org/data/2.5/weather?q={}&mode=json&units=metric&appid={}')
API_7DAY = ('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid={}')
API_KEY = os.environ.get("CITY_WEATHER_KEY")

def query_api(city):
    try: 
        print(API_URL.format(city, API_KEY))
        data = requests.get(API_URL.format(city, API_KEY)).json()
    except Exception as exc:
        print(exc)
        data = None 
    return data

def query_7day(lat, lon):
    try: 
        print(API_7DAY.format(lat, lon, API_KEY))
        data = requests.get(API_7DAY.format(lat, lon, API_KEY)).json()
    except:
        data = None 
    return data