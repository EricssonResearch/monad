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
import time
import itertools
import sys
sys.path.append('../OpenStreetMap')

from datetime import timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from operator import itemgetter
from routeGenerator import coordinates_to_nearest_stops, get_route



class DB():
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # INDEX
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Class variables
    # Constructor
    # General
    # Time Helpers
    # GA Helpers & Initial Population
    # Travel Requests
    # Routes
    # Bus
    # Time Table
    # Bus Stop Location
    # Weather

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Class variables
    # ---------------------------------------------------------------------------------------------------------------------------------------
    server = "130.238.15.114"
    port = 27017
    database = "monad1"
    user = "monadStudent"
    password = "M0nad2015"
    timeSeparator = ":"
    minutesDay = 1440
    hoursDay = 24
    minutesHour = 60
    formatTime = '%H:%M'
    yesterday = datetime.datetime(2015, 11, 12)
    busLine = []
    initBusLine = []
    noOfslices = 0
    # Could we store datetime here, instead of integers ?????????????
    timeSliceArray = [[3, 5], [6, 8], [9, 11], [12, 14], [15, 17], [18, 20], [21, 23]]

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        # self.client = MongoClient(DB.server, DB.port, maxPoolSize=200)
        self.client = MongoClient("mongodb://" + DB.user + ":" + DB.password + "@" + DB.server, DB.port, maxPoolSize=200, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000)
        self.db = self.client[DB.database]
        self.generateInitialBusLine(self.getRouteId(), len(DB.timeSliceArray))

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

    def decorator(afunction):
        # A wrapper function is used to wrap functionalites you want around the original function
        def wrapper(*args):
            # Checks whether or not the original function as been executed once
            if not wrapper.has_run:
                wrapper.has_run = True
                return afunction(*args)
            else:
                pass
        wrapper.has_run = False
        return wrapper

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
    # GA Helpers & Initial Population
    # ---------------------------------------------------------------------------------------------------------------------------------------
    '''
    def generateGenotype(self, line):
         Called when generating the initial population, it generates
        each gene.
        @param: line - integer with the line's ID
        # today = datetime.date.today() - timedelta(13)
        today = DB.yesterday
        hour = self.mergeRandomTime(self.getRandomHour(), self.getRandomMinute())
        return list([line, self.generateRandomCapacity(), datetime.datetime.combine(today, datetime.datetime.strptime(hour, self.formatTime).time())])
    '''
    def generateGenotype(self):
        ''' This function is called for each gene, ie. this function creates a gene
        Similar to generateGenotype
        '''
        today = DB.yesterday
        randomFrequency = random.randrange(5, 30)
        busLine = self.generateBusLine()
        startTimeSlice = self.generateRandomStartTimeSlice()
        return list([busLine, self.generateRandomCapacity(), randomFrequency, datetime.datetime.combine(today, startTimeSlice)])

    '''
    def generatePhenotype(self, line, startingTime):
         This is the function that changes the genotype into a phenotype.
        It generates the time table for a particular individual.

        @param: line - integer with the line's ID
        @param: startingTime - initial starting time for the trip

        tripTimeTable = []
        busStop = self.getRouteStop(line)
        startingBusStopTime = startingTime
        tripTimeTable.append([self.getBusStopName(busStop[0]["busStop"]), startingTime])
        for j in range(len(busStop)-1):
            startingBusStopTime = startingBusStopTime + timedelta(minutes=busStop[j]["interval"])
            tripTimeTable.append([self.getBusStopName(busStop[j+1]["busStop"]), startingBusStopTime])
        return tripTimeTable
    '''

    def generatePhenotype2(self, genotype):
        ''' It will generate a set of trips for the current time slice
        @param: genotype - array containing info for a time slice
        @return: [[[busStop, Time],[busStop, Time]],[[busStop, Time],[busStop, Time]]
        '''
        gene = []
        phenotype = []
        busStop = self.getRouteStop(genotype[0])
        '''
        if busStop is None:
            print "======="
            print genotype
            print "======="
        '''
        timeSlice = self.getCurrentTimeSlice(genotype[3])
        tripsBefore = self.calculateTrips(timeSlice[0], genotype[3], genotype[2])
        initialTripStartTime = self.getInitialTripStartTime(tripsBefore, genotype[2], genotype[3])
        tripsAfter = self.calculateTrips(timeSlice[1], genotype[3], genotype[2])
        totalTrips = tripsBefore + tripsAfter + 1
        for i in range(totalTrips):
            gene = []
            startTime = initialTripStartTime + timedelta(minutes=i*genotype[2])
            # print busStop[0]["busStop"]
            # print startTime
            gene.append([self.getBusStopName(busStop[0]["busStop"]), startTime])
            # Update starting time for new trip
            for j in range(len(busStop)-1):
                startTime = startTime + timedelta(minutes=busStop[j]["interval"])
                gene.append([self.getBusStopName(busStop[j+1]["busStop"]), startTime])
            phenotype.append(gene)
        return phenotype

    def getCurrentTimeSlice(self, time):
        ''' It will return starting time of timeSlice and it will return ending time of timeSlice
        '''
        currentHour = time.hour
        for i in range(len(DB.timeSliceArray)):
            if currentHour >= DB.timeSliceArray[i][0] and currentHour <= DB.timeSliceArray[i][1]:
                startingTime = DB.timeSliceArray[i][0]
                endingTime = DB.timeSliceArray[i][1]
                break
        startingTime = datetime.datetime.combine(DB.yesterday, datetime.time(startingTime, 0, 0))
        endingTime = datetime.datetime.combine(DB.yesterday, datetime.time(endingTime, 59, 59))
        return [startingTime, endingTime]

    def calculateTrips(self, boundary, point, frequency):
        ''' Returns the number of trips between two times, given a frequency
        '''
        secDif = abs(int(time.mktime(boundary.timetuple())-time.mktime(point.timetuple())))
        minDif = secDif / DB.minutesHour
        return minDif / frequency

    def getInitialTripStartTime(self, trips, frequency, startingTime):
        ''' Returns the time for the first trip
        '''
        totalMinutes = trips * frequency
        return startingTime - timedelta(minutes=totalMinutes)

    @decorator
    def generateInitialBusLine(self, line, sliceLength):
        for i in line:
            for j in range(sliceLength):
                DB.initBusLine.append(i)
        DB.busLine = DB.initBusLine

    def generateBusLine(self):
        ''' Generates an array that will provide with line ID for each gene
        '''
        if len(DB.busLine) == 0:
            line = self.getRouteId()
            sliceLength = len(DB.timeSliceArray)
            for i in line:
                for j in range(sliceLength):
                    DB.initBusLine.append(i)
            DB.busLine = DB.initBusLine
            '''
            print "abc"
            print DB.initBusLine
            '''
            # DB.busLine = DB.initBusLine
        for x in DB.busLine:
            DB.busLine.remove(x)
            if len(DB.busLine) == 0:
                DB.busLine = DB.initBusLine
            return x

    def generateRandomStartTimeSlice(self):
        ''' Generates random starting times for a time time slice.
        However, this might be changed since there is no need to
        look on the whole time slice
        '''
        if DB.noOfslices == len(DB.timeSliceArray):
            DB.noOfslices = 0
        # random.seed(64)
        b = DB.timeSliceArray[DB.noOfslices]
        hour = random.randint(b[0], b[1])
        minute = random.randint(0, 59)
        seconds = random.randint(1, 59)
        randomTime = datetime.time(hour, minute, seconds)
        DB.noOfslices = DB.noOfslices+1
        return randomTime

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

    def getTravelRequestBetween(self, start, end, line):
        ''' Queries the requests using an initial date and a final date.
        Returns the whole bag of documents found

        @param: start - Initial date for the query
        @param: end - Final date for the query
        '''
        req = self.db.UserTrip.find({"startTime": {"$gte": start, "$lt": end}, "line" : line})
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

    def getReqCountByEndBusStop(self, start, end):
        ''' Performs a summarized query grouping the requests by ending bus stop,
        end time and the line.
        Returns a bag of found documents. These ones have 3 group columns,
        as well as a count column.

        @param: start - Initial datetime for the query
        @param: end - Final datetime for the query
        '''
        pipeline = [{"$match": {"requestTime": {"$gte": start, "$lt": end}}},
                   {"$group": {"_id": {"endTime": "$endTime", "busStop": "$endBusStop", "line": "$line"}, "total": {"$sum": 1}}},
                   {"$sort": {"_id.endTime": 1}}]
        return list(req for req in self.db.UserTrip.aggregate(pipeline))

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
        TODO: TAlk with travel planner to decide what is the difference between startTime and requestTime in UserTrip.
        IMPORTANT!!!! In $group, make sure key value of "_id" matches the $match key value!!
        '''
        queryResults = []
        pipeline = [{"$match": {"startTime": {"$gte": start, "$lt": end}}},
                   {"$group": {"_id": {"RequestTime": "$startTime", "BusStop": "$startBusStop", "line": "$line"}, "total": {"$sum": 1}}},
                   {"$sort": {"_id.RequestTime": 1}}]
        groupQuery = self.db.UserTrip.aggregate(pipeline)
        for x in groupQuery:
            queryResults.append(x)
        return queryResults

    def getRequestsFromDB(self, start, end):
        ''' NOT USED AT THE TIME (Nov 23rd).
        Gets travel requests from the database. Attempts to cluster the
        requests based on time and calculates a count of the total requests
        between a time window.

        @param: start - lower time bound
        @param: end - upper time bound
        @return: yesterday's requests: startTime, startBusStop, endBusStop.
        '''
        reqs = []
        requests = self.db.TravelRequestLookAhead.find({"$and": [{"startTime": {"$gte": start}}, {"startTime": {"$lt": end}}]}, {"startTime": 1, "startBusStop": 1, "endBusStop": 1, "_id": 0})  # New collection for LookAhead
        for req in requests:
            reqs.append([req.get('startTime', None), req.get('startBusStop', None), req.get('endBusStop', None)])
        return reqs

    # TODO: THIS FUNCTION HAS ERRORS BUT ITS NOT CALLED
    def calculateReqNumTrip(self, capacity, trip_stTime, trip_endTime, requestLeftIn, lineNum = 2):
        ''' Calculate average waiting time for request for specific trip(defined by starting trip time and end trip time)
        @param capacity of specific trip, trip start time and end time should be given
        @param requestLeftIn, request list haven't been taken by last trip due to capacity
        @param line number 
        return average waiting time, request list which can't be taken because of capacity
        '''
        BusStplist = []
        dirlist =[]
        RequestTaken = []
        requestLeftOut = []
        pplInBus = 0
        totalrequestnum = 0
        totalWaitingTime = timedelta(minutes=0)
        if isinstance(trip_stTime, str):
            a = datetime.datetime.strptime(trip_stTime, '%Y-%m-%d %H:%M:%S')
        else:
            a = trip_stTime

        trip_time_table = self.generatePhenotype(lineNum, a)

        for i in trip_time_table:
            BusStplist.append([i[0], i[1], 0,0,0])
            dirlist.append(i[0])
        sorted(BusStplist, key=itemgetter(1))   


        if isinstance(trip_stTime, str):
            startTime = datetime.datetime.strptime(trip_stTime,'%Y-%m-%d %H:%M:%S')
        else:
            startTime = trip_stTime
        if isinstance(trip_endTime, str):
            endTime =datetime.datetime.strptime(trip_endTime,'%Y-%m-%d %H:%M:%S')
        else:
            endTime = trip_endTime
        
        endTime = max(BusStplist[len(BusStplist)-1][1], endTime)
        Requests = self.getRequestsFromDB(startTime, endTime)

        Requests = list(requestLeftIn + Requests)

        list(itertools.chain.from_iterable(Requests))
        sorted(Requests, key=itemgetter(1)) 

        ppltakebus = 0
        for i in BusStplist:  
            for req in Requests:
                if (req[1], req[2]) in itertools.combinations(dirlist, 2): #:
                    if req[1] == i[0]:
                        if (i[1] - req[0] > timedelta(minutes=0)) and i[4] < capacity:
                            i[2] = i[2] + 1
                            totalrequestnum = totalrequestnum + 1
                            pplInBus = pplInBus + 1
                            i[4] = pplInBus
                            totalWaitingTime = totalWaitingTime + i[1] - req[0]
                        else:
                            requestLeftOut.append(req)
                    if req[2] == i[0] and req not in requestLeftOut:
                        i[3] = i[3] + 1
                        pplInBus = pplInBus - 1
                        i[4] = pplInBus

        if totalrequestnum != 0:
            avgWaitingTime = (totalWaitingTime.total_seconds()/60.0)/totalrequestnum
        else: 
            avgWaitingTime = 0

        return BusStplist, requestLeftOut, totalWaitingTime.total_seconds()/60.0, avgWaitingTime

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
    # Time Table
    # ---------------------------------------------------------------------------------------------------------------------------------------
    #TODO: THIS FUNCTION IS NOT CALLED; IT HAS ERRORSSS??!?!?
    def processReqest(self, start, end):
        ''' :param start:lower time bound
        :param end: upper time bound
        :return: requests between start and end time ,its generate decompose each multiple line request
        into 2 requests one for each line
        '''
        reqs = []
        nreqs = []
        reqs = self.getRequestsFromDB(start, end)
        samelinereq = 0
        diflinereq = 0
        for req in reqs:
            id = self.getBusStopId(req[1])
            sourceline = self.getBusStopline(id)
            id = self.getBusStopId(req[2])
            destline = self.getBusStopline(id)
            if sourceline == destline:
                nreqs.append(req)
                samelinereq += 1
            else:
                sbusstops = self.getRouteStop(sourceline)
                dbusstops = self.getRouteStop(destline)

                set1 = set(x['busStop'] for x in sbusstops)
                set2 = set(x['busStop'] for x in dbusstops)
                commonbusstopid = set1.intersection(set2)
                commonbusstop = self.getBusStopName(commonbusstopid.pop())

                nreqs.append([req[0], req[1], commonbusstop])
                #print " breakdown request into" % req[0], req[1], commonbusstop
                triptimetable = self.generatePhenotype(sourceline, req[0])
                for x in triptimetable:
                    if x[0] == commonbusstop:
                        tripdate = x[1]
                nreqs.append([tripdate, commonbusstop, req[2]])
                diflinereq += 1

        return nreqs

        objID = ObjectId()
        timeTable = {
            "_id": objID,
            "line": line,
            "date": datetime.datetime(startTime.date().year, startTime.date().month, startTime.date().day, 0, 0, 0),
            "timetable": tripObjectList
        }
        # print timeTable
        self.db.TimeTable.insert_one(timeTable)

    def insertBusTrip(self, individual):
        ''' Insert trip details to BusTrip by best individual

        @param: individual, best individual selected by GA
        '''
        tripObjectList = []
        # requestLeftIn = []
        BUSID = 1
        for i in range(len(individual)):
            line = individual[i][0]
            if i > 0:
                if line != individual[i-1][0]:
                    self.insertTimeTable2(individual[i-1][0], startTime, tripObjectList)
                    tripObjectList[:] = []
            objID = ObjectId()
            tripObjectList.append(objID)
            capacity = individual[i][1]
            startTime = individual[i][2] + timedelta(1)
            busID = BUSID  # Need to assign busID for every Trip
            trajectory = self.getRoute(line, "trajectory")
            '''
            if i == 0:
                startTimeLastTrip = datetime.datetime(startTime.date().year, startTime.date().month, startTime.date().day, 0, 0, 0)
            else:
                startTimeLastTrip = startTime = individual[i-1][2]
            if i < len(individual):
                endTime = (individual[i][2])
            else:
                endTime = datetime.datetime(startTime.date().year, startTime.date().month, startTime.date().day, 23, 59, 59)
            passengerNumList, requestLeftIn, twt, awt = self.calculateReqNumTrip(capacity, startTimeLastTrip, endTime, requestLeftIn)
            sorted(passengerNumList, key=itemgetter(1))
            '''
            # print passengerNumList
            for j in range(len(trajectory)):
                interval = int(trajectory[j]["interval"])
                if j == 0:
                    trajectory[j]["time"] = startTime + datetime.timedelta(minutes=interval)
                else:
                    trajectory[j]["time"] = trajectory[j-1]["time"] + datetime.timedelta(minutes=interval)
                '''
                trajectory[j]["totalPassengers"] = passengerNumList[j][4]
                trajectory[j]["boardingPassengers"] = passengerNumList[j][2]
                trajectory[j]["departingPassengers"] = passengerNumList[j][3]
                '''
                trajectory[j]["totalPassengers"] = 0
                trajectory[j]["boardingPassengers"] = 0
                trajectory[j]["departingPassengers"] = 0
                del trajectory[j]["interval"]
            trip = {
                "_id": objID,
                "capacity": capacity,
                "line": line,
                "startTime": startTime,
                "busID": busID,
                "endTime": trajectory[len(trajectory)-1]["time"],
                "trajectory": trajectory
            }
            # print trip
            self.db.BusTrip.insert_one(trip)
            if i == len(individual) - 1:
                self.insertTimeTable2(line, startTime, tripObjectList)

    def insertTimeTable2(self, line, startTime, tripObjectList):
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

    def getBusStopline(self, id):
        ''' Retrieves the line of a busStop

        @param: id - Bus stop id that is gonna be queried
        '''
        line = self.db.Route.find({"trajectory.busStop": ObjectId(id)})
        return line[0]['line']

    def generateRouteGraph(self):
        '''Generate Directed RouteGraph
        It's a one time job, won't be called by other functions.
        Only when there is new bus stop added should use this function to update RouteGraph
        '''
        allBusStop = self.db.BusStop.find()

        busStopNameList = {}
        tmpList = []
        print allBusStop.count()
        for bs in allBusStop:
            busStopNameList[bs['name']] = bs['_id']
        dictKey = ['busStop', 'condinates', 'distance', '_id', 'timeCost']

        busstop = self.db.BusStop.find() 
        for b in busstop:
            connectedBusStop = []
            connectedNameList = []
            nearStop = coordinates_to_nearest_stops(float(b['longitude']), float(b['latitude']), 300)
            #print list(nearStop['bus_stops'])[:1]
            for j in range(len(nearStop['bus_stops'])):
                if nearStop['bus_stops'][j][0] in busStopNameList.keys() and len(nearStop['bus_stops'][j][0]) > 0 \
                and nearStop['bus_stops'][j][0] not in connectedNameList and nearStop['bus_stops'][j][0] != b['name']:
                    condinatesList = [(float(b['longitude']), float(b['latitude'])), (nearStop['bus_stops'][j][1][0], nearStop['bus_stops'][j][1][1])]
                    #print condinatesList
                    timeDict = get_route(condinatesList)
                    timeCost = timeDict['cost'][1]
                    #print timeC
                    tmpList = list(nearStop['bus_stops'][j])
                    tmpList.append(busStopNameList.get(nearStop['bus_stops'][j][0]))
                    #print tmpList
                    tmpList.append(timeCost)
                    busStopDict = dict(zip(dictKey, tmpList))
                    connectedBusStop.append(busStopDict)
                    connectedNameList.append(nearStop['bus_stops'][j][0])

            objID = ObjectId()
            orgBusID = busStopNameList.get(b['name'])
            orgBusName = b['name']
            newRoute = {
            "_id": objID,
            "orgBusID": orgBusID,
            "orgBusName": orgBusName,
            "connectedBusStop": connectedBusStop
            }
            #print newRoute
            self.db.RouteGraph.insert_one(newRoute)

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Weather
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def insertWeather(self, weather):
        ''' '''
        self.db.Weather.insert_one(weather)

    def selectWeather(self, date):
        ''' '''
        return self.db.Weather.find({"time": {"$gte": datetime.datetime.combine(date, datetime.time(0, 0)), "$lt": datetime.datetime.combine(date, datetime.time(23, 59))}})

    def selectBusTrip(self, date):
        ''' '''
        return self.db.BusTrip.find({"startTime": {"$gte": date, "$lt": date + timedelta(minutes=60)}}).sort([("line", 1), ("startTime", 1)])
