# -*- coding: utf-8 -*-
import bson
import datetime
import pymongo
import sys
import cProfile, pstats

from planner import TravelPlanner, Mode
from bson.objectid import ObjectId
from pymongo import MongoClient
from subprocess import call

class tester:

    def __init__(self):
        print ("Setting up test system...")
        client = MongoClient()
        self.db = client.monad

        busStops = self.db.BusStop.find()
        self.busStopDict = {}
        for stop in busStops:
            self.busStopDict[stop["name"]] = stop

        print ("Running UnitTests...")
        call(["python", "test_planner.py"])

    def test(self, start, end, time, timeMode, routeMode, profiling = False):
        self.tp = TravelPlanner(self.db)
        print ("Testing...")
        request = {
                "_id": ObjectId(),
                "userID": 4711,
                "requestTime": datetime.datetime.utcnow()
        }
        request["startBusStop"] = self.busStopDict[start]["_id"]
        request["endBusStop"] = self.busStopDict[end]["_id"]
        request["startPositionLatitude"] = self.busStopDict[start]["latitude"]
        request["startPositionLongitude"] = self.busStopDict[start]["longitude"]
        request["endPositionLatitude"] = self.busStopDict[end]["latitude"]
        request["endPositionLongitude"] = self.busStopDict[end]["longitude"]
        if (timeMode == Mode.startTime):
            request["startTime"] = time
            request["endTime"] = "null"
        elif (timeMode == Mode.arrivalTime):
            request["startTime"] = "null"
            request["endTime"] = time
        else:
            print ("Error while preparing the test: timeMode is " + str(timeMode))
            return None
        print ("Request ID: " + str(request["_id"]))
        self.db.TravelRequest.insert_one(request)

        if (profiling):
            pr = cProfile.Profile()
            pr.enable()
            json = self.tp.getBestRoutes(request["_id"], routeMode)
            pr.disable()
            pstats.Stats(pr).print_stats('planner')
        else:
            json = self.tp.getBestRoutes(request["_id"], routeMode)
        return json

    def printBestResult(self, jsonObject):
        if (jsonObject == None or jsonObject == {}):
            print ("No route found!")
            return
        best = jsonObject[1]
        trip = "Route from " + best[0]["startBusStop"] + " to " + best[-1]["endBusStop"]
        time = "Trip starts at " + best[0]["startTime"] + " and ends at " + best[-1]["endTime"]
        line = "Taking line " + str(best[0]["line"])
        if (len(best) > 1):
            for i in range(1, len(best)):
                trip += " via " + best[i]["startBusStop"]
                line += " and " + str(best[i]["line"])
                if (i < len(best)):
                    time += ". Waiting at intermediate busstop from " + best[i - 1]["endTime"] + \
                            " to " + best[i]["startTime"]
        print (trip)
        print (time)
        print (line)

    def printJson(self, jsonObject):
        if (jsonObject == None or jsonObject == {}):
            print ("No route found!")
            return
        best = jsonObject[1]
        route = "Route from " + best[0]["startBusStop"] + " to " + best[-1]["endBusStop"]
        print (route)
        for key in jsonObject.keys():
            tripLine = 'Trip ' + str(key)
            print (tripLine)
            for trip in jsonObject[key]:
                tour = "From " + trip["startBusStop"] + " to " + trip["endBusStop"]
                time = "Start " + str(trip["startTime"]) + " until " + str(trip["endTime"])
                line = "Used line " + str(trip["line"])
                print (tour)
                print (time)
                print (line)

