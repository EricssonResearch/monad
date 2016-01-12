# -*- coding: utf-8 -*-
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
NUM_OF_ROUTES_RETURNED  = 5
MAXIMUM_NUMBER_OF_LINES = 150
MAXIMUM_TIME_DIFFERENCE = datetime.timedelta(hours = 3)
TIME_DIFF_15MIN         = datetime.timedelta(minutes = 15)
MAX_SEARCH_DEPTH        = 7
FIRST                   = 0
LAST                    = -1
# tripTuple
TT_ROUTE           = 0
TT_TIME_DIFFERENCE = 1
TT_DEPARTURE_TIME  = 2
TT_ARRIVAL_TIME    = 3
# partialRoutes
PR_ROUTE = 0
PR_START = 1
PR_END   = 2
PR_LINE  = 3
# end of constants


class Mode:
    tripTime = 1
    waitTime = 2
    startTime   = 3
    arrivalTime = 4

# Documentation at the end of the file
class TravelPlanner:

    def __init__(self, client):
        self.db = client
        self.travelRequest = self.db.TravelRequest
        self.route = self.db.Route
        self.timeTable = self.db.TimeTable
        self.userTrip = self.db.UserTrip
        self.busTrip = self.db.BusTrip
        self.busStop = self.db.BusStop
        self.busStops = self._getBusStops()

    def _prepareSearch(self):
        self.singleRoutes   = []
        self.multiRoutes    = []
        self.possibleRoutes = []
        self.tripTuples     = []
        self.lineTuples     = []
        self.lineSchedules  = []

        for i in range(MAXIMUM_NUMBER_OF_LINES):
            self.lineSchedules.append(None)


