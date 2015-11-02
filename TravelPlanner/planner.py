# Copyright 2015 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not 
# use this file except in compliance with the License. You may obtain a copy 
# of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
# License for the specific language governing permissions and limitations 
# under the License.


import pymongo
import datetime
import bson

from pymongo import MongoClient
from bson.objectid import ObjectId

NUM_OF_ROUTES_RETURNED = 5
# tripTuple
TT_ROUTE = 0
TT_TIME_DIFFERENCE = 1
TT_DEPARTURE_TIME = 2
TT_ARRIVAL_TIME = 3
# possibleRoutes
PR_ROUTE = 0
PR_START = 1
PR_END   = 2
PR_LINE  = 3
# doubleRoute
DR_ROUTE1 = 0
DR_START1 = 1
DR_END1   = 2
DR_LINE1  = 3
DR_ROUTE2 = 4
DR_START2 = 5
DR_END2   = 6
DR_LINE2  = 7
# position
POS_LATITUDE  = 0
POS_LONGITUDE = 1

# Dummy class, will be used for the moment until the real RA is ready
LAT_TOPELIUS = 59.888213
LON_TOPELIUS = 17.648799
LAT_STUDENTS = 59.857667
LON_STUDENTS = 17.613137
LAT_STADSHUS = 59.860432
LON_STADSHUS = 17.640485
LAT_GRINDSTU = 59.839929
LON_GRINDSTU = 17.639780
class RouteAdministrator:
    def __init__(self):
        pass

    def getBusStop(self, latitude, longitude):
        if (latitude == LAT_TOPELIUS and longitude == LON_TOPELIUS):
            return "Topeliusgatan"
        if (latitude == LAT_STUDENTS and longitude == LON_STUDENTS):
            return "Studentstaden"
        if (latitude == LAT_STADSHUS and longitude == LON_STADSHUS):
            return "Stadshuset"
        if (latitude == LAT_GRINDSTU and longitude == LON_GRINDSTU):
            return "Grindstugan"

    def getBusStopPosition(self, name):
        if (name == "Topeliusgatan"):
            return (LAT_TOPELIUS, LON_TOPELIUS)
        if (name == "Studentstaden"):
            return (LAT_STUDENTS, LON_STUDENTS)
        if (name == "Stadshuset"):
            return (LAT_STADSHUS, LON_STADSHUS)
        if (name == "Grindstugan"):
            return (LAT_GRINDSTU, LON_GRINDSTU)
# End of dummy part

class Mode:
    tripTime = 1
    waitTime = 2
    startTime   = 3
    arrivalTime = 4

class TravelPlanner:

    def __init__(self, client):
        self.db = client.monad
        self.travelRequest = self.db.TravelRequest
        self.route = self.db.Route
        self.timeTable = self.db.TimeTable
        self.userTrip = self.db.UserTrip
        self.busStop = self.db.BusStop
        self.busTrip = self.db.BusTrip

        self.fittingRoutes = []
        self.startingWaypoint = []
        self.endingWaypoint = []
        self.doubleRoutes = []
        self.possibleRoutes = []
        self.tripTuples = []


    def _searchOtherRoutes(self, busLine, busStopID):
        cursor = self.route.find({"trajectory.busStop": busStopID, 
                "trajectory.busStop": self.endBusStop["_id"], "line": {"$ne": busLine}})
        if (cursor is None):
            return []
        possibilities = []
        startNumber = 0
        for route in cursor:
            fits = False
            if ((route["line"] == (busLine - 100)) or (route["line"] == (busLine + 100))):
                continue 
            for i in range(len(route["trajectory"])):
                if (route["trajectory"][i]["busStop"] == busStopID):
                    fits = True
                    startNumber = i
                elif (route["trajectory"][i]["busStop"] == self.endBusStop["_id"]):
                    if (fits):
                        possibilities.append((route, startNumber, i, route["line"]))
                    break
        return possibilities

    def _findFittingRoutes(self):
        request = self.travelRequest.find_one({"_id": self.requestID})
        self.startBusStop = self.busStop.find_one({"_id": request["startBusStop"]})
        self.endBusStop   = self.busStop.find_one({"_id": request["endBusStop"]})
        self.userID = request["userID"]
        self.requestTime = request["requestTime"]

        if (request["endTime"] == "null"):
            self.startTime = request["startTime"]
            self.endTime   = 0
            self.timeMode  = Mode.startTime
        elif (request["startTime"] == "null"):
            self.startTime = 0
            self.endTime   = request["endTime"]
            self.timeMode  = Mode.arrivalTime
        else:
            return

        cursor = self.route.find({"trajectory.busStop": self.startBusStop["_id"],
                "trajectory.busStop": self.endBusStop["_id"]})
        for route in cursor:
            fits = False
            for i in range(len(route["trajectory"])):
                if (route["trajectory"][i]["busStop"] == self.startBusStop["_id"]):
                    self.startingWaypoint.append(i)
                    self.fittingRoutes.append(route)
                    fits = True
                elif (route["trajectory"][i]["busStop"] == self.endBusStop["_id"]):
                    if (fits):
                        self.endingWaypoint.append(i)
                    break

        self.startLines = self.route.find({"trajectory.busStop": self.startBusStop["_id"]})
        for startLine in self.startLines:
            maybe = False
            startNumber = 0
            for i in range(len(startLine["trajectory"])):
                if (startLine["trajectory"][i]["busStop"] == self.startBusStop["_id"]):
                    maybe = True
                    startNumber = i
                elif (maybe): 
                    self.possibleRoutes = self._searchOtherRoutes(startLine["line"], 
                            startLine["trajectory"][i]["busStop"])
                    if (self.possibleRoutes == []):
                        continue
                    for entry in self.possibleRoutes:
                        self.doubleRoutes.append((startLine, startNumber, i, startLine["line"],
                                entry[PR_ROUTE], entry[PR_START], entry[PR_END], entry[PR_LINE]))
        
   
    def _isBetterTrip(self, i):
        if (self.timeMode == Mode.startTime):
            if (self.timeToArrival < self.tripTuples[i][TT_TIME_DIFFERENCE]):
                return True
            elif (self.timeToArrival == self.tripTuples[i][TT_TIME_DIFFERENCE]):
                if (self.dptTime > self.tripTuples[i][TT_DEPARTURE_TIME]):
                    if (self.routeMode == Mode.tripTime):
                        return True
                else:
                    if (self.routeMode == Mode.waitTime):
                        return True
        elif (self.timeMode == Mode.arrivalTime):
            if (self.diffToArrTime < self.tripTuples[i][TT_TIME_DIFFERENCE]):
                return True
            elif (self.diffToArrTime == self.tripTuples[i][TT_TIME_DIFFERENCE]):
                if (self.dptTime > self.tripTuples[i][TT_DEPARTURE_TIME]):
                    if (self.routeMode == Mode.tripTime):
                        return True
                else:
                    if (self.routeMode == Mode.waitTime):
                        return True
        return False

    def _rankTrip(self, trip):
        tripProcessed = False
        if (len(self.tripTuples) >= NUM_OF_ROUTES_RETURNED):
            if (not self._isBetterTrip(-1)):
                return
            
        for i in range(len(self.tripTuples)):
            if (self._isBetterTrip(i)):
                if (self.timeMode == Mode.startTime):
                    self.tripTuples.insert(i, 
                            (trip, self.timeToArrival, self.dptTime, self.arrTime))
                elif (self.timeMode == Mode.arrivalTime):
                    self.tripTuples.insert(i, 
                            (trip, self.diffToArrTime, self.dptTime, self.arrTime))
                tripProcessed = True
                break

        if (tripProcessed == False):
            if (self.timeMode == Mode.startTime):
                self.tripTuples.append((trip, self.timeToArrival, self.dptTime, self.arrTime))
            elif (self.timeMode == Mode.arrivalTime):
                self.tripTuples.append((trip, self.diffToArrTime, self.dptTime, self.arrTime))
        self.tripTuples = self.tripTuples[:NUM_OF_ROUTES_RETURNED]

    def _insertTrip(self, trip):
        if (self.timeMode == Mode.startTime):
            self.timeToArrival = self.arrTime - self.startTime
            if (self.tripTuples == []):
                self.tripTuples.append((trip, self.timeToArrival, self.dptTime, self.arrTime))
                return
            self._rankTrip(trip)

        elif (self.timeMode == Mode.arrivalTime):
            self.diffToArrTime = self.endTime - self.arrTime
            if (self.tripTuples == []):
                self.tripTuples.append((trip, self.diffToArrTime, self.dptTime, self.arrTime))
                return
            self._rankTrip(trip)

    def _findSecondTrip(self, route, startTrip):
        ttCollection = self.timeTable.find_one({"line": route[DR_LINE2]})
        trips = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
        self.bestArrivalTime = datetime.datetime.max
        self.bestSecondTrip = None
        for trip in trips:
            self.dptSwitch = trip["trajectory"][route[DR_START2]]["time"]
            self.arrTime   = trip["trajectory"][route[DR_END2]]["time"]
            if ((self.arrSwitch < self.dptSwitch) and (self.arrTime < self.bestArrivalTime)):
                self.bestSecondTrip = trip
                self.bestArrivalTime = self.arrTime

    def _findFirstTrip(self, route, trip):
        ttCollection = self.timeTable.find_one({"line": route[DR_LINE1]})
        trips = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
        self.bestDepartureTime = datetime.datetime.min
        self.bestSecondTrip = None
        for trip in trips:
            self.dptTime   = trip["trajectory"][route[DR_START1]]["time"]
            self.arrSwitch = trip["trajectory"][route[DR_END1]]["time"]
            if ((self.arrSwitch < self.dptSwitch) and (self.dptTime > self.bestDepartureTime)):
                self.bestFirstTrip = trip
                self.bestDepartureTime = self.dptTime

    def _findBestRoute(self):
        counter = 0
        for route in self.fittingRoutes:
            ttCollection = self.timeTable.find_one({"line": route["line"]})
            schedules = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})

            for trip in schedules:
                self.dptTime = trip["trajectory"][self.startingWaypoint[counter]]["time"]
                self.arrTime = trip["trajectory"][self.endingWaypoint[counter]]["time"]
                if (self.timeMode == Mode.startTime):
                    if (self.dptTime > self.startTime):
                        self._insertTrip(trip)
                elif (self.timeMode == Mode.arrivalTime):
                    if (self.arrTime < self.endTime):
                        self._insertTrip(trip)

            counter = counter + 1

        for route in self.doubleRoutes: 
            print "Line 1: " + str(route[DR_LINE1]) + " - Line 2: " + str(route[DR_LINE2])
            if (self.timeMode == Mode.startTime):
                ttCollection = self.timeTable.find_one({"line": route[DR_LINE1]})
                schedules = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
                for trip in schedules:
                    self.dptTime   = trip["trajectory"][route[DR_START1]]["time"]
                    self.arrSwitch = trip["trajectory"][route[DR_END1]]["time"]
                    if (self.dptTime > self.startTime):
                        self._findSecondTrip(route, trip)
                        self._insertTrip((route, trip, self.bestSecondTrip))
            elif (self.timeMode == Mode.arrivalTime):
                ttCollection = self.timeTable.find_one({"line": route[DR_LINE2]})
                schedules = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
                for trip in schedules["timetable"]:
                    self.dptSwitch = trip["trajectory"][route[DR_START2]]["time"]
                    self.arrTime   = trip["trajectory"][route[DR_END2]]["time"]
                    if (self.arrTime < self.endTime):
                        self._findFirstTrip(route, trip)
                        self._insertTrip((route, trip, self.bestFirstTrip))


    #TODO: Implement storing of double routes
    def _updateDatabase(self):
        entryList = []
        self.userTripList = []
        i = 0
        for (trip, timeDiff, dptTime, arrTime) in self.tripTuples:
            userTripID = ObjectId()
            if (isinstance(trip, tuple)):
                continue # DoubleRoute
            else:
                newEntry = {
                        "_id": userTripID,
                        "userID": self.userID,
                        "line": trip["line"],
                        "busID": trip["busID"],
                        "startBusStop": self.startBusStop,
                        "endBusStop": self.endBusStop,
                        "startTime": dptTime,
                        "endTime": arrTime,
                        "requestTime": self.requestTime,
                        "feedback": -1,
                        "trajectory": [],
                        "requestId": self.requestID,
                        "booked": False
                }
                started = False
                for stop in trip["trajectory"]:
                    if (not started):
                        continue
                    started = True
                    newEntry["trajectory"].append(stop["busStop"])
                    if (stop["busStop"] == self.endBusStop):
                        break
            i += 1
            entryList.append(newEntry)
            self.userTripList.append(userTripID)
        if (entryList != []):
            self.userTrip.insert_many(entryList)


    def getBestRoutes(self, requestID, mode = Mode.tripTime):
        self.requestID = requestID
        self.routeMode = mode
        self._findFittingRoutes()
        
        if ((self.fittingRoutes == []) and (self.doubleRoutes == [])):
            print "No fitting routes found"
            return None
        print "Found " + str(len(self.fittingRoutes)) + "/" + str(len(self.doubleRoutes)) + " fitting/double Routes"

        self._findBestRoute()
        print "Found " + str(len(self.tripTuples)) + " tripTuples"

        if (self.tripTuples == []):
            print "No best route found"
            return None

        self._updateDatabase()

        return self.userTripList


