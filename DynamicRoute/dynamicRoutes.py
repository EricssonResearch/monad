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
__author__ = 'mohammad'
import random
import string
import collections
import datetime
import itertools
import numpy
import datetime
import sys
import math
sys.path.append('../OpenStreetMap')
sys.path.append('../LookAhead')
from datetime import timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from operator import itemgetter
from dbConnection import DB
import networkx as nx
import matplotlib.pyplot as plt
from bson.objectid import ObjectId
from routeGenerator import coordinates_to_nearest_stops, get_route

class DynamicRoutes():
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # INDEX
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Class variables
    # Constructor
    # Create Graph
    # Generate Dynamic Routes
    # Store Dynamic Routes into Database

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Class variables
    # ---------------------------------------------------------------------------------------------------------------------------------------
    server = "130.238.15.114"
    port = 27017
    database = "monad1"
    user = "monadStudent"
    password = "M0nad2015"
    dbClass = DB()

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Constructor
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def __init__(self):

       self.client = MongoClient("mongodb://" + self.user + ":" + self.password + "@" + self.server, self.port, maxPoolSize=200, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000)
       self.db = self.client[DB.database]
       
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Create Graph
    # ---------------------------------------------------------------------------------------------------------------------------------------

    def creategraph(self):
        '''
        create the Uppsala city graph from database of connected bus stops
        :return: graph
        '''
        DG = nx.DiGraph()
        collections = self.client.monad1.RouteGraph.find()
        for col in collections:
            if col['_id'] not in DG:
                DG.add_node(col['orgBusName'], name = col['_id'])
            for c in col['connectedBusStop']:
                if c['_id'] not in DG:
                    DG.add_node(c['busStop'], name = c['_id'])
                    DG.add_weighted_edges_from([(col['orgBusName'], c['busStop'], c['distance'])])
            DG.add_weighted_edges_from([(col['orgBusName'], c['busStop'], c['distance'])])
        return DG
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Generate Dynamic Routes
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def generateRoutes(self, DG, start_date, end_date):
        '''
        generate dynamic routes for Uppsala city based on users requests between start and end date
        :param DG: city graph
        :param start_date: start date for requests
        :param end_date: end date for requests
        :return:list of routes which serve all requests
        all routes start from central station and end in central station
        '''
        
        routes =[]
        routebusstopsdic ={}
        index = 0
        routesid =[]
        tempids=[]
        bus_allocated = 0
        busStops = self.client.monad1.BusStop.find()
        for stop in busStops:
            routebusstopsdic[stop['name']] = index
            index += 1
        tmatrix = numpy.zeros((busStops.count(), busStops.count()), dtype=numpy.int)
        reqs = self.dbClass.getRequestsFromDB(start_date, end_date)
        for req in reqs:
            i = routebusstopsdic[self.dbClass.getBusStopName(req[1])]
            j = routebusstopsdic[self.dbClass.getBusStopName(req[2])]
            if i != j:
                tmatrix[j][i] += 1
            else:
                tmatrix[j][i] = 0
        maxnumber = max(map(max, tmatrix))
        while maxnumber > 0:
            maxnumber = max(map(max, tmatrix))
            indx = numpy.where(tmatrix == maxnumber)
            Start_bus_stop = [key for key, value in routebusstopsdic.iteritems() if value == indx[0][0]]
            End_bus_stop = [key2 for key2, value in routebusstopsdic.iteritems() if value == indx[1][0]]
            try:
                if Start_bus_stop[0]!=End_bus_stop[0]:
                    bus_stops1 = nx.astar_path(DG, "Centralstationen", Start_bus_stop[0])
                    bus_stops2 = nx.astar_path(DG, Start_bus_stop[0], End_bus_stop[0], heuristic=None, weight='distance')
                    bus_stops3 = nx.astar_path(DG, End_bus_stop[0], "Centralstationen")
                    bus_stops = bus_stops1+bus_stops2 +bus_stops3
                    getin = 0
                    getout = 0
                    nbusstops = [bus_stops[0]]
                    intrip = []
                    outtrip = []
                    for i in range(1, len(bus_stops)):

                        if bus_stops[i-1] != bus_stops[i]:
                            nbusstops.append(bus_stops[i])
                    routes.append(nbusstops)
                    for i in range(0, len(nbusstops)):

                        getin = 0
                        getout = 0
                        for j in range(i, len(nbusstops)):
                            getin += tmatrix[routebusstopsdic[nbusstops[i]]][routebusstopsdic[nbusstops[j]]]
                            intrip.append([nbusstops[i], nbusstops[j], getin])
                        for l in range(0, i+1):
                            getout += tmatrix[routebusstopsdic[nbusstops[l]]][routebusstopsdic[nbusstops[i]]]
                    buscapacity = 100
                    temp =[]
                    bus_free=100
                    for k in range(0, len(intrip)):

                        if intrip[k][2] > 0 and bus_free > 0:
                            if bus_free >= intrip[k][2]:
                                bus_free = bus_free - intrip[k][2]
                                intrip[k][2] = 0
                                tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]] = 0
                                bus_allocated =bus_allocated + bus_free
                            else:
                                bus_free = 0
                                intrip[k][2] =intrip[k][2] - bus_free
                                tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]] = tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]] - bus_free
                                bus_allocated = bus_allocated + bus_free
                            temp.append([intrip[k][1], bus_free])
                        if intrip[k][0] in temp:
                            bus_free += temp[1]
                            bus_allocated =100 - bus_free
            except:nx.NetworkXNoPath

        client = MongoClient()
        client = MongoClient('130.238.15.114',27017)
        for i in routes:
            for j in range(0, len(i)):
                temp = client.monad1.BusStop.find_one({"name": i[j]})
                tempids.append(temp['_id'])
            routesid.append(tempids)
            tempids = []
        return routesid

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # store Dynamic Routes to database
    # ---------------------------------------------------------------------------------------------------------------------------------------
    def storeRoutesToDB(self,routes):
        '''store routes(a bus stop id list) from generateRoutes into DB, should be written to collection Routes
        for timebeing, it be stored into DynamicRoute for testing
        @param: routes: a list of new dynamic routes in list of bus stop id
        output: new route will be written into DynamicRoute 
        '''
        duration = 0
        line = 1
        trajectory = []
        tmpList = []
        todayDate = datetime.datetime.now()
        today = datetime.datetime(todayDate.year, todayDate.month, todayDate.day)        
        todayRoute = self.dbClass.db.dynamicRoute.find({'date': today})
        dictKey = ['interval', 'busStop']
        if todayRoute.count() == 0:
            print 'todays route is writing......'
            for i in range(len(routes)):
                for j in range(len(routes[i])):
                    if j == 0:
                        tmpList.append(0)
                    else:
                        adjointBusStopList = [(self.dbClass.getBusStopLongitudeByID(routes[i][j]), self.dbClass.getBusStopLatitudebyID(routes[i][j])), \
                                                (self.dbClass.getBusStopLongitudeByID(routes[i][j-1]), self.dbClass.getBusStopLatitudebyID(routes[i][j-1]))]
                        adjointBusStopRoute = get_route(adjointBusStopList)
                        interval = int(math.ceil(float(adjointBusStopRoute['cost'][1])/float(self.dbClass.minutesHour)))
                        tmpList.append(interval)
                        duration += interval
                    tmpList.append(routes[i][j])
                    trajectoryDict = dict(zip(dictKey, tmpList))
                    tmpList = []
                    trajectory.append(trajectoryDict)
                objID = ObjectId()
                route = {"_id": objID, "trajectory": trajectory, "date": today, "duration": duration, "line": line}
                self.dbClass.db.DynamicRoute.insert_one(route)
                line += 1
                duration = 0
                tmpList = []
                trajectory = []

    def dynamicRoutesGenerator(self):
        DG = self.creategraph()
        #define a test date bound
        startdate = datetime.datetime(2015, 11, 11, 0, 0, 0)
        enddate = datetime.datetime(2015, 11, 12, 0, 0, 0)
        routes = self.generateRoutes(DG, startdate, enddate)
        self.storeRoutesToDB(routes)

if __name__ == '__main__':
    DR = DynamicRoutes()
    DR.dynamicRoutesGenerator()















