from datetime import datetime
import requests

'''
http://api.openweathermap.org/data/2.5/weather?q=porto%20alegre,br
&units=metric&mode=jason&APPID=20babcfa6a6caac6dbdf16ff686ce15c

http://api.openweathermap.org/data/2.5/forecast?q=porto%20alegre,br
&units=metric&mode=jason&APPID=20babcfa6a6caac6dbdf16ff686ce15c
'''

# API_KEY = 'fad2198966614566819195135f61530fS'
API_KEY = '20babcfa6a6caac6dbdf16ff686ce15c'
API_URL = ('http://api.openweathermap.org/data/2.5/weather?q={}&mode=json&units=metric&appid={}')
API_7DAY = ('https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&units=metric&appid={}')

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
    except Exception as exc:
        print(exc)
        data = None 
    return data