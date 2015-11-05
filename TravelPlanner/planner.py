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

# constants
NUM_OF_ROUTES_RETURNED = 5
MAXIMUM_NUMBER_OF_LINES = 150
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
# end of constants


class Mode:
    tripTime = 1
    waitTime = 2
    startTime   = 3
    arrivalTime = 4

class TravelPlanner:

    def __init__(self, client, debug = False):
        self.db = client.monad1
        self.travelRequest = self.db.TravelRequest
        self.route = self.db.Route
        self.timeTable = self.db.TimeTable
        self.userTrip = self.db.UserTrip
        self.busTrip = self.db.BusTrip

        self.fittingRoutes = []
        self.startingWaypoint = []
        self.endingWaypoint = []
        self.doubleRoutes = []
        self.possibleRoutes = []
        self.tripTuples = []
        self.lineTuples = []
        self.lineSchedules = []

        self.bestSecondTrip = None
        self.bestFirstTrip = None

        self.debug = debug

        for i in range(MAXIMUM_NUMBER_OF_LINES):
            self.lineSchedules.append(None)


    def _isDoubleRoute(self, trip):
        if (isinstance(trip, tuple)):
            return True
        else:
            return False

    def _searchOtherRoutes(self, busLine, busStopID):
        cursor = self.route.find({"trajectory.busStop": busStopID, 
                "trajectory.busStop": self.endBusStop, "line": {"$ne": busLine}})
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
                elif (route["trajectory"][i]["busStop"] == self.endBusStop):
                    if (fits):
                        possibilities.append((route, startNumber, i, route["line"]))
                    break
        return possibilities

    def _findFittingRoutes(self):
        request = self.travelRequest.find_one({"_id": self.requestID})
        self.startBusStop = request["startBusStop"]
        self.endBusStop   = request["endBusStop"]
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

        cursor = self.route.find({"trajectory.busStop": self.startBusStop,
                "trajectory.busStop": self.endBusStop})
        for route in cursor:
            fits = False
            for i in range(len(route["trajectory"])):
                if (route["trajectory"][i]["busStop"] == self.startBusStop):
                    self.startingWaypoint.append(i)
                    self.fittingRoutes.append(route)
                    fits = True
                elif (route["trajectory"][i]["busStop"] == self.endBusStop):
                    if (fits):
                        self.endingWaypoint.append(i)
                    break

        self.startLines = self.route.find({"trajectory.busStop": self.startBusStop})
        for startLine in self.startLines:
            maybe = False
            startNumber = 0
            for i in range(len(startLine["trajectory"])):
                if (startLine["trajectory"][i]["busStop"] == self.startBusStop):
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
            if (self._isDoubleRoute(trip)):
                self.arrTime = self.bestArrivalTime
            self.timeToArrival = self.arrTime - self.startTime
            if (self.tripTuples == []):
                self.tripTuples.append((trip, self.timeToArrival, self.dptTime, self.arrTime))
                return
            self._rankTrip(trip)

        elif (self.timeMode == Mode.arrivalTime):
            if (self._isDoubleRoute(trip)):
                self.dptTime = self.bestDepartureTime
            self.diffToArrTime = self.endTime - self.arrTime
            if (self.tripTuples == []):
                self.tripTuples.append((trip, self.diffToArrTime, self.dptTime, self.arrTime))
                return
            self._rankTrip(trip)

    def _findSecondTrip(self, route, startTrip):
        if (self.lineSchedules[route[DR_LINE2]] == None):
            ttCollection = self.timeTable.find_one({"line": route[DR_LINE2]})
            trips = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
            self.lineSchedules[route[DR_LINE2]] = trips
        else:
            trips = self.lineSchedules[route[DR_LINE2]].rewind()
        self.bestArrivalTime = datetime.datetime.max
        for trip in trips:
            self.dptSwitch = trip["trajectory"][route[DR_START2]]["time"]
            self.arrTime   = trip["trajectory"][route[DR_END2]]["time"]
            if ((self.arrSwitch < self.dptSwitch) and (self.arrTime < self.bestArrivalTime)):
                self.bestSecondTrip = trip
                self.bestArrivalTime = self.arrTime

    def _findFirstTrip(self, route, trip):
        if (self.lineSchedules[route[DR_LINE1]] == None):
            ttCollection = self.timeTable.find_one({"line": route[DR_LINE1]})
            trips = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
            self.lineSchedules[route[DR_LINE1]] = trips
        else:
            trips = self.lineSchedules[route[DR_LINE1]].rewind()
        self.bestDepartureTime = datetime.datetime.min
        for trip in trips:
            self.dptTime   = trip["trajectory"][route[DR_START1]]["time"]
            self.arrSwitch = trip["trajectory"][route[DR_END1]]["time"]
            if ((self.arrSwitch < self.dptSwitch) and (self.dptTime > self.bestDepartureTime)):
                self.bestFirstTrip = trip
                self.bestDepartureTime = self.dptTime

    def _findBestRoute(self):
        counter = 0
        for route in self.fittingRoutes:
            if (self.lineSchedules[route["line"]] == None):
                ttCollection = self.timeTable.find_one({"line": route["line"]})
                trips = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
                self.lineSchedules[route["line"]] = trips
            else:
                trips = self.lineSchedules[route["line"]].rewind()

            for trip in trips:
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
            if ((route[DR_LINE1], route[DR_LINE2]) in self.lineTuples):
                continue
            else:
                self.lineTuples.append((route[DR_LINE1], route[DR_LINE2]))
            if (self.debug):
                print "Line 1: " + str(route[DR_LINE1]) + " - Line 2: " + str(route[DR_LINE2])

            if (self.timeMode == Mode.startTime):
                if (self.lineSchedules[route[DR_LINE1]] == None):
                    ttCollection = self.timeTable.find_one({"line": route[DR_LINE1]})
                    trips = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
                    self.lineSchedules[route[DR_LINE1]] = trips
                else:
                    trips = self.lineSchedules[route[DR_LINE1]].rewind()

                for trip in trips:
                    self.dptTime   = trip["trajectory"][route[DR_START1]]["time"]
                    self.arrSwitch = trip["trajectory"][route[DR_END1]]["time"]
                    if (self.dptTime > self.startTime):
                        self._findSecondTrip(route, trip)
                        self._insertTrip((route, trip, self.bestSecondTrip))

            elif (self.timeMode == Mode.arrivalTime):
                if (self.lineSchedules[route[DR_LINE2]] == None):
                    ttCollection = self.timeTable.find_one({"line": route[DR_LINE2]})
                    trips = self.busTrip.find({"_id": {"$in": ttCollection["timetable"]}})
                    self.lineSchedules[route[DR_LINE2]] = trips
                else:
                    trips = self.lineSchedules[route[DR_LINE2]].rewind()

                for trip in trips:
                    self.dptSwitch = trip["trajectory"][route[DR_START2]]["time"]
                    self.arrTime   = trip["trajectory"][route[DR_END2]]["time"]
                    if (self.arrTime < self.endTime):
                        self._findFirstTrip(route, trip)
                        self._insertTrip((route, trip, self.bestFirstTrip))


    def _updateDatabase(self):
        entryList = []
        self.userTripDict = {}
        i = 0
        for (trip, timeDiff, departureTime, arrivalTime) in self.tripTuples:
            if (self._isDoubleRoute(trip)):
                if (self.timeMode == Mode.startTime):
                    (route, startTrip, endTrip) = trip
                elif (self.timeMode == Mode.arrivalTime):
                    (route, endTrip, startTrip) = trip
                startID = ObjectId()
                endID = ObjectId()
                switchBusStop = startTrip["trajectory"][route[DR_END1]]["busStop"]
                entryStart = {
                        "_id": startID,
                        "userID" : self.userID,
                        "line": route[DR_LINE1],
                        "busID": startTrip["busID"],
                        "startBusStop": self.startBusStop,
                        "endBusStop": switchBusStop,
                        "startTime": departureTime,
                        "endTime": startTrip["trajectory"][route[DR_END1]]["time"],
                        "requestTime": self.requestTime,
                        "feedback": -1,
                        "requestID": self.requestID,
                        "next": endID,
                        "booked": False
                }
                started = False
                trajectory = []
                for stop in startTrip["trajectory"]:
                    if (stop["busStop"] == self.startBusStop):
                        started = True
                    if (not started):
                        continue
                    started = True
                    trajectory.append(stop["busStop"])
                    if (stop["busStop"] == switchBusStop):
                        break
                entryStart["trajectory"] = trajectory

                entryEnd = {
                        "_id": endID,
                        "userID" : self.userID,
                        "line": route[DR_LINE2],
                        "busID": endTrip["busID"],
                        "startBusStop": endTrip["trajectory"][route[DR_START2]]["busStop"],
                        "endBusStop": self.endBusStop,
                        "startTime": endTrip["trajectory"][route[DR_START2]]["time"],
                        "endTime": arrivalTime,
                        "requestTime": self.requestTime,
                        "feedback": -1,
                        "requestID": self.requestID,
                        "booked": False
                }
                started = False
                trajectory = []
                for stop in endTrip["trajectory"]:
                    if (stop["busStop"] == switchBusStop):
                        started = True
                    if (not started):
                        continue
                    started = True
                    trajectory.append(stop["busStop"])
                    if (stop["busStop"] == self.endBusStop):
                        break
                entryEnd["trajectory"] = trajectory
                newEntry = [entryStart, entryEnd]

            else:
                userTripID = ObjectId()
                entry = {
                        "_id": userTripID,
                        "userID": self.userID,
                        "line": trip["line"],
                        "busID": trip["busID"],
                        "startBusStop": self.startBusStop,
                        "endBusStop": self.endBusStop,
                        "startTime": departureTime,
                        "endTime": arrivalTime,
                        "requestTime": self.requestTime,
                        "feedback": -1,
                        "requestID": self.requestID,
                        "booked": False
                }
                started = False
                trajectory = []
                for stop in trip["trajectory"]: 
                    if (stop["busStop"] == self.startBusStop):
                        started = True
                    if (not started):
                        continue
                    trajectory.append(stop["busStop"])
                    if (stop["busStop"] == self.endBusStop):
                        started = False
                        break
                entry["trajectory"] = trajectory
                newEntry = [entry]
            i += 1
            entryList.extend(newEntry)
            self.userTripDict[i] = newEntry
        if (entryList != []):
            self.userTrip.insert_many(entryList)

    def _convertToJson(self):
        self.jsonObject = {}
        for ut in self.userTripDict:
            entries = []
            for entry in self.userTripDict[ut]:
                newEntry = {
                        "_id": str(entry["_id"]),
                        "userID" : entry["userID"],
                        "line": entry["line"],
                        "busID": entry["busID"],
                        "startBusStop": str(entry["startBusStop"]),
                        "endBusStop": str(entry["endBusStop"]),
                        "startTime": str(entry["startTime"]),
                        "endTime": str(entry["endTime"]),
                        "requestTime": str(entry["requestTime"]),
                        "feedback": -1,
                        "requestID": str(entry["requestID"]),
                        "booked": False
                }
                if ("next" in entry):
                    newEntry["next"] = str(entry["next"])
                trajectory = []
                for stop in entry["trajectory"]:
                    trajectory.append(str(stop))
                newEntry["trajectory"] = trajectory
                entries.append(newEntry)
            self.jsonObject[ut] = entries


    def getBestRoutes(self, requestID, mode = Mode.tripTime):
        self.requestID = requestID
        self.routeMode = mode
        self._findFittingRoutes()
        
        if ((self.fittingRoutes == []) and (self.doubleRoutes == [])):
            if (self.debug):
                print "No fitting routes found"
            return None
        if (self.debug):
            print "Found " + str(len(self.fittingRoutes)) + "/" + str(len(self.doubleRoutes)) + \
                    " fitting/double Routes"

        self._findBestRoute()
        if (self.debug):
            print "Found " + str(len(self.tripTuples)) + " tripTuples"

        if (self.tripTuples == []):
            if (self.debug):
                print "No best route found"
            return None

        self._updateDatabase()
        self._convertToJson()

        return self.jsonObject


