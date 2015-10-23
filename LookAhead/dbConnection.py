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
import collections
import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from operator import itemgetter



class DB():
    # DB Credentials
    server = "130.238.15.114"
    port = 27017
    database = "monad"
    timeSeparator = ":"
    minutesDay = 1440
    hoursDay = 24
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
        return req

    def getTravelRequest(self, column):
        req = self.db.TravelRequestLookAhead.find({}, {"_id": False})
        return self.retrieveData(req, column)

    # These function will be called for every gene in order to get the difference
    def getTravelRequestBetween(self, start, end):
        req = self.db.TravelRequest.find({ "StartTime": {"$gte": start, "$lt": end}})
        return req

    def getTravelRequestSummary(self, start, end):
        keyf = "function(doc) { return { startBusStop: doc.startBusStop, hour: doc.startTime.getHours(), minute: doc.startTime.getMinutes()};}"
        condition = {"startTime": {"$gte": start, "$lt": end}}
        initial = {"count": 0}
        reduce = "function(curr, result) { result.count++; }"
        # req = self.db.TravelRequest.group(keyf, condition, initial, reduce)
        req = self.db.TravelRequestLookAhead.group(keyf, condition, initial, reduce)
        req = sorted(req, key=itemgetter("hour","minute"))
        return req

    def getTravelRequestSummary2(self, start, end, busStop):
        keyf = "function(doc) { return { startBusStop: doc.startBusStop, hour: doc.startTime.getHours(), minute: doc.startTime.getMinutes()};}"
        condition = {"startTime": {"$gte": start, "$lt": end}, "startBusStop": {"$eq": busStop}}
        initial = {"count": 0}
        reduce = "function(curr, result) { result.count++; }"
        # req = self.db.TravelRequest.group(keyf, condition, initial, reduce)
        req = self.db.TravelRequestLookAhead.group(keyf, condition, initial, reduce)
        req = sorted(req, key=itemgetter("hour","minute"))
        return req        

    # These function will be called for every gene in order to get the difference
    # def getTravelRequestBetween(self, start, end):
    #    for doc in self.db.TravelRequest.find({'time': {'$gte': start, '$lt': end}}):
    #        print doc

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
        tripDay = self.db.route.find({"line": line}, {"tripDay": 1})
        return self.retrieveData(tripDay, "tripDay")

    def getRouteStop(self, line):
        routeStop = self.db.route.find({"line": line}, {"stop": 1})
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
            self.db.bus.insert_one(bus)

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

    def mergeRandomTime(self, hour, minute):
        if len(str(hour)) == 1:
            hour = "0" + str(hour)
        if len(str(minute)) == 1:
            minute = "0" + str(minute)
        return str(hour) + DB.timeSeparator + str(minute)

    def generateMinute(self, time):
        hours, minutes = time.split(DB.timeSeparator)
        if int(hours) == 24:
            hours = "0"
        return int(hours) * DB.minutesHour + int(minutes)

    def generateTime(self, time):
        hours, minutes = divmod(time, DB.minutesHour)
        if hours == 24:
            hours = 0
        return self.mergeRandomTime(hours, minutes)

    # Trip
    # Generate TT from seed random starting time
    def generateStartingTripTime(self):
        return list([self.getRoute("line"), self.generateRandomCapacity(), self.generateTime(self.generateMinute(self.mergeRandomTime(self.getRandomHour(),self.getRandomMinute())))])

    def generateFitnessTripTimeTable(self, line, startingTime):
        tripTimeTable = []
        busStop = self.getRouteStop(line)
        minuteSeed = self.generateMinute(startingTime)
        tripTimeTable.append([busStop[0][0],self.generateTime(minuteSeed)])
        for j in range(len(busStop)-1):
            minuteSeed = minuteSeed + busStop[j][1]
            if minuteSeed > DB.minutesDay:
                minuteSeed = minuteSeed - DB.minutesDay
            tripTimeTable.append([busStop[j+1][0],self.generateTime(minuteSeed)])
        return tripTimeTable

    def generateTripTimeTable(self, timetable):
        timeTable = []
        for i in range(len(timetable)):
            busStop = self.getRouteStop(timetable[i][0])
            numberStop = len(busStop)-1
            # print numberStop
            minuteSeed = self.generateMinute(timetable[i][2])
            tripTimeTable = []
            tripTimeTable.append([busStop[0][0],self.generateTime(minuteSeed)])
            for j in range(numberStop):
                minuteSeed = minuteSeed + busStop[j][1]
                if minuteSeed > DB.minutesDay:
                    minuteSeed = minuteSeed - DB.minutesDay
                tripTimeTable.append([busStop[j+1][0],self.generateTime(minuteSeed)])
            timeTable.append([timetable[i][0], timetable[i][1], list(self.flatten(tripTimeTable))])
        return sorted(timeTable, key = itemgetter(2))

    def generateTripTimeTable2(self, line):
        tripTimeTable = []
        seed = self.mergeRandomTime(self.getRandomHour(),self.getRandomMinute())
        busStop = self.getRouteStop(line)
        numberStop = len(busStop)
        minuteSeed = self.generateMinute(seed)
        for i in range(numberStop):
            minuteSeed = minuteSeed + busStop[i][1]
            if minuteSeed > DB.minutesDay:
                minuteSeed = minuteSeed - DB.minutesDay
            tripTimeTable.append(self.generateTime(minuteSeed))
        return list(self.flatten([self.getRoute("line"), self.generateRandomCapacity(), list(self.flatten(tripTimeTable))]))

    def generateTimeTable(self, line):
        timeTable = []
        tripDay = int(self.getTripDay(line))
        for i in range(tripDay):
            timeTable.append(self.generateTripTimeTable(line))
        return timeTable

    # Dont forget to credit this function on Stack Overflow
    # http://stackoverflow.com/questions/14820273/confused-by-chain-enumeration
    def flatten(self, element):
        for el in element:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in self.flatten(el):
                    yield sub
            else:
                yield el

    # Time Table
    def insertTimeTable(self, document):
        timeTable = []
        # route5 = {"line": 5, "durationTime":39, routeStop2}
        # {"line": document[i][0], "date": str(now.strftime("%Y-%m-%d")), "timetable": }
        now = datetime.datetime.now()
        for i in range(len(document)):
            j = 0
            trip = []
            # print document[i][2]
            for j in range(len(document[i][2])/2):
                ind = j * 2
                trip.append({"BusStop": document[i][2][ind],"DptTime": document[i][2][ind+1]})
                # print trip
            timeTable.append({"capacity": document[i][1],"trip": trip})
        # print timeTable
        self.db.timeTable.insert_one({"line": document[0][0], "date": str(now.strftime("%Y-%m-%d")), "timetable": timeTable})


    def getRequestsFromDB(self):
        ''' Gets travel requests from the database. Attempts to cluster the requests based on time 
        and calculates a count of the total requests between a time window.

        @param: start - lower time bound
        @param: end - upper time bound
        @return: total number of requests.
        '''
        reqs = []
        requests = self.db.TravelRequestLookAhead.find()  # New collection for LookAhead
        for req in requests:
            reqs.append(req.get('startTime', None))
        return reqs