################### Finding fitting Routes ########################################################

    def _range(self, length):
        return range(length - 2, -1, -1)

    def _searchLastRoute(self, busLine, busStopID):
        cursor = self.route.find({"$and": [
                {"trajectory.busStop": busStopID}, 
                {"trajectory.busStop": self.endBusStop},
                {"date": self.searchDay},
                {"line": {"$ne": busLine}},
                {"trajectory.busStop": {"$nin": [self.startBusStop]}}]})
        if (cursor is None):
            return []
        possibilities = []
        startNumber = 0
        for route in cursor:
            fits = False
            for stopNo in range(len(route["trajectory"])):
                if (route["trajectory"][stopNo]["busStop"] == busStopID):
                    fits = True
                    startNumber = stopNo
                elif (route["trajectory"][stopNo]["busStop"] == self.endBusStop):
                    if (fits):
                        possibilities.append((route, startNumber, stopNo, route["line"]))
                        if (self.foundPossibility == MAX_SEARCH_DEPTH):
                            self.foundPossibility = self.noSwitches
                    break
        return possibilities
            
    def _searchIntermediate(self, busLine, searchLevel, busStopID, previousStop):
        self.noSwitches += 1
        middleLines = self.route.find({"$and": [
                {"trajectory.busStop": busStopID},
                {"date": self.searchDay},
                {"line": {"$ne": busLine}},
                {"trajectory.busStop": {"$nin": [self.startBusStop, self.endBusStop, 
                        previousStop]}}]})
        if (middleLines is None):
            return []
        possible = []
        startNumber = 0
        for route in middleLines:
            fits = False
            for stopNo in range(len(route["trajectory"])):
                if (fits):
                    if (self.noSwitches == searchLevel):
                        third = self._searchLastRoute(route["line"], 
                                route["trajectory"][stopNo]["busStop"])
                    else:
                        third = self._searchIntermediate(route["line"], searchLevel,
                                route["trajectory"][stopNo]["busStop"],
                                route["trajectory"][stopNo - 1]["busStop"])
                    if (third == []):
                        continue
                    for last in third:
                        middle = (route, startNumber, stopNo, route["line"])
                        if (isinstance(last, tuple)):
                            possible.append([middle, last])
                        else:
                            tempList = [middle]
                            for entry in last:
                                tempList.append(entry)
                            possible.append(tempList)
                elif (route["trajectory"][stopNo]["busStop"] == busStopID):
                    fits = True
                    startNumber = stopNo
        self.noSwitches -= 1
        return possible

    def _searchMulti(self):
        for level in range(2, MAX_SEARCH_DEPTH):
            if (level > (self.foundPossibility + 1)):
                break
            firstLines = self.route.find({"trajectory.busStop": self.startBusStop,
                    "date": self.searchDay})
            for firstLine in firstLines:
                maybe = False
                startNumber = 0
                for stopNo in range(len(firstLine["trajectory"])):
                    if (firstLine["trajectory"][stopNo]["busStop"] == self.startBusStop):
                        maybe = True
                        startNumber = stopNo
                    elif (maybe):
                        self.noSwitches = 1
                        options = self._searchIntermediate(firstLine["line"], level,
                                firstLine["trajectory"][stopNo]["busStop"],
                                firstLine["trajectory"][stopNo - 1]["busStop"])
                        if (options == []):
                            continue
                        for entry in options:
                            temp = [(firstLine, startNumber, stopNo, firstLine["line"])]
                            temp.extend(entry)
                            self.multiRoutes.append(temp)

    def _findFittingRoutes(self):
        self.foundPossibility = MAX_SEARCH_DEPTH
        request = self.travelRequest.find_one({"_id": self.requestID})
        self.startBusStop = request["startBusStop"]
        self.endBusStop   = request["endBusStop"]
        self.userID       = request["userID"]
        self.requestTime  = request["requestTime"]

        if (request["endTime"] == "null"):
            self.startTime = request["startTime"]
            self.endTime   = 0
            self.timeMode  = Mode.startTime
            self.searchDay = request["startTime"].replace(hour = 0, minute = 0, second = 0)
        elif (request["startTime"] == "null"):
            self.startTime = 0
            self.endTime   = request["endTime"]
            self.timeMode  = Mode.arrivalTime
            self.searchDay = request["endTime"].replace(hour = 0, minute = 0, second = 0)
        else:
            return

        cursor = self.route.find({"trajectory.busStop": self.startBusStop,
                "trajectory.busStop": self.endBusStop, "date": self.searchDay})
        for route in cursor:
            fits = False
            startNumber = 0
            for i in range(len(route["trajectory"])):
                if (route["trajectory"][i]["busStop"] == self.startBusStop):
                    startNumber = i
                    fits = True
                elif (route["trajectory"][i]["busStop"] == self.endBusStop):
                    if (fits):
                        self.singleRoutes.append([(route, startNumber, i, route["line"])])
                        self.foundPossibility = 0
                    break

        startLines = self.route.find({"$and": [
                {"trajectory.busStop": self.startBusStop},
                {"date": self.searchDay},
                {"trajectory.busStop": {"$nin": [self.endBusStop]}}]})
        for startLine in startLines:
            maybe = False
            startNumber = 0
            for i in range(len(startLine["trajectory"])):
                if (startLine["trajectory"][i]["busStop"] == self.startBusStop):
                    maybe = True
                    startNumber = i
                elif (startLine["trajectory"][i]["busStop"] == self.endBusStop):
                    break
                elif (maybe):
                    self.noSwitches = 1
                    self.possibleRoutes = self._searchLastRoute(startLine["line"], 
                            startLine["trajectory"][i]["busStop"])
                    if (self.possibleRoutes == []):
                        continue
                    for entry in self.possibleRoutes:
                        self.multiRoutes.append([(startLine, startNumber, i, startLine["line"]),
                                entry])
                        if (self.foundPossibility == MAX_SEARCH_DEPTH):
                            self.foundPossibility = 1

        if (self.singleRoutes == []):
            self._searchMulti()


