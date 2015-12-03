# -*- coding: utf-8 -*-
"""
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

"""
import forecastio
import sys
sys.path.append('../OpenStreetMap')
from datetime import date
from datetime import timedelta
from dbConnection import DB
from routeGenerator import string_to_coordinates
from operator import itemgetter

class Weather(object):
    """Implements a class to modify timetables based on weather"""
    # ------------------------------------------------------------
    # Class variables
    # ------------------------------------------------------------
    # Forecastio API Credentials
    apiKey = "664dfbd4b12d75c56aab4503f2ddda01"
    # Uppsala central address
    address = "Kungsgatan"
    # Special weather conditions
    # conditions = ["clear-day", "clear-night", "rain", "snow", "sleet", "wind", "fog", "cloudy", "partly-cloudy-day", "partly-cloudy-night"]
    conditions = ["rain", "snow", "fog", "cloudy", "clear-night"]

    def __init__(self):
        # super(Weather, self).__init__()
        # self.arg = arg
        self.formatBusTrip(self.findTrip(self.getWeather(-1, Weather.address, Weather.apiKey), Weather.conditions))

    def getCoordinates(self, address):
        """Uses the Route Generator to search for an address"""
        coordinates = string_to_coordinates(address)
        return coordinates["latitude"], coordinates["longitude"]

    def callWeatherAPI(self, apiKey, latitude, longitude):
        """Calls API to get weather information"""
        return forecastio.load_forecast(apiKey, latitude, longitude)

    def getWeatherHourly(self, forecast):
        """Returns the weather info on a specific frequency
        A switch statement can be implemented to pass info
        on a specific frequency (hourly, daily, etc).
        """
        return forecast.hourly()

    def setQueryDay(self, days):
        """Depending on how workflow is gonna be, pass days to query as a
        parameter
        """
        return date.today() + timedelta(days)

    def queryWeather(self, date):
        """
        """
        db = DB()
        return db.selectWeather(date)

    def countWeather(self, weather):
        """
        """
        return weather.count()

    def insertWeather(self, address, apiKey, days):
        """Calls API to get weather information
        """
        db = DB()
        coordinates = self.getCoordinates(address)
        forecast = self.getWeatherHourly(self.callWeatherAPI(apiKey, coordinates[0], coordinates[1]))
        for data in forecast.data:
            if data.time.date() == self.setQueryDay(days):
                weather = {'icon': data.icon, 'time': data.time, 'temperature': data.temperature}
                db.insertWeather(weather)

    def getWeather(self, days, address, apiKey):
        """
        """
        if self.countWeather(self.queryWeather(self.setQueryDay(days))) == 0:
            self.insertWeather(address, apiKey, days)
        return self.queryWeather(self.setQueryDay(days))

    def findTrip(self, weather, conditions):
        trip = []
        db = DB()
        # Running trough the weather
        for i in weather:
            # Search for pre defined special weather conditions
            # This can be a function that evaluates temperature and time
            if self.evaluateWeather(i["icon"], i["temperature"], i["time"], conditions):
                # Query related trips between i["time"] and an hour later
                trips = db.selectBusTrip(i["time"])
                # Append them on the trips array
                trip.append([i["icon"], i["temperature"], i["time"], trips])
        # print trip
        return trip

    def evaluateWeather(self, icon, temperature, time, conditions):
        if icon in conditions:
            return True
        else:
            return False

    def formatBusTrip(self, trip):
        busTrip = []
        for i in xrange(len(trip)):
            for j in trip[i][3]:
                busTrip.append([j["line"], j["_id"]])
        busTrip = sorted(busTrip, key=itemgetter(0))
        self.searchTimeTable(busTrip)

    def searchTimeTable(self, busTrip):
        timetable = []
        busId = []
        line = busTrip[0][0]
        busId.append(busTrip[0][1])
        db = DB()
        for i in xrange(1, len(busTrip)):
            if line != busTrip[i][0]:
                timetable = db.selectTimeTablebyBusTrip(busId)
                timetable2 = self.processSomething(timetable, busId)
                db.updateTimetable(timetable2[0], timetable2[1])
                # db.deleteBusTrip(timetable2[1])
                # notifyUsers(timetable2[1])
                busId = []
            line = busTrip[i][0]
            busId.append(busTrip[i][1])
        timetable = db.selectTimeTablebyBusTrip(busId)
        timetable2 = self.processSomething(timetable, busId)
        db.updateTimetable(timetable2[0], timetable2[1])

    def processSomething(self, timetable, busId):
        for t in timetable:
            tt = [t["_id"], self.diff(t["timetable"], busId)]
        return tt

    def diff(self, a, b):
        b = set(b)
        return [aa for aa in a if aa not in b]

    def evaluateTrip(self, trip):
        count = 0
        chromosome = []
        line = None
        db = DB()
        # Loop trough the whole trip structure
        # trip structure: icon, temperature, time and trips cursor
        for i in xrange(len(trip)):
            # Loop trough trips cursor
            # trips cursor: startTime, line and capacity
            for j in trip[i][3]:
                # print j["_id"]
                print j["_id"]
                selectTimeTablebyBusTrip
                for reg in db.selectTimeTablebyBusTrip([j["_id"]]):
                    print reg
                    print "======"
                '''
                if line is None:
                    line = j["line"]
                    startTime = j["startTime"]
                    capacity = j["capacity"]
                if line != j["line"]:
                    # Divided 60 by that number  to get frequency
                    if trip[i][0] in Weather.conditions:
                        # Calculate frequency on that hour
                        frequency = int(round(60/count))
                        # Change the frequency of the buses
                        # >> freq, less buses
                        # << freq, more buses
                        frequency = frequency - 2
                        if frequency < 0:
                            frequency = 5
                    chromosome.append([line, capacity, frequency, startTime])
                    # print j["startTime"], j["line"], j["capacity"]
                    # time = [trip[i][2],
                    startTime = j["startTime"]
                    count = 0
                count = count + 1
                line = j["line"]
                '''
            # print "======"
        # print chromosome

if __name__ == '__main__':
    Weather()
