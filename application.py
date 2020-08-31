
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
        message = "Sorry, city not found in the database."
        return render_template("failure.html", message = message)
    lat = city[0]['lat']
    lng = city[0]['lng']
    json_7day = query_7day(lat, lng)
    # print(json_7day)
    if 'current' in json_7day:
        weather = {}
        current = json_7day['current']
        weather['title'] = f"Weather in {city[0]['city']}, {city[0]['country']} ({city[0]['state']})"
        weather['icon'] = current['weather'][0]['icon']
        weather['temp'] = f"{round(current['temp'])}°C"
        weather['feels_like'] = f"{round(current['feels_like'])}°C"
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
        # return render_template('result_page.html', weather = weather, forecast=forecast) 

        # here we return a html snippet that is controlled  by a js script in 'weather.html'
        return render_template('result.html', weather = weather, forecast=forecast)
    else:
        message = "Sorry, there was a problem with your request. Try again."
        return render_template("failure.html", message = message)

if __name__ == '__main__':
    app.run(debug=True)