################### Evaluate found Routes ######################

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
            if (not self._isBetterTrip(LAST)):
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

    def _getBusTrips(self, line):
        if (self.lineSchedules[line] == None):
            ttColl = self.timeTable.find_one({"line": line, "date": self.searchDay})
            if (ttColl == None):
                trips = []
            else:
                trips = list(self.busTrip.find({"_id": {"$in": ttColl["timetable"]}}))
                self.lineSchedules[line] = trips
        else:
            trips = self.lineSchedules[line]
        return trips

    def _findNextTrip(self, route, part, arrSwitch):
        trips = self._getBusTrips(route[part][PR_LINE])
        bestArrivalTime = datetime.datetime.max
        bestNextTrip    = None
        for trip in trips:
            dptSwitch = trip["trajectory"][route[part][PR_START]]["time"]
            arrTime   = trip["trajectory"][route[part][PR_END]]["time"]
            if ((arrSwitch < dptSwitch) and (arrTime < bestArrivalTime)):
                bestNextTrip = trip
                bestArrivalTime = arrTime
        return (bestNextTrip, bestArrivalTime)

    def _findPreviousTrip(self, route, part, dptSwitch):
        trips = self._getBusTrips(route[part][PR_LINE])
        bestDepartureTime = datetime.datetime.min
        bestPreviousTrip  = None
        for trip in trips:
            dptTime   = trip["trajectory"][route[part][PR_START]]["time"]
            arrSwitch = trip["trajectory"][route[part][PR_END]]["time"]
            if ((arrSwitch < dptSwitch) and (dptTime > bestDepartureTime)):
                bestPreviousTrip = trip
                bestDepartureTime = dptTime
        return (bestPreviousTrip, bestDepartureTime)

    def _isFastRoute(self):
        if (len(self.tripTuples) > 0):
            departure = self.tripTuples[0][TT_DEPARTURE_TIME]
            arrival = self.tripTuples[0][TT_ARRIVAL_TIME]
            if ((arrival - departure) < TIME_DIFF_15MIN):
                return True
        return False

    def _findBestRoute(self):
        counter = 0
        for route in self.singleRoutes:
            trips = self._getBusTrips(route[FIRST][PR_LINE])
            for trip in trips:
                self.dptTime = trip["trajectory"][route[FIRST][PR_START]]["time"]
                self.arrTime = trip["trajectory"][route[FIRST][PR_END]]["time"]
                if (self.timeMode == Mode.startTime):
                    if ((self.dptTime > self.startTime) and 
                            (self.dptTime < (self.startTime + MAXIMUM_TIME_DIFFERENCE))):
                        self._insertTrip((route, [trip]))
                elif (self.timeMode == Mode.arrivalTime):
                    if ((self.arrTime < self.endTime) and 
                            (self.arrTime > (self.endTime - MAXIMUM_TIME_DIFFERENCE))):
                        self._insertTrip((route, [trip]))

            counter += 1

        if (self._isFastRoute()):
            return

        for route in self.multiRoutes:
            tempList = []
            for i in range(len(route)):
                tempList.append(route[i][PR_LINE])
            if (tempList in self.lineTuples):
                continue
            else:
                self.lineTuples.append(tempList)

            if (self.timeMode == Mode.startTime):
                trips = self._getBusTrips(route[FIRST][PR_LINE])
                for trip in trips:
                    self.dptTime = trip["trajectory"][route[FIRST][PR_START]]["time"]
                    arrSwitch    = trip["trajectory"][route[FIRST][PR_END]]["time"]
                    if ((self.dptTime > self.startTime) and 
                            (self.dptTime < (self.startTime + MAXIMUM_TIME_DIFFERENCE))):
                        tripList = [trip]
                        for i in range(1, len(route)):
                            (nextTrip, arrSwitch) = self._findNextTrip(route, i, arrSwitch)
                            tripList.append(nextTrip)
                        self.arrTime = arrSwitch
                        self._insertTrip((route, tripList))

            elif (self.timeMode == Mode.arrivalTime):
                trips = self._getBusTrips(route[LAST][PR_LINE])
                for trip in trips:
                    dptSwitch    = trip["trajectory"][route[LAST][PR_START]]["time"]
                    self.arrTime = trip["trajectory"][route[LAST][PR_END]]["time"]
                    if ((self.arrTime < self.endTime) and 
                            (self.arrTime > (self.endTime - MAXIMUM_TIME_DIFFERENCE))):
                        tripList = [trip]
                        for i in self._range(len(route)):
                            (prevTrip, dptSwitch) = self._findPreviousTrip(route, i, dptSwitch)
                            tripList.insert(FIRST, prevTrip)
                        self.dptTime = dptSwitch
                        self._insertTrip((route, tripList))


