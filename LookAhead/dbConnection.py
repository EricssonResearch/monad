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
from datetime import timedelta
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
    formatTime = '%H:%M'

    # Constructor
    def __init__(self):
        self.client = MongoClient(DB.server, DB.port, maxPoolSize=200)
        self.db = self.client[DB.database]

    def createCollection(self, name):
        self.db.createCollection(name)

    def parseData(self, data, column):
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
        return self.parseData(req, column)

    # These function will be called for every gene in order to get the difference
    def getTravelRequestBetween(self, start, end):
        req = self.db.TravelRequest.find({"StartTime": {"$gte": start, "$lt": end}})
        return req

    def getTravelRequestSummary(self, start, end):
        # keyf = "function(doc) { return { startBusStop: doc.startBusStop, hour: doc.startTime.getHours()-2, minute: doc.startTime.getMinutes()};}"
        keyf = "function(doc) { return { startBusStop: doc.startBusStop, hour: doc.startTime.getHours(), minute: doc.startTime.getMinutes()};}"
        condition = {"startTime": {"$gte": start, "$lt": end}}
        initial = {"count": 0}
        reduce = "function(curr, result) { result.count++; }"
        # req = self.db.TravelRequest.group(keyf, condition, initial, reduce)
        req = self.db.TravelRequestLookAhead.group(keyf, condition, initial, reduce)
        req = sorted(req, key=itemgetter("hour", "minute"))
        return req

    def grpReqByBusstopAndTime(self, start, end):
        """
        def getTravelRequestSummary2(self, start, end, busStop):
        keyf = "function(doc) { return { startBusStop: doc.startBusStop, hour: doc.startTime.getHours(), minute: doc.startTime.getMinutes()};}"
        condition = {"startTime": {"$gte": start, "$lt": end}, "startBusStop": {"$eq": busStop}}
        initial = {"count": 0}
        reduce = "function(curr, result) { result.count++; }"
        # req = self.db.TravelRequest.group(keyf, condition, initial, reduce)
        req = self.db.TravelRequestLookAhead.group(keyf, condition, initial, reduce)
        req = sorted(req, key=itemgetter("hour","minute"))

        return req        
        """
        #dataFile = open("/home/ziring/result.txt", "w")
        queryResults = []
        # A query is made to group request made to a busstop and counting the number of similar requests made

        pipline = [{"$match": {"startTime": {"$gte": start, "$lt": end}}},
                   {"$group": {"_id": {"RequestTime": "$startTime", "BusStop": "$startBusStop"}, "total": {"$sum": 1}}},
                   {"$sort": {"_id.RequestTime": 1}}]

        groupQuery = self.db.TravelRequestLookAhead.aggregate(pipline)
        for x in groupQuery:
            queryResults.append(x)
            #dataFile.write(str(x)+'\n'+'\n')

        #dataFile.close()
        return queryResults

    # These function will be called for every gene in order to get the difference
    # def getTravelRequestBetween(self, start, end):
    #    for doc in self.db.TravelRequest.find({'time': {'$gte': start, '$lt': end}}):
    #        print doc

    # Routes
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
            return self.parseData(route, column)

    def getLine(self, line):
        line = self.db.Route.find({"line": line})
        return self.parseData(line, None)

    def dropRoute(self):
        self.db.Route.drop()

    def getTripDay(self, line):
        return DB.minutesDay / self.getFrequency(line)

    def getRouteStop(self, line):
        routeStop = self.db.Route.find({"line": line}, {"trajectory": 1})
        return self.parseData(routeStop, "trajectory")

    def getFrequency(self, line):

        return self.parseData(self.db.Route.find({"line": line}, {"frequency": 1}), "frequency")



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
        return self.parseData(bus, column)

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
        # today = datetime.date.today()
        today = datetime.date.today() - timedelta(13)
        hourFormat = "%H:%M"
        hour = self.generateTime(self.generateMinute(self.mergeRandomTime(self.getRandomHour(),self.getRandomMinute())))
        return list([line, self.generateRandomCapacity(),datetime.datetime.combine(today,datetime.datetime.strptime(hour, hourFormat).time())])

    # Fitness trip time table
    # This is the function that changes the genotype into a phenotype. It generates the time table for a particular individual.
    def generateFitnessTripTimeTable(self, line, startingTime):
        tripTimeTable = []
        busStop = self.getRouteStop(line)
        startingBusStopTime = startingTime
        tripTimeTable.append([self.getBusStopName(busStop[0]["busStop"]), startingTime])
        for j in range(len(busStop)-1):
            startingBusStopTime = startingBusStopTime + timedelta(minutes=busStop[j]["interval"])
            tripTimeTable.append([self.getBusStopName(busStop[j+1]["busStop"]),startingBusStopTime])
        return tripTimeTable

    # After GA, this function is called to generate all the bus stops given the initial starting times based on the best individual
    def generateTripTimeTable(self, timetable):
        timeTable = []
        for i in range(len(timetable)):
            busStop = self.getRouteStop(timetable[i][0])
            tripTimeTable = []
            tripTimeTable.append([busStop[0]["name"],timetable[i][2]])
            startingBusStopTime = timetable[i][2]
            for j in range(len(busStop)-1):
                startingBusStopTime = startingBusStopTime + timedelta(minutes=busStop[j]["interval"])
                tripTimeTable.append([busStop[j+1]["name"],startingBusStopTime])
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


    def getRequestsFromDB(self, start, end):
        ''' Gets travel requests from the database. Attempts to cluster the requests based on time 
        and calculates a count of the total requests between a time window.

        @param: start - lower time bound
        @param: end - upper time bound
        @return: yesterday's requests with fields startTime, startBusStop, endBusStop.
        '''
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        yesterdayStart = datetime.datetime(yesterday.year, yesterday.month, yesterday.day,0,0,0)
        todayStart = datetime.datetime(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day,0,0,0)
        reqs = []
        requests = self.db.TravelRequestLookAhead.find({"$and": [{"startTime": {"$gte": start}}, {"startTime": {"$lt":
            end}}]}, {"startTime": 1, "startBusStop": 1, "endBusStop": 1, "_id": 0})  # New collection for LookAhead
        for req in requests:
            reqs.append([req.get('startTime', None), req.get('startBusStop', None), req.get('endBusStop', None)])
            #reqs.append(req.get('startTime', None))
        return reqs   

    # Bus Stop Location
    def getBusStopLatitude(self, busStop):
        return self.parseData(self.db.BusStop.find({"name": busStop}, {"latitude": 1}), "latitude")

    def getBusStopLongitude(self, busStop):
        return self.parseData(self.db.BusStop.find({"name": busStop}, {"longitude": 1}), "longitude")

    def getBusStopId(self, busStop):
        return self.parseData(self.db.BusStop.find({"name": busStop}), "_id")

    def getBusStopName(self, id):
        return self.parseData(self.db.BusStop.find({"_id": id}), "name")


    def MaxReqNumTrip(self,trip_sTime,tripEnd, lineNum = 2):
        BusStplist = []
        dirlist =[]
        a = datetime.datetime.strptime(trip_sTime, '%Y-%m-%d %H:%M:%S')
        # t =datetime.datetime.strptime(trip_sTime,'%Y-%m-%d %H:%M:%S').time()
        # e =datetime.datetime.strptime(tripEnd,'%Y-%m-%d %H:%M:%S').time()
        #get the trip time table
        # trip_time_table = self.generateFitnessTripTimeTable(lineNum,trip_sTime[11:16])
        trip_time_table = self.generateFitnessTripTimeTable(lineNum,a)
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

    def insertBusTrip(self, individual):
        '''
        Insert trip details to BusTrip by best individual
        @param: individual, best individual selected by GA
        '''

        tripObjectList = []
        for i in range(len(individual)):
            objID = ObjectId()
            tripObjectList.append(objID)
            line = individual[i][0]
            capacity = individual[i][1]
            startTime = individual[i][2]
   
            trajectory = self.getRoute("trajectory")

            for j in range(len(trajectory)):
                interval = int(trajectory[j]["interval"])
                if j == 0:
                    trajectory[j]["time"] = startTime + datetime.timedelta(minutes=interval)
                else: 
                    trajectory[j]["time"] = trajectory[j-1]["time"] + datetime.timedelta(minutes=interval)
                del trajectory[j]["interval"]

            trip = {
                "_id": objID,
                "capacity": capacity,
                "line": line,
                "startTime": startTime,
                "endTime": trajectory[len(trajectory)-1]["time"],
                "trajectory": trajectory 
            }
            #print trip
            self.db.BusTrip.insert_one(trip)
        self.insertTimeTable1(line, startTime, tripObjectList)

    def insertTimeTable1(self, line, startTime, tripObjectList):            
        ''' 
        Insert object list of BusTrip to TimeTable
        @param: line, lineNo
        @param: startTime, the date of timetable will be used for
        @param: tripObjectList, list of trip object id of specific line
        '''

        objID = ObjectId()
        timeTable = {
            "_id": objID,
            "line": line,
            "date": datetime.datetime(startTime.date().year, startTime.date().month, startTime.date().day, 0, 0, 0),
            "timetable": tripObjectList
        }    
        #print timeTable
        self.db.TimeTable.insert_one(timeTable) 
