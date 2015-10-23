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

from pymongo import MongoClient

NUM_OF_ROUTES_RETURNED = 5
RT_ROUTE = 0
RT_ARRIVAL_TIME = 1
RT_TIME_DIFFERENCE = 1
RT_DEPARTURE_TIME = 2
RT_ARRIVAL_TIME = 3
POS_LATITUDE  = 0
POS_LONGITUDE = 1

# Dummy class, will be used for the moment until the real RA is ready
import random
class RouteAdministrator:
    def __init__(self):
        pass

    def getBusStop(self, Latitude, Longitude):
        availableStops = ["Flogsta Centrum", "Sernanders vag", "Ekeby hus", "Oslogatan", 
                          "Studentstaden", "Ekonomikum", "Gotgatan", "Skolgatan"]
        return random.choice(availableStops)

    def getBusStopPosition(self, name):
        return (2.3, 1.4)

class Mode:
    tripTime = 1
    waitTime = 2
    startTime   = 3
    arrivalTime = 4

class TravelPlanner:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.monad
        self.fittingRoutes = []
        self.startingWaypoint = []
        self.endingWaypoint = []
        self.routeList = []
        self.counter = 0


    def _findFittingRoutes(self):
        request = self.db.TravelRequest.find_one({"_id": self.requestID})
        self.startPositionLat = request["startPositionLatitude"]
        self.startPositionLon = request["startPositionLongitude"]
        self.endPositionLat   = request["endPositionLatitude"]
        self.endPositionLon   = request["endPositionLongitude"]

        #TODO: Use real RouteAdministrator
        ra = RouteAdministrator()
        self.startBusStop = ra.getBusStop(self.startPositionLat, startPositionLon)
        self.endBusStop   = ra.getBusStop(self.endPositionLat, endPositionLon)
        self.startBusStopPosition = ra.getBusStopPosition(self.startBusStop)
        self.endBusStopPosition   = ra.getBusStopPosition(self.endBusStop)

        if (request["startTime"] == "null"):
            self.startTime = 0
            self.endTime   = request["EndTime"]
            self.timeMode  = Mode.arrivalTime
        elif (request["endTime"] == "null"):
            self.startTime = request["StartTime"]
            self.endTime   = 0
            self.timeMode  = Mode.startTime
        else:
            return

        cursor = self.db.Route.find({"stop.name": self.startBusStop, "stop.name": self.endBusStop})
        for route in cursor:
            self.fits = False
            for i in range(len(route["stop"])):
                if (route["stop"][i]["name"] == self.startBusStop):
                    self.startingWaypoint.append(i)
                    self.fittingRoutes.append(route)
                    self.fits = True
                elif (route["stop"][i]["name"] == self.endBusStop):
                    if (self.fits):
                        self.endingWaypoint.append(i)
                    break

   
    def _isBetterTrip(self, i):
        if (self.timeMode == Mode.startTime):
            if (self.timeToArrival <= self.tripTuples[i][RT_ARRIVAL_TIME]):
                if (self.dptTime < self.tripTuples[i][RT_DEPARTURE_TIME]):
                    if (self.routeMode == Mode.tripTime):
                        return True
                else:
                    if (self.routeMode == Mode.waitTime):
                        return True
        elif (self.timeMode == Mode.arrivalTime):
            if (self.diffToArrTime <= self.tripTuples[i][RT_TIME_DIFFERENCE]):
                if (self.dptTime > self.tripTuples[i][RT_DEPARTURE_TIME]):
                    if (self.routeMode == Mode.tripTime):
                        return True
                else:
                    if (self.routeMode == Mode.waitTime):
                        return True
        return False

    def _rankTrip(self, trip):
        for i in range(len(self.tripTuples)):
            if (self._isBetterTrip(i)):
                if (self.timeMode == Mode.startTime):
                    self.tripTuples.insert(i, 
                            (trip, self.timeToArrival, self.dptTime, self.arrTime))
                elif (self.timeMode == Mode.arrivalTime):
                    self.tripTuples.insert(i, 
                            (trip, self.diffToArrTime, self.dptTime, self.arrTime))
                self.tripProcessed = True
                break
            if (i > NUM_OF_ROUTES_RETURNED):
                self.tripProcessed = True
                break
        if (self.tripProcessed == False):
            if (self.timeMode == Mode.startTime):
                self.tripTuples.append((trip, self.timeToArrival, self.dptTime, self.arrTime))
            elif (self.timeMode == Mode.arrivalTime):
                self.tripTuples.append((trip, self.diffToArrTime, self.dptTime, self.arrTime))

    def _insertTrip(self, trip):
        self.tripProcessed = False
        self.dptTime = trip["busstops"][self.startingWaypoint[self.counter]]["time"]
        self.arrTime = trip["busstops"][self.endingWaypoint[self.counter]]["time"]
        
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

    def _findBestRoute(self):
        self.counter = 0
        self.tripTuples = []
        for route in self.fittingRoutes:
            self.timeTable = db.timeTable.find_one({"line": route["line"]})
            for trip in self.timeTable["timetable"]:
                for stop in trip["busstops"]:
                    if (self.timeMode == Mode.startTime):
                        if (stop["busstop"] == self.startBusStop):
                            if (stop["time"] > self.startTime):
                                self._insertTrip(trip)
                    elif (self.timeMode == Mode.arrivalTime):
                        if (stop["busstop"] == self.endBusStop):
                            if (stop["time"] < self.endTime):
                                self._insertTrip(trip)

            self.counter = self.counter + 1


    def _updateDatabase(self):
        self.entryList = []
        self.userTripList = []
        i = 0
        for (trip, timeDiff, dptTime, arrTime) in self.tripTuples:
            userTripID = ObjectId()
            newEntry = {
                    "_id": userTripID,
                    "travelRequest": self.requestID,
                    "busId": trip["busId"],
                    "startTime": dptTime,
                    "endTime": arrTime,
                    "trajectory": [
                        {
                            "latitude":  self.startBusStopPosition[POS_LATITUDE],
                            "longitude": self.startBusStopPosition[POS_LONGITUDE],
                            "name": self.startBusStop
                        },
                        {
                            "latitude":  self.endBusStopPosition[POS_LATITUDE],
                            "longitude": self.endBusStopPosition[POS_LONGITUDE],
                            "name": self.endBusStop
                        }
                    ]
            }
            i += 1
            self.entryList.append(newEntry)
            self.userTripList.append(userTripID)
            if (i >= NUM_OF_ROUTES_RETURNED):
                break
        db.UserTrip.insert_many(entryList)


    def getBestRoutes(self, requestID, mode = Mode.tripTime):
        self.requestID = requestID
        self.routeMode = mode
        self._findFittingRoutes()
        
        if (self.fittingRoutes == []):
            return []

        self._findBestRoute()

        self._updateDatabase()

        return self.userTripList[:NUM_OF_ROUTES_RETURNED]