################### Process Results ######################

    def _getBusStops(self):
        busStopDict = {}
        stops = self.busStop.find()
        for stop in stops:
            busStopDict[stop["_id"]] = stop["name"]
        return busStopDict

    def _updateDatabase(self):
        entryList = []
        self.userTripDict = {}
        rank = 0
        for ((route, trips), timeDiff, departureTime, arrivalTime) in self.tripTuples:
            newEntry = []
            IDList = []
            for i in range(len(trips)):
                IDList.append(ObjectId())
            ctr = 0
            for trip in trips:
                startStopID = trip["trajectory"][route[ctr][PR_START]]["busStop"]
                endStopID   = trip["trajectory"][route[ctr][PR_END]]["busStop"]
                entry = {
                        "_id": IDList[ctr],
                        "userID" : self.userID,
                        "line": route[ctr][PR_LINE],
                        "busID": trip["busID"],
                        "startBusStop": self.busStops[startStopID],
                        "endBusStop": self.busStops[endStopID],
                        "startTime": trip["trajectory"][route[ctr][PR_START]]["time"],
                        "endTime": trip["trajectory"][route[ctr][PR_END]]["time"],
                        "requestTime": self.requestTime,
                        "feedback": -1,
                        "requestID": self.requestID,
                        "busTripID": trip["_id"],
                        "booked": False
                }
                if (len(trips) > (ctr + 1)):
                    entry["next"] = IDList[ctr + 1]
                started = False
                trajectory = []
                for stop in trip["trajectory"]:
                    if (stop["busStop"] == startStopID):
                        started = True
                    if (not started):
                        continue
                    trajectory.append(self.busStops[stop["busStop"]])
                    if (stop["busStop"] == endStopID):
                        break
                entry["trajectory"] = trajectory
                newEntry.append(entry)
                ctr += 1
            
            rank += 1
            entryList.extend(newEntry)
            self.userTripDict[rank] = newEntry
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
                        "startBusStop": entry["startBusStop"],
                        "endBusStop": entry["endBusStop"],
                        "startTime": str(entry["startTime"]),
                        "endTime": str(entry["endTime"]),
                        "requestTime": str(entry["requestTime"]),
                        "feedback": -1,
                        "requestID": str(entry["requestID"]),
                        "booked": False,
                        "busTripID": str(entry["busTripID"]),
                        "trajectory": entry["trajectory"]
                }
                if ("next" in entry):
                    newEntry["next"] = str(entry["next"])
                entries.append(newEntry)
            self.jsonObject[ut] = entries


################### Public interface ######################

    def getBestRoutes(self, requestID, mode = Mode.tripTime):
        self.requestID = requestID
        self.routeMode = mode
        self._prepareSearch()
        self._findFittingRoutes()
        
        if ((self.singleRoutes == []) and (self.multiRoutes == [])):
            return None

        self._findBestRoute()

        if (self.tripTuples == []):
            return None

        self._updateDatabase()
        self._convertToJson()

        return self.jsonObject


#################
# Documentation #
#################

# Constructor: TravelPlanner(database)
#  - Parameters: database: Database object
#  - Return value: TravelPlanner object
#
# Public function: userTripObject getBestRoutes(requestID, mode)
#  Parameters: 
#   - requestID: ID of the request, will be used to find the request in the database
#   - mode (default = Mode.tripTime): The mode the best route should be selected by,
#                either tripTime (shortest time in the bus) or waitTime (shortest time until the
#                bus starts from the selected waypoint). The preferred usage is through the Mode
#                class (see below).
#  Return value:
#   - userTripObject: A JSON object containing the userTrip items marking the recommended trips.
#                     The number of items is specified by the constant NUM_OF_ROUTES_RETURNED,
#                     which is currently 5. 
#
# Mode class
#  - tripTime = 1
#        Puts the focus on finding the shortest route for the client
#  - waitTime = 2
#        Puts the focus on the soonest begin of the journey
#  - startTime   = 3
#        Shows that the client wants to start as soon as possible after a given point of time
#  - arrivalTime = 4
#        Shows that the client wants to arrive before a certain point of time



