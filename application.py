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
import csv

app = Flask(__name__)

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
    resp = query_api(city)
    if resp['cod'] == 200:
        data.append(resp)
        html = render_template('result.html', data = data)
        print(html)
        return html
    else:
        message = "City not found: " + city 
        return render_template("failure.html", message = message)

if __name__ == '__main__':
    app.run(port=8000, debug=True)

