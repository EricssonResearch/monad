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
import random
import string
import datetime
import collections
from pymongo import MongoClient
from bson.objectid import ObjectId



class DB():
    # DB Credentials
    server = "130.238.15.114"
    port = 27017
    database = "monad"
    timeSeparator = ":"
    minutesDay = 1440
    hoursDay = 23
    minutesHour = 60

    # Constructor
    def __init__(self):
        self.client = MongoClient(DB.server, DB.port)
        self.db = self.client[DB.database]

    def createCollection(self, name):
        self.db.createCollection(name)
    
    def retrieveData(self, data, column):
        if column is None:
            for document in data:
                return document
        else:
            for document in data:
            	return document[column]
                
    # Travel Requests
    def getTravelRequestCount(self):
        return self.db.TravelRequest.count()

    def getRandomTravelRequestId(self):
        req = self.db.TravelRequest.find()[random.randrange(self.getTravelRequestCount())]
        return req["_id"]

    def getRandomTravelRequest(self, column):
        req = self.db.TravelRequest.find(
            {"_id": ObjectId(self.getRandomTravelRequestId())})

    def getTravelRequest(self, object, column):
        req = self.db.TravelRequest.find({"_id": ObjectId(object)})
        return self.retrieveData(req, column)
        
	# Routes
    def populateRoute(self, route):
        # route5 = {"line": 5, "durationTime":39, routeStop2}
        # routeStop5 = ["Stenhagenskolan","Herrhagens Byväg","Kiselvägen","Stenhagens Centrum","Stenröset","Stenhällen","Gatstenen","Hedensbergsvägen","Flogsta centrum","Rickomberga","Studentstaden","Ekonomikum","Götgatan","Skolgatan","Stadshuset","Centralstationen","Samariterhemmet","Strandbodgatan","Kungsängsesplanaden","Vimpelgatan","Lilla Ultuna","Kuggebro","Vilan","Nämndemansvägen","Lapplandsresan","Ölandsresan","Daneport","Västgötaresan","Gotlandsresan","Smålandsvägen"]
        self.db.route.insert_one(route)

    def getRouteId(self):
        route = self.db.route.find().distinct("line")
        return route

    def getRoute(self, column):
        routeId = self.getRouteId()
        for r in routeId:
            route = self.db.route.find({"line": r})
            return self.retrieveData(route, column)

    def dropRoute(self):
        self.db.route.drop()

    def getTripDay(self, line):
    	tripDay = self.db.route.find( { "line" : line  }, {"tripDay" : 1} )
    	return self.retrieveData(tripDay, "tripDay")
    
    def getRouteStop(self, line):
        routeStop = self.db.route.find( { "line" : line  }, {"stop" : 1} )
    	return self.retrieveData(routeStop, "stop")
    
    # Bus
    # https://www.ul.se/en/About-UL/About-our-public-function/
    # In total we deploy around 125 city buses, 250 regional buses and 11
    # trains.
    def generateRandomText(self, size=3, chars=string.ascii_uppercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def generateRandomNumber(self, size=3, chars=string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def generateRandomCapacity(self):
        capacity = [20, 60, 120]
        return random.choice(capacity)

    def generatePlate(self):
        return self.generateRandomText() + self.generateRandomNumber()

    def dropBusCollection(self):
        self.db.bus.drop()

    def populateBus(self, size):
        for x in range(0, size):
            bus = {"capacity": self.generateRandomCapacity(), "plate": self.generatePlate()}
            bus_id = self.db.bus.insert_one(bus).inserted_id

    def getBusCount(self):
        return self.db.bus.count()

    def getRandomBusId(self):
        bus = self.db.bus.find()[random.randrange(self.getBusCount())]
        return bus["_id"]

    def getRandomBus(self, column):
        bus = self.db.bus.find(
            {"_id": ObjectId(self.getRandomBusId())})
        return self.retrieveData(bus, column)

    # Generate fake time table
    # Let's create a trip every headway minutes
    def setHeadWay(self, line):
        tripDay = int(self.getTripDay(line))
        return DB.minutesDay / tripDay

    def getRandomHour(self):
        return random.randrange(DB.hoursDay)

    def getRandomMinute(self):
        return random.randrange(DB.minutesHour)

    def mergeRandomTime(self,hour,minute):
        return str(hour) + DB.timeSeparator + str(minute)

    def generateMinute(self, time):
        hours, minutes = time.split(DB.timeSeparator)
        if int(hours)==24:
            hours="0"
        return int(hours) * DB.minutesHour + int(minutes)

    def generateTime(self, time):
        hours, minutes = divmod(time, DB.minutesHour)
        if hours==24:
            hours=0
        return self.mergeRandomTime(hours, minutes)

    # Trip
    # Generate TT from seed random starting time
    def generateTripTimeTable(self, line):
        tripTimeTable = []
        seed = self.mergeRandomTime(self.getRandomHour(),self.getRandomMinute())
        busStop = self.getRouteStop(line)
        numberStop = len(busStop)
        minuteSeed = self.generateMinute(seed)
        for i in range(numberStop):
            minuteSeed = minuteSeed + busStop[i][1]
            if minuteSeed > DB.minutesDay:
            	minuteSeed = minuteSeed - DB.minutesDay;
            # tripTimeTable.append([busStop[i][0],self.generateTime(minuteSeed)])
            # tripTimeTable.append([self.generateTime(minuteSeed)])
            tripTimeTable.append(self.generateTime(minuteSeed))
        #print list(self.flatten([self.getRoute("line"),self.getRandomBus("plate"),self.flatten(tripTimeTable)]))
        #return list(self.flatten([self.getRoute("line"),self.getRandomBus("plate"),self.flatten(tripTimeTable)]))
        #print list([self.getRoute("line"),self.getRandomBus("plate"),self.flatten(tripTimeTable)])
        return list(self.flatten([self.getRoute("line"), self.getRandomBus("plate"), list(self.flatten(tripTimeTable))]))

    def generateTimeTable(self, line):
        timeTable = []
        tripDay = int(self.getTripDay(line))
        for i in range(tripDay):
            #timeTable.append([self.getRoute("line"),self.getRandomBus("plate"),self.generateTripTimeTable(self.mergeRandomTime(self.getRandomHour(),self.getRandomMinute()),self.getRouteStop(line))])
            timeTable.append(self.generateTripTimeTable(line))
        print timeTable
        return timeTable
    
    def flatten(self, l):
        for el in l:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in self.flatten(el):
                    yield sub
            else:
                yield el
