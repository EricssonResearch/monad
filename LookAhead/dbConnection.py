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
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # DB Credentials
    # ---------------------------------------------------------------------------------------------------------------------------------------
    server = "130.238.15.114"
    port = 27017
    database = "monad"
    timeSeparator = ":"
    minutesDay = 1440
    hoursDay = 24
    minutesHour = 60
    formatTime = '%H:%M'
    yesterday = datetime.datetime(2015, 10, 21)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        self.client = MongoClient(DB.server, DB.port, maxPoolSize=200)
        self.db = self.client[DB.database]

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # General
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def createCollection(self, name):
        ''' NOT USED AT THE TIME (Nov 6th).
        Interface function that creates a new collection on DB

        @param: name - Name of the collection to be created
        '''
        self.db.createCollection(name)

    def parseData(self, data, column):
        ''' Access the result of a DB query.
        Funcionality must be added when result is greater than one document
        If a column is specified, it will just retrieve that one

        @param: data - Data retrieved from DB
        @param: column - Name of the collection field that needs to be
        retrieved. If None, it will retrieve the whole document
        '''
        if column is None:
            for document in data:
                return document
        else:
            for document in data:
                return document[column]

    def generateRandomText(self, size=3, chars=string.ascii_uppercase):
        ''' NOT USED AT THE TIME (Nov 6th).
        Returns a string of size 3 that contains random characters

        '''
        return ''.join(random.choice(chars) for _ in range(size))

    def generateRandomNumber(self, size=3, chars=string.digits):
        ''' NOT USED AT THE TIME (Nov 6th).
        Returns a string of size 3 that contains random digits

        '''
        return ''.join(random.choice(chars) for _ in range(size))

    def flatten(self, element):
        ''' Dont forget to credit this function to Stack Overflow:
        http://stackoverflow.com/questions/14820273/confused-by-chain-enumeration
        This function recieves a list that can have several multiple levels
        and it returns a a single level list.

        @param: element - Array that is going to be processed
        '''
        for el in element:
            if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
                for sub in self.flatten(el):
                    yield sub
            else:
                yield el

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Time Helpers
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def getRandomHour(self):
        ''' Returns a random integer between 0 and DB.hoursDay

        '''
        return random.randrange(DB.hoursDay)

    def getRandomMinute(self):
        ''' Returns a random integer between 0 and DB.minutesHour

        '''
        return random.randrange(DB.minutesHour)

    def mergeRandomTime(self, hour, minute):
        ''' Returns a string with a format similar to DB.formatTime

        @param: hour - String that contains an hour
        @param: minute - String that contains a minute
        '''
        if len(str(hour)) == 1:
            hour = "0" + str(hour)
        if len(str(minute)) == 1:
            minute = "0" + str(minute)
        return str(hour) + DB.timeSeparator + str(minute)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Travel Requests
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def getTravelRequestCount(self):
        ''' NOT USED AT THE TIME (Nov 6th).
        It counts the number of requests made on the travel request collection

        '''
        return self.db.TravelRequest.count()

    def getRandomTravelRequestId(self):
        ''' NOT USED AT THE TIME (Nov 6th).
        It queries a random request and retrieves only its ID

        '''
        req = self.db.TravelRequest.find()[random.randrange(self.getTravelRequestCount())]
        return req["_id"]

    def getRandomTravelRequest(self):
        ''' NOT USED AT THE TIME (Nov 6th).
        It queries a request by its IDS and retrieves the whole document

        '''
        req = self.db.TravelRequest.find(
            {"_id": ObjectId(self.getRandomTravelRequestId())})
        return req

    def getTravelRequest(self, column):
        ''' It queries all the requests from the travel request collection.
        All the document is retrieved except the "_id"

        @param: column - Name of the collection field that needs to be retrieved
        If None, it will retrieve the whole document
        '''
        req = self.db.TravelRequestLookAhead.find({}, {"_id": False})
        return self.parseData(req, column)

    def getTravelRequestBetween(self, start, end):
        ''' Queries the requests using an initial date and a final date.
        Returns the whole bag of documents found

        @param: start - Initial date for the query
        @param: end - Final date for the query
        '''
        req = self.db.TravelRequestLookAhead.find({"startTime": {"$gte": start, "$lt": end}})
        return req

    def getTravelRequestSummary(self, start, end):
        ''' NOT USED AT THE TIME (Nov 6th).
        It was replaced by grpReqByBusstopAndTime since the use of JS on
        the keyf was giving some problems with the time.
        Performs a summarized query grouping the requests by bus stop,
        hour and minute.
        Returns the whole bag of documents found with the 3 group columns,
        as well as the a count column.
        It is used to evaluate an individual.

        @param: start - Initial datetime for the query
        @param: end - Final datetime for the query
        '''
        keyf = "function(doc) { return { startBusStop: doc.startBusStop, hour: doc.startTime.getHours(), minute: doc.startTime.getMinutes()};}"
        condition = {"startTime": {"$gte": start, "$lt": end}}
        initial = {"count": 0}
        reduce = "function(curr, result) { result.count++; }"
        # req = self.db.TravelRequest.group(keyf, condition, initial, reduce)
        req = self.db.TravelRequestLookAhead.group(keyf, condition, initial, reduce)
        req = sorted(req, key=itemgetter("hour", "minute"))
        return req

    def grpReqByBusstopAndTime(self, start, end):
        ''' Performs a summarized query grouping the requests by bus stop,
        hour and minute.
        Returns the whole bag of documents found with the 3 group columns,
        as well as the a count column.
        It is used to evaluate an individual.
        A query is made to group requests made to a busstop and counting
        the number of similar requests made

        @param: start - Initial datetime for the query
        @param: end - Final datetime for the query
        '''
        queryResults = []
        pipline = [{"$match": {"startTime": {"$gte": start, "$lt": end}}},
                   {"$group": {"_id": {"RequestTime": "$startTime", "BusStop": "$startBusStop"}, "total": {"$sum": 1}}},
                   {"$sort": {"_id.RequestTime": 1}}]
        groupQuery = self.db.TravelRequestLookAhead.aggregate(pipline)
        for x in groupQuery:
            queryResults.append(x)
        return queryResults

    def getRequestsFromDB(self, start, end):
        ''' Gets travel requests from the database. Attempts to cluster the requests based on time 
        and calculates a count of the total requests between a time window.

        @param: start - lower time bound
        @param: end - upper time bound
        @return: yesterday's requests with fields startTime, startBusStop, endBusStop.
        '''
        reqs = []
        # yesterday = datetime.date.today() - datetime.timedelta(days=1)
        # yesterdayStart = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 0, 0, 0)
        # todayStart = datetime.datetime(datetime.date.today().year, datetime.date.today().month, datetime.date.today().day, 0, 0, 0)
        requests = self.db.TravelRequestLookAhead.find({"$and": [{"startTime": {"$gte": start}}, {"startTime": {"$lt":
            end}}]}, {"startTime": 1, "startBusStop": 1, "endBusStop": 1, "_id": 0})  # New collection for LookAhead
        for req in requests:
            reqs.append([req.get('startTime', None), req.get('startBusStop', None), req.get('endBusStop', None)])
        return reqs

    def MaxReqNumTrip(self, trip_sTime, tripEnd, lineNum=2):
        BusStplist = []
        dirlist = []
        a = datetime.datetime.strptime(trip_sTime, '%Y-%m-%d %H:%M:%S')
        # t =datetime.datetime.strptime(trip_sTime,'%Y-%m-%d %H:%M:%S').time()
        # e =datetime.datetime.strptime(tripEnd,'%Y-%m-%d %H:%M:%S').time()
        # get the trip time table
        # trip_time_table = self.generateFitnessTripTimeTable(lineNum,trip_sTime[11:16])
        trip_time_table = self.generateFitnessTripTimeTable(lineNum, a)
        for i in trip_time_table:
            BusStplist.append([i[0], 0])
            dirlist.append(i[0])
        t = datetime.datetime.strptime(trip_sTime, '%Y-%m-%d %H:%M:%S')
        e = datetime.datetime.strptime(tripEnd, '%Y-%m-%d %H:%M:%S')
        # get all requests where starting time is more than trip starting time
        Requests = self.getRequestsFromDB(t, e)
        # get only the requests with start location in bus stops and end location in bus stps
        for req in Requests:
            for i in BusStplist:
                if (req[1], req[2]) in itertools.combinations(dirlist, 2):
                    if req[1] == i[0]:
                        i[1] += 1
                    if req[2] == i[0]:
                        i[1] += -1
        sum = 0
        for i in BusStplist:
            sum += i[1]
            i[1] = sum
        return BusStplist

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Routes
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def populateRoute(self, route):
        ''' This function should be written again since the DB layout
         has changed.

        @param: route - List with route information
        '''
        # route5 = {"line": 5, "durationTime":39, routeStop2}
        # routeStop5 = ["Stenhagenskolan","Herrhagens Byväg","Kiselvägen","Stenhagens Centrum","Stenröset","Stenhällen","Gatstenen","Hedensbergsvägen","Flogsta centrum","Rickomberga","Studentstaden","Ekonomikum","Götgatan","Skolgatan","Stadshuset","Centralstationen","Samariterhemmet","Strandbodgatan","Kungsängsesplanaden","Vimpelgatan","Lilla Ultuna","Kuggebro","Vilan","Nämndemansvägen","Lapplandsresan","Ölandsresan","Daneport","Västgötaresan","Gotlandsresan","Smålandsvägen"]
        self.db.Route.insert_one(route)

    def dropRoute(self):
        ''' This function drops the whole route collection.

        '''
        self.db.Route.drop()

    def getRouteId(self):
        ''' Retrieves a list with the different number of lines that has
        been inserted on the route collection.

        '''
        route = self.db.Route.find().distinct("line")
        return route

    def getRoute(self, line, column):
        ''' Retrieves a particular line document.

        @param: line - integer with the line's ID
        @param: column - it is a string with the name of the field
        '''
        return self.parseData(self.db.Route.find({"line": line}), column)

    def getTripDay(self, line):
        ''' Retrieves an aprox number of trips by day given the ratio
        between the minutes on the day and the line frequency.

        However, the idea of the frequency is not being considered on
        the future implementations, so this function might be removed

        @param: line - integer with the line's ID
        '''
        return DB.minutesDay / self.getFrequency(line)

    def getRouteStop(self, line):
        ''' Retrieves an array with all the trajectory of a particular line.
        A trajectory include the bus stops and the times between them.

        @param: line - integer with the line's ID
        '''
        return self.parseData(self.db.Route.find({"line": line}, {"trajectory": 1}), "trajectory")

    def getFrequency(self, line):
        ''' Retrieves the frequency of a bus line.

        @param: line - integer with the line's ID
        '''
        return self.parseData(self.db.Route.find({"line": line}, {"frequency": 1}), "frequency")

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Bus
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # https://www.ul.se/en/About-UL/About-our-public-function/
    # In total, around 125 city buses, 250 regional buses and 11 trains.
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def dropBusCollection(self):
        ''' This function drops the whole bus collection.

        '''
        self.db.bus.drop()

    def generateRandomCapacity(self):
        ''' This function randomly chooses a capacity from an array.
        This information should be stored on the DB.
        Also, the capapcity values were generated out of the blue.
        A bus collection has not been included on the new DB layout.

        '''
        capacity = [20, 60, 120]
        return random.choice(capacity)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # GA Helpers
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def generateStartingTripTime(self, line):
        ''' Called when generating the initial population, it generates
        each gene.

        @param: line - integer with the line's ID
        '''
        # today = datetime.date.today() - timedelta(13)
        today = DB.yesterday
        hour = self.mergeRandomTime(self.getRandomHour(), self.getRandomMinute())
        return list([line, self.generateRandomCapacity(), datetime.datetime.combine(today, datetime.datetime.strptime(hour, self.formatTime).time())])

    def generateFitnessTripTimeTable(self, line, startingTime):
        ''' This is the function that changes the genotype into a phenotype.
        It generates the time table for a particular individual.

        @param: line - integer with the line's ID
        @param: startingTime - initial starting time for the trip
        '''
        tripTimeTable = []
        busStop = self.getRouteStop(line)
        startingBusStopTime = startingTime
        tripTimeTable.append([self.getBusStopName(busStop[0]["busStop"]), startingTime])
        for j in range(len(busStop)-1):
            startingBusStopTime = startingBusStopTime + timedelta(minutes=busStop[j]["interval"])
            tripTimeTable.append([self.getBusStopName(busStop[j+1]["busStop"]), startingBusStopTime])
        return tripTimeTable

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Time Table
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def generateTripTimeTable(self, timetable):
        ''' After GA, this function is called to generate all the bus stops
        given the initial starting times based on the best individual.

        @param: timetable - best inidividual from GA experiment
        '''
        timeTable = []
        for i in range(len(timetable)):
            busStop = self.getRouteStop(timetable[i][0])
            tripTimeTable = []
            tripTimeTable.append([busStop[0]["name"], timetable[i][2]])
            startingBusStopTime = timetable[i][2]
            for j in range(len(busStop)-1):
                startingBusStopTime = startingBusStopTime + timedelta(minutes=busStop[j]["interval"])
                tripTimeTable.append([busStop[j+1]["name"], startingBusStopTime])
            timeTable.append([timetable[i][0], timetable[i][1], list(self.flatten(tripTimeTable))])
        return sorted(timeTable, key=itemgetter(2))

    def insertTimeTable(self, document):
        ''' This function takes the result from generateTripTimeTable, and
        generates a JSON document with the DB layout. Then, it proceeds to
        insert it on the DB.

        @param: document - A timetable for a whole day
        '''
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

    def insertTimeTable1(self, line, startTime, tripObjectList):
        ''' Insert object list of BusTrip to TimeTable

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
        # print timeTable
        self.db.TimeTable.insert_one(timeTable)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Bus Stop Location
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def getBusStopLatitude(self, busStop):
        ''' Retrieves the latitude of a particular bus stop

        @param: busStop - Bus stop name that is gonna be queried
        '''
        return self.parseData(self.db.BusStop.find({"name": busStop}, {"latitude": 1}), "latitude")

    def getBusStopLongitude(self, busStop):
        ''' Retrieves the longitude of a particular bus stop

        @param: busStop - Bus stop name that is gonna be queried
        '''
        return self.parseData(self.db.BusStop.find({"name": busStop}, {"longitude": 1}), "longitude")

    def getBusStopId(self, busStop):
        ''' Retrieves the id of a particular bus stop

        @param: busStop - Bus stop name that is gonna be queried
        '''
        return self.parseData(self.db.BusStop.find({"name": busStop}), "_id")

    def getBusStopName(self, id):
        ''' Retrieves the name of a particular bus stop

        @param: id - Bus stop id that is gonna be queried
        '''
        return self.parseData(self.db.BusStop.find({"_id": id}), "name")

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Bus Trip
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def insertBusTrip(self, individual):
        ''' Insert trip details to BusTrip by best individual

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
            # print trip
            self.db.BusTrip.insert_one(trip)
        self.insertTimeTable1(line, startTime, tripObjectList)
