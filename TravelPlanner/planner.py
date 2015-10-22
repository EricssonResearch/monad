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
import random

from pymongo import MongoClient

NUM_OF_ROUTES_RETURNED = 5
RT_ROUTE = 0
RT_ARRIVAL_TIME = 1
RT_DEPARTURE_TIME = 2
RT_TIME_DIFFERENCE = 1
RT_ARRIVAL_TIME = 3

class RouteAdministrator:

    def __init__(self):
        pass

    def getBusStop(self, Latitude, Longitude):
        availableStops = ["Flogsta Centrum", "Sernanders vag", "Ekeby hus", "Oslogatan", 
                          "Studentstaden", "Ekonomikum", "Gotgatan", "Skolgatan"]
        return random.choice(availableStops)

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


    def _startpointFits(self, dptTime):
        if ((self.timeMode == Mode.startTime) and (self.startTime < dptTime)):
            return True
        elif ((self.timeMode == Mode.arrivalTime) and (self.endTime > dptTime)):
            return True
        return False

    def _endpointFits(self, dptTime):
        if (self.fits):
            if ((self.timeMode == Mode.arrivalTime) and (self.endTime > dptTime)):
                del self.startingWaypoint[-1]
                del self.fittingRoutes[-1]
                return False
            return True
        return False

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


    def _isBetterRoute(self, i):
        if (self.timeMode == Mode.startTime):
            if (self.timeToArrival <= self.routeTuples[i][RT_ARRIVAL_TIME]):
                if (self.dptTime < self.routeTuples[i][RT_DEPARTURE_TIME]):
                    if (self.routeMode == Mode.tripTime):
                        return True
                else:
                    if (self.routeMode == Mode.waitTime):
                        return True
        elif (self.timeMode == Mode.arrivalTime):
            if (self.diffToArrTime <= self.routeTuples[i][RT_TIME_DIFFERENCE]):
                if (self.dptTime > self.routeTuples[i][RT_DEPARTURE_TIME]):
                    if (self.routeMode == Mode.tripTime):
                        return True
                else:
                    if (self.routeMode == Mode.waitTime):
                        return True
        return False

    def _rankRoute(self):
        for i in range(len(self.routeTuples)):
            if (self._isBetterRoute(i)):
                if (self.timeMode == Mode.startTime):
                    self.routeTuples.insert(i, 
                            (route, self.timeToArrival, self.dptTime, self.arrTime))
                elif (self.timeMode == Mode.arrivalTime):
                    self.routeTuples.insert(i, 
                           (route, self.diffToArrTime, self.dptTime, self.arrTime))
                self.routeProcessed = True
                break
            if (i > NUM_OF_ROUTES_RETURNED):
                self.routeProcessed = True
                break
        if (self.routeProcessed == False):
            if (self.timeMode == Mode.startTime):
                self.routeTuples.append((route, self.timeToArrival, self.dptTime, self.arrTime))
            elif (self.timeMode == Mode.arrivalTime):
                self.routeTuples.append((route, self.diffToArrTime, self.dptTime, self.arrTime))

    def _insertRoute(self, route):
        self.routeProcessed = False
        self.dptTime = route["Waypoints"][self.startingWaypoint[self.counter]]["DptTime"]
        self.arrTime = route["Waypoints"][self.endingWaypoint[self.counter]]["DptTime"]

        if (self.timeMode == Mode.startTime):
            self.timeToArrival = self.arrTime - self.startTime
            if (self.routeTuples == []):
                self.routeTuples.append((route, self.timeToArrival, self.dptTime, self.arrTime))
                return
            self._rankRoute()

        elif (self.timeMode == Mode.arrivalTime):
            self.diffToArrTime = self.endTime - self.arrTime
            if (self.routeTuples == []):
                self.routeTuples.append((route, self.diffToArrTime, self.dptTime, self.arrTime))
                return
            self._rankRoute()

    def _findBestRoute(self):
        self.counter = 0
        self.routeTuples = []
        for route in self.fittingRoutes:
            self._insertRoute(route)
            self.counter = self.counter + 1

        for route in self.routeTuples:
            self.routeList.append(route[RT_ROUTE])


    def _updateDatabase(self):
        self.entryList = []
        for route in self.routeTuples:
            newEntry = {
                    "_id": ObjectId(),
                    "travelRequest": self.requestID }

    def getBestRoutes(self, requestID, mode = Mode.tripTime):
        self.requestID = requestID
        self.routeMode = mode
        self._findFittingRoutes()
        
        if (self.fittingRoutes == []):
            return []

        self._findBestRoute()

        self._updateDatabase()

        return self.routeList[:NUM_OF_ROUTES_RETURNED]


