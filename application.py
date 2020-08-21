
# set FLASK_APP=main.py
# flask run --reload

from pprint import pprint as pp
from flask import Flask, flash, redirect, render_template, request, url_for
from weather import query_api, query_7day
from datetime import datetime
import csv
import cs50

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

# WORDS = []
COUNTRIES = []
db = cs50.SQL('sqlite:///database/cities.db')


@app.route('/')
def index():
    return render_template('layout.html') 

@app.route('/spinner')
def spinner():
    return render_template('spinner.html')
     
@app.route("/search/<string:query>")
def search(query):
    # take care of upper and lower case
    query = query.lower() + '%'
    cities = db.execute("""select id, city, country, state from cities
                             where lower(city) like  ?
                             order by city""", (query,))
    html = render_template("search.html", cities=cities)
    return html

@app.route('/city/<int:id>', methods = ['get'])
def city(id):
    city = db.execute('select * from cities where id = ?', (id,))
    if not city:
        message = "City not found: " + city['city']
        return render_template("failure.html", message = message)
    lat = city[0]['lat']
    lng = city[0]['lng']
    json_7day = query_7day(lat, lng)
    if json_7day:
        weather = {}
        current = json_7day['current']
        weather['title'] = f"Weather in {city[0]['city']}, {city[0]['country']} ({city[0]['state']})"
        weather['icon'] = current['weather'][0]['icon']
        weather['temp'] = f"{round(current['temp'])}°C"
        weather['feels_like'] = f"{current['feels_like']}°C"
        weather['description'] = current['weather'][0]['description']
        weather['humidity'] = f"{current['humidity']} %"
        weather['sunrise'] = datetime.fromtimestamp(current['sunrise']).strftime("%H:%M")
        weather['sunset'] = datetime.fromtimestamp(current['sunset']).strftime("%H:%M")
        weather['datetime'] = datetime.now().strftime("%a, %m/%d %H:%M")
        weather['speed'] = f"{round(current['wind_speed'] * 3.6)} km/h"

        forecast = []
        seven_day = json_7day['daily']
        seven_day.pop(0) # remove today's weather
        for day in seven_day:
            wdict = {}
            wdict['icon'] = day['weather'][0]['icon']
            wdict['date'] = datetime.fromtimestamp(day['dt']).strftime("%a %m/%d")
            wdict['temp'] = str(round(day['temp']['day'])) + "°C"
            forecast.append(wdict)
        #  here we have the possibily of the server returns a complete html page
        # this route is set in href attribute of the search item link
        return render_template('result_page.html', weather = weather, forecast=forecast) 

        # here we return a html snippet that is controlled  by a js script in 'weather.html'
        # return render_template('result.html', weather = weather, forecast=forecast)
    else:
        message = "City not found: " + city['city']
        return render_template("failure.html", message = message)

@app.route('/form/<city>')
@app.route('/form/<city>/<country>', methods = ['get'])
def form(city, country = None):
    if country != None:
        city = city + ',' + country
    json_resp = query_api(city)
    #pp(json_resp)
    if json_resp['cod'] == 200: # resp != None
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
        weather['lat'] = json_resp['coord']['lat']
        weather['lon'] = json_resp['coord']['lon']
        forecast = []
        json_7day = query_7day(weather['lat'], weather['lon'])
        if json_7day['daily']:
            seven_day = json_7day['daily']
            seven_day.pop(0)
            for day in seven_day:
                wdict = {}
                wdict['icon'] = day['weather'][0]['icon']
                wdict['date'] = datetime.fromtimestamp(day['dt']).strftime("%a %m/%d")
                wdict['temp'] = str(round(day['temp']['day'])) + "°C"
                forecast.append(wdict)
        #for wdata in forecast:
            #print(wdata['temp'], wdata['icon'], wdata['date'])
        #pp(weather)
        html = render_template('result.html', weather = weather, forecast=forecast)
        # print(html)
        return html
    else:
        message = "City not found: " + city 
        return render_template("failure.html", message = message)

if __name__ == '__main__':
    app.run(debug=True)

