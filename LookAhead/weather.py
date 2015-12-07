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
import copy
import sys
sys.path.append('../OpenStreetMap')
from datetime import date
from datetime import timedelta
from dbConnection import DB
from fitness import Fitness
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
        self.processWeather(self.getAffectedTrip(self.getWeather(Weather.address, Weather.apiKey, -4), Weather.conditions))

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
        """ Calls API to get weather information
        """
        db = DB()
        coordinates = self.getCoordinates(address)
        forecast = self.getWeatherHourly(self.callWeatherAPI(apiKey, coordinates[0], coordinates[1]))
        for data in forecast.data:
            if data.time.date() == self.setQueryDay(days):
                weather = {'icon': data.icon, 'time': data.time, 'temperature': data.temperature}
                db.insertWeather(weather)

    def getWeather(self, address, apiKey, days):
        """ This is the function to be called if someone wants to know the weather :D
        """
        if self.countWeather(self.queryWeather(self.setQueryDay(days))) == 0:
            self.insertWeather(address, apiKey, days)
        return self.queryWeather(self.setQueryDay(days))

    def getAffectedTrip(self, weather, conditions):
        """ Looks trips on DB that are gonna be affected by the weather
        """
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
        return trip

    def evaluateWeather(self, icon, temperature, time, conditions):
        """ Evaluates if a result from the weather is part of a 
        special weather condition
        """
        if icon in conditions:
            return True
        else:
            return False

    def processWeather(self, trip):
        """ This functions is like a main process.
        From here, functions to modify the timetable and bustrips are called
        """
        if len(trip) > 0:
            trip2 = copy.deepcopy(trip)
            fitness = Fitness()
            db = DB()
            # Generates new busTrips and updates the timetable
            chromosome = self.generateBusTrip(trip)
            # This function deletes busTrips and references & notifies users
            self.modifyTimeTable(trip2)
            individual = fitness.genTimetable(chromosome)
            db.insertBusTrip2(individual)

    def modifyTimeTable(self, trip):
        timetable = []
        busId = []
        busTrip = []
        db = DB()
        for i in xrange(len(trip)):
            for j in trip[i][3]:
                busTrip.append([j["line"], j["_id"]])
        busTrip = sorted(busTrip, key=itemgetter(0))
        line = busTrip[0][0]
        busId.append(busTrip[0][1])
        for i in xrange(1, len(busTrip)):
            if line != busTrip[i][0]:
                timetable = db.selectTimeTablebyBusTrip(busId)
                newTimetable = self.generateTimetable(timetable, busId)
                db.updateTimetable(newTimetable[0], newTimetable[1], newTimetable[2], newTimetable[3])
                self.deleteBusTrip(newTimetable[3])
                # notifyUsers(timetable2[1])
                busId = []
            line = busTrip[i][0]
            busId.append(busTrip[i][1])
        timetable = db.selectTimeTablebyBusTrip(busId)
        newTimetable = self.generateTimetable(timetable, busId)
        db.updateTimetable(newTimetable[0], newTimetable[1], newTimetable[2], newTimetable[3])
        self.deleteBusTrip(newTimetable[3])
        # notifyUsers(timetable2[1])

    def generateTimetable(self, timetable, busId):
        '''
        '''
        for t in timetable:
            tt = [t["_id"], t["date"], t["line"], self.getArrayDifference(t["timetable"], busId)]
        return tt

    def getArrayDifference(self, a, b):
        '''
        http://stackoverflow.com/questions/6486450/python-compute-list-difference
        b = set(b)
        return [aa for aa in a if aa not in b]
        '''
        b = set(b)
        return [instanceA for instanceA in a if instanceA not in b]


    def deleteBusTrip(self, busTrip):
        db = DB()
        for bt in busTrip:
            db.deleteBusTrip(bt)

    def generateBusTrip(self, trip):
        line = 0
        count = 0
        chromosome = []
        for tripInstance in trip:
            for busInstance in tripInstance[3]:
                if line != busInstance["line"] and count !=0:
                    chromosome.append([line, capacity, self.calculateFrequency(count), startTime])
                    count = 0
                if count == 0:
                    capacity = busInstance["capacity"]
                    startTime = busInstance["startTime"]
                line = busInstance["line"]
                count += 1
        chromosome.append([line, capacity, self.calculateFrequency(count), startTime])
        return chromosome
        '''
        fitness = Fitness()
        db = DB()
        count = 0
        capacity = 0
        startTime = 0
        chromosome = []
        line = None
        # Loop trough the whole trip structure
        # trip structure: icon, temperature, time and trips cursor
        for i in xrange(len(trip)):
            # Loop trough trips cursor
            # trips cursor: startTime, line and capacity
            for j in trip[i][3]:
                if line is None:
                    line = j["line"]
                    startTime = j["startTime"]
                    capacity = j["capacity"]
                if line != j["line"]:
                    chromosome.append([line, capacity, self.calculateFrequency(count), startTime])
                    startTime = j["startTime"]
                    capacity = j["capacity"]
                    count = 0
                count = count + 1
                line = j["line"]
        chromosome.append([line, capacity, self.calculateFrequency(count), startTime])
        # It will generate one chromosome per each bus line
        # As long as the conditions are not good, the frequency
        # will be the same on a particular line
        print chromosome
        # individual = fitness.genTimetable(chromosome)
        # print individual
        # db.insertBusTrip2(individual)  # Increase functionality to update on the timetable
        '''

    def calculateFrequency(self, count):
        minutes = 60
        factor = 2
        minFreq = 10
        # Calculate frequency: divided 60 by count
        frequency = int(round(minutes/count))
        # Change buses frequency: >freq <buses | <freq >buses
        frequency = frequency - factor
        # if frequency <= 0:
        if frequency <= minFreq:
            frequency = minFreq
        return frequency


if __name__ == '__main__':
    Weather()
