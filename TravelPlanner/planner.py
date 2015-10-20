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

class Mode:
    tripTime = 1
    waitTime = 2
    startTime   = 3
    arrivalTime = 4

class TravelPlanner:

    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.monad
        self.busStops = []
        self.busStopIDs = []
        self.fittingRoutes = []
        self.startingWaypoint = []
        self.endingWaypoint = []
        self.minTimeDiff = datetime.timedelta.max
        self.bestRouteStartTime = datetime.datetime(2015, 1, 1)
        self.bestTravelTime = datetime.timedelta.max
        self.counter = 0

        cursor = self.db.BusStopLocation.find({"Available": 1})
        for stop in cursor:
            self.busStops.append([stop["Longitude"], stop["Latitude"]])
            self.busStopIDs.append(stop["_id"])


    def _updateTimeTableDB(self):
        for point in self.bestRoute["Waypoints"]:
            if (point["BusStopID"] == self.startID):
                point["PsgGetOn"] += 1
            if (point["BusStopID"] == self.endID):
                point["PsgGetOff"] += 1
                break
        updated = self.db.TimeTable.update_one(
            {"_id": self.bestRoute["_id"]},
            {"$set": {"Waypoints": self.bestRoute["Waypoints"]}})

    def _updateRequestDB(self):
        updated = self.db.TravelRequest.update_one(
            {"_id": self.requestID},
            {"$set": {
                "AssignedRoute.StartID": self.startID,
                "AssignedRoute.EndID":   self.endID,
                "AssignedRoute.RouteID": self.bestRoute["_id"],
                "Duration": self.bestTravelTime.total_seconds() 
                }
            })


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
        self.startPosition = request["StartPosition"]
        self.endPosition   = request["EndPosition"]
        self.startID = self.busStopIDs[self.busStops.index(self.startPosition)]
        self.endID   = self.busStopIDs[self.busStops.index(self.endPosition)]
        if (request["StartTime"] == ""):
            self.startTime = 0
            self.endTime   = request["EndTime"]
            self.timeMode  = Mode.arrivalTime
        else:
            self.startTime = request["StartTime"]
            self.endTime   = 0
            self.timeMode  = Mode.startTime

        cursor = self.db.TimeTable.find({"Waypoints.BusStopID": self.endID, 
            "StartBusstop": {"$ne": self.endPosition}})
        for route in cursor:
            self.fits = False
            for i in range(len(route["Waypoints"])):
                if (route["Waypoints"][i]["BusStopID"] == self.startID):
                    if (self._startpointFits(route["Waypoints"][i]["DptTime"])):
                        self.startingWaypoint.append(i)
                        self.fittingRoutes.append(route)
                        self.fits = True
                elif (route["Waypoints"][i]["BusStopID"] == self.endID):
                    if (self._endpointFits(route["Waypoints"][i]["DptTime"])):
                        self.endingWaypoint.append(i)
                    break

    def _findBestRoute(self):
        self.bestRoute = self.fittingRoutes[0]
        self.counter = 0
        for route in self.fittingRoutes:
            self.arrTime = route["Waypoints"][self.endingWaypoint[self.counter]]["DptTime"]
            self.dptTime = route["Waypoints"][self.startingWaypoint[self.counter]]["DptTime"]
            self.travelTime = self.arrTime - self.dptTime
            self.timeToArrival = self.arrTime - self.startTime

            if (self.timeToArrival <= self.minTimeDiff):
                if (self.routeMode == Mode.tripTime):
                    if (self.dptTime > self.bestRouteStartTime):
                        self.bestRoute = route
                        self.minTimeDiff = self.timeToArrival
                        self.bestRouteStartTime = self.dptTime
                        self.bestTravelTime = self.travelTime
                elif (self.routeMode == Mode.waitTime):
                    if (self.dptTime < self.bestRouteStartTime):
                        self.bestRoute = route
                        self.minTimeDiff = self.timeToArrival
                        self.bestRouteStartTime = self.dptTime
                        self.bestTravelTime = self.travelTime
            self.counter = self.counter + 1


    def getBestRoute(self, requestID, mode = Mode.tripTime):
        self.requestID = requestID
        self.routeMode = mode
        self._findFittingRoutes()
        
        if (self.fittingRoutes == []):
            return []

        self._findBestRoute()

        self._updateRequestDB()
        self._updateTimeTableDB()

        return [self.bestRoute]


