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
import itertools
from pymongo import MongoClient
from bson.objectid import ObjectId
from operator import itemgetter
import itertools



class DB():
    # DB Credentials
    server = "130.238.15.114"
    port = 27017
    database = "monad"
    timeSeparator = ":"
    minutesDay = 1440
    hoursDay = 24
    minutesHour = 60
    formatTime = '%H:%M'

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
        req = self.db.TravelRequest.find({"StartTime": {"$gte": start, "$lt": end}})
        return req

    def getTravelRequestSummary(self, start, end):
        keyf = "function(doc) { return { startBusStop: doc.startBusStop, hour: doc.startTime.getHours()-2, minute: doc.startTime.getMinutes()};}"
        condition = {"startTime": {"$gte": start, "$lt": end}}
        initial = {"count": 0}
        reduce = "function(curr, result) { result.count++; }"
        # req = self.db.TravelRequest.group(keyf, condition, initial, reduce)
        req = self.db.TravelRequestLookAhead.group(keyf, condition, initial, reduce)
        req = sorted(req, key=itemgetter("hour", "minute"))
        return req

    def getReqStartEndTime(self, start, end):


        # A query is made to group request which have same startBusStop and between specific duration
        # return summary of request
        #pipline = [{"$match": {"startTime": {"$gte": start, "$lt": end}}}]
        pipline = [{"$match": [{"startTime": {"$gte": start, "$lt": end}}]}]

        reqs =[]
        requests = self.db.TravelRequestLookAhead.aggregate(pipline)
        for req in requests:
            reqs.append([req.get('startTime', None), req.get('startBusStop', None), req.get('endBusStop', None)])

        return reqs


    def getTravelRequestBetween(self, start, end):
        requests = self.db.TravelRequestLookAhead.find({"startTime": {"$gte": start, "$lt": end}})
        reqs =[]
        for req in requests:
            reqs.append([req.get('startTime', None), req.get('startBusStop', None), req.get('endBusStop', None)])

        return reqs

    def getTravelRequestSummaryByEndBusStop(self, start, end, endBusStop):

        # A query is made to group request which have same endBusStop and between specific duration
        # return summary of request
        pipline = [{"$match": {"$and": [{"startTime": {"$gte": start, "$lt": end}}, {"endBusStop" : endBusStop}]}},
            {"$group": {"_id": "$endBusStop", "count": {"$sum": 1}}}]

        requestSum = self.db.TravelRequestLookAhead.aggregate(pipline)

        return self.retrieveData(requestSum, 'count')
    def MaxReqNumTrip(self,trip_sTime,end,lineNum = 2):

        #create dic
        BusStplist = []
        dirlist =[]
        #get the trip time table
        t =datetime.datetime.strptime(trip_sTime,'%Y-%m-%d %H:%M:%S').time()
        e =datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S').time()


        trip_time_table = self.generateFitnessTripTimeTable(lineNum,trip_sTime[11:16])
        for i in trip_time_table:
            BusStplist.append([i[0],0])
            dirlist.append(i[0])
        t =datetime.datetime.strptime(trip_sTime,'%Y-%m-%d %H:%M:%S')
        e =datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
        #get all requests where starting t is more than trip starting time
        Requests = self.getTravelRequestBetween(t,e)
       

        #get only the requests with start location in bus stops and end location in bus stps
        counter = 0
        counter2 = 0
        for req in Requests:
            for i in BusStplist:
                if (req[1], req[2]) in itertools.combinations(dirlist, 2):
                    if req[1] == i[0]:
                        i[1] += 1
                        counter +=1
                    if req[2] == i[0]:
                        i[1] += -1
                        counter2 +=1

        sum = 0;
        for i in BusStplist:
            sum += i[1]
            i[1] = sum
        return BusStplist




        # These function will be called for every gene in order to get the difference
        # def getTravelRequestBetween(self, start, end):
        #    for doc in self.db.TravelRequest.find({'time': {'$gte': start, '$lt': end}}):
        #        print doc


    def populateRoute(self, route):
        # route5 = {"line": 5, "durationTime":39, routeStop2}
        # routeStop5 = ["Stenhagenskolan","Herrhagens Byväg","Kiselvägen","Stenhagens Centrum","Stenröset","Stenhällen","Gatstenen","Hedensbergsvägen","Flogsta centrum","Rickomberga","Studentstaden","Ekonomikum","Götgatan","Skolgatan","Stadshuset","Centralstationen","Samariterhemmet","Strandbodgatan","Kungsängsesplanaden","Vimpelgatan","Lilla Ultuna","Kuggebro","Vilan","Nämndemansvägen","Lapplandsresan","Ölandsresan","Daneport","Västgötaresan","Gotlandsresan","Smålandsvägen"]
        self.db.Route.insert_one(route)

    def getRouteId(self):
        route = self.db.Route.find().distinct("line")
        return route

    def getRoute(self, column):
        routeId = self.getRouteId()
        for r in routeId:
            route = self.db.Route.find({"line": r})
            return self.retrieveData(route, column)

    def getLine(self, line):
        line = self.db.Route.find({"line": line})
        return self.retrieveData(line, None)

    def dropRoute(self):
        self.db.Route.drop()

    def getTripDay(self, line):
        frequency = self.db.Route.find({"line": line}, {"frequency": 1})
        frequency = self.retrieveData(frequency, "frequency")
        return DB.minutesDay / frequency

    def getRouteStop(self, line):
        routeStop = self.db.Route.find({"line": line}, {"trajectory": 1})
        return self.retrieveData(routeStop, "trajectory")

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
    # Generate TT from seed random starting time. Called when generating the initial population
    def generateStartingTripTime(self, line):
        return list([line, self.generateRandomCapacity(), self.generateTime(self.generateMinute(self.mergeRandomTime(self.getRandomHour(),self.getRandomMinute())))])

    # Fitness trip time table
    # This is the function that changes the genotype into a phenotype. It generates the time table for a particular individual.
    def generateFitnessTripTimeTable(self, line, startingTime):
        tripTimeTable = []
        busStop = self.getRouteStop(line)
        minuteSeed = self.generateMinute(startingTime)
        #minuteSeed =startingTime.minute
        tripTimeTable.append([self.getBusStopName(busStop[0]["busStop"]),self.generateTime(minuteSeed)])
        for j in range(len(busStop)-1):
            minuteSeed = minuteSeed + busStop[j]["interval"]
            if minuteSeed > DB.minutesDay:
                minuteSeed = minuteSeed - DB.minutesDay
            tripTimeTable.append([self.getBusStopName(busStop[j+1]["busStop"]),self.generateTime(minuteSeed)])
        return tripTimeTable

    # After GA, this function is called to generate all the bus stops given the initial starting times based on the best individual
    def generateTripTimeTable(self, timetable):
        timeTable = []
        for i in range(len(timetable)):
            busStop = self.getRouteStop(timetable[i][0])
            numberStop = len(busStop)-1
            # print numberStop
            minuteSeed = self.generateMinute(timetable[i][2])
            tripTimeTable = []
            tripTimeTable.append([busStop[0]["name"],self.generateTime(minuteSeed)])
            for j in range(numberStop):
                minuteSeed = minuteSeed + busStop[j]["interval"]
                if minuteSeed > DB.minutesDay:
                    minuteSeed = minuteSeed - DB.minutesDay
                tripTimeTable.append([busStop[j+1]["name"],self.generateTime(minuteSeed)])
            timeTable.append([timetable[i][0], timetable[i][1], list(self.flatten(tripTimeTable))])
        return sorted(timeTable, key = itemgetter(2))

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
    # This function takes the result from generateTripTimeTable, and generates a JSON document with the DB layout. Then, it proceeds to insert it on the DB.
    def insertTimeTable(self, document):
        timeTable = []
        bus = []
        for i in range(len(document)):
            j = 0
            trip = []
            bus = []
            busId = self.getRandomMinute()
            bus.append(busId)
            # print document[i][2]
            for j in range(len(document[i][2])/2):
                ind = j * 2
                if len(document[i][2][ind+1]) < 5:
                    print (document[i][2][ind+1])
                trip.append({"busStop": document[i][2][ind], "time": datetime.datetime.strptime(document[i][2][ind+1], DB.formatTime), "capacity": document[i][1], "latitude": self.getBusStopLatitude(document[i][2][ind]), "longitude": self.getBusStopLongitude(document[i][2][ind])})
            timeTable.append({"busId": bus, "busStops": trip})
        self.db.timeTable.insert_one({"line": document[0][0], "date": datetime.datetime.now(), "timetable": timeTable})


    def getRequestsFromDB(self,start,end):
        reqs = []
        requests = self.db.TravelRequestLookAhead.find({"$and": [{"startTime": {"$gte": start}}, {"startTime": {"$lt": end}}]}, {"startTime": 1, "startBusStop": 1, "endBusStop": 1, "_id": 0})  # New collection for LookAhead
        for req in requests:
            reqs.append([req.get('startTime', None), req.get('startBusStop', None), req.get('endBusStop', None)])

        return reqs   

    # Bus Stop Location
    def getBusStopLatitude(self, busStop):
        return self.retrieveData(self.db.BusStop.find({"name": busStop}, {"latitude": 1}), "latitude")

    def getBusStopLongitude(self, busStop):
        return self.retrieveData(self.db.BusStop.find({"name": busStop}, {"longitude": 1}), "longitude")

    def getBusStopId(self, busStop):
        return self.retrieveData(self.db.BusStop.find({"name": busStop}), "_id")

    def getBusStopName(self, id):
        return self.retrieveData(self.db.BusStop.find({"_id": id}), "name")

    def MaxReqNumTrip(self,trip_sTime,tripEnd, lineNum = 2):

        BusStplist = []
        dirlist =[]
        t =datetime.datetime.strptime(trip_sTime,'%Y-%m-%d %H:%M:%S').time()
        e =datetime.datetime.strptime(tripEnd,'%Y-%m-%d %H:%M:%S').time()
        #get the trip time table
        trip_time_table = self.generateFitnessTripTimeTable(lineNum,trip_sTime[11:16])
        for i in trip_time_table:
            BusStplist.append([i[0],0])
            dirlist.append(i[0])
        t = datetime.datetime.strptime(trip_sTime,'%Y-%m-%d %H:%M:%S')
        e =datetime.datetime.strptime(tripEnd,'%Y-%m-%d %H:%M:%S')

        #get all requests where starting time is more than trip starting time
        Requests = self.getRequestsFromDB(t, e)

        #get only the requests with start location in bus stops and end location in bus stps
        for req in Requests:
            for i in BusStplist:
                if (req[1], req[2]) in itertools.combinations(dirlist, 2):
                    if req[1] == i[0]:
                        i[1] += 1
                    if req[2] == i[0]:
                        i[1] += -1

        sum = 0;
        for i in BusStplist:
            sum += i[1]
            i[1] = sum
        return BusStplist

