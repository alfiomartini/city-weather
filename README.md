# Abstract

This web application provides current weather information and a seven day forecast for most cities of the world (with at least 15000 inhabitants). The server side is implemented with _Flask_, a micro web framework written in python. As the user types in the  search input text area, a dynamically built list of cities, whose names start with the user current input text, is shown. This list is built using _jQuery AJAX_ methods. If there are more than one city with the same name, the user has to select the country in order to disambiguate his/her choice. After clicking the search button, the weather forecast html page is rendered in the same initial page. The database of cities and countries are comprised by free _.csv_ files provided by _datahub.io_. Weather data and parameters are collected using the free APIs provided by _openweathermap.org_. The idea to implement this application came after reading _Tristan Ganry's_ article [How to build a web app using Python’s Flask and Google App Engine](http://tiny.cc/6rw8qz).