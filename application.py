# mkdir weather-app
# virtual venv
# call venv\Scripts\activate.bat (same as source for Linux)
# pip install Flask
# ...and other needed dependencies ...
# set FLASK_APP=main.py
# flask run --reload

from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from weather import query_api
from datetime import datetime
import csv

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
# see https://roadmap.sh/guides/http-caching
# see https://pythonise.com/series/learning-flask/python-before-after-request
@app.after_request
def after_request(response):
    # Cache-Control specifies how long and in what manner should the content be cached. 
    # no-store specifies that the content is not to be cached by any of the caches
    # (public, private, server)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    # how long a cache content should be considered fresh? never.
    response.headers["Expires"] = 0
    # stops the response from being cached. It might not necessarily work.
    # Pre HTPP/1.1
    response.headers["Pragma"] = "no-cache"
    return response

WORDS = []
COUNTRIES = []

with open("cities/archive/world-cities-sorted.csv", "r", newline="", encoding='utf-8') as csv_file:
    # fieldnames: name,country,subcountry, geonameid
    csv_reader = csv.DictReader(csv_file)
    # reads all lines in the file into a list of lines
    for row in csv_reader:
        city = row['name']
        country = row['country']
        subcountry = row['subcountry']
        geoid = row['geonameid']
        WORDS.append({'name':city, 'country':country, 
                      'subcountry': subcountry, 'id':geoid})

with open("countries/archive/country-codes.csv", "r", newline="", encoding='utf-8') as csv_file:
    # fieldnames: Name, Code
    csv_reader = csv.DictReader(csv_file)
    # reads all lines in the file into a list of lines
    for row in csv_reader:
        country = row['Name']
        code = row['Code']
        COUNTRIES.append({'country':country, 'code':code})

@app.route('/')
def index():
    return render_template('weather.html', data=COUNTRIES) 
     
@app.route("/search/<string:query>")
def search(query):
    # using list comprehension
    # take care of upper and lower case
    # print(query)
    wordList =  [[word['name'],  word['subcountry'], word['country']] 
                 for word in WORDS 
                 if query and word['name'].lower().startswith(query.lower())]
    html = render_template("search.html", words=wordList)
    return html

@app.route('/form/<city>')
@app.route('/form/<city>/<country>', methods = ['get'])
def form(city, country = None):
    data = []
    if country != None:
        city = city + ',' + country
    json_resp = query_api(city)
    pp(json_resp)
    if json_resp['cod'] == 200: # resp != None
        data.append(json_resp)
        weather = {}
        weather['title'] = f"Weather in {json_resp['name']}, {json_resp['sys']['country']}"
        weather['icon'] = json_resp['weather'][0]['icon']
        weather['temp'] = f"{round(json_resp['main']['temp'])}°C"
        weather['min_temp'] = f"{round(json_resp['main']['temp_min'])}°C"
        weather['max_temp'] = f"{round(json_resp['main']['temp_max'])}°C"
        weather['feels_like'] = f"{round(json_resp['main']['feels_like'])}°C"
        weather['description'] = json_resp['weather'][0]['description']
        weather['humidity'] = f"{json_resp['main']['humidity']} %"
        weather['sunrise'] = datetime.fromtimestamp(json_resp['sys']['sunrise']).strftime("%H:%M")
        weather['sunset'] = datetime.fromtimestamp(json_resp['sys']['sunset']).strftime("%H:%M")
        weather['datetime'] = datetime.fromtimestamp(json_resp['dt']).strftime("%a, %m/%d %H:%M")
        weather['speed'] = f"{round(json_resp['wind']['speed'] * 3.6)} km/h"
        html = render_template('result.html', weather = weather)
        #print(html)
        return html
    else:
        message = "City not found: " + city 
        return render_template("failure.html", message = message)

if __name__ == '__main__':
    app.run(port=8000, debug=True)

