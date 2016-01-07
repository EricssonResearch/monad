__author__ = 'mohammad'
import random
import string
import collections
import datetime
import itertools
import numpy
import datetime
from datetime import timedelta
from pymongo import MongoClient
from bson.objectid import ObjectId
from operator import itemgetter
from dbConnection import DB
import networkx as nx
import matplotlib.pyplot as plt
from bson.objectid import ObjectId


class DynamicRoutes():
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # INDEX
    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Class variables
    # Constructor
    # Create Graph
    # Generate Dynamic Routes

    # ---------------------------------------------------------------------------------------------------------------------------------------
    # Class variables
    # ---------------------------------------------------------------------------------------------------------------------------------------
    server = "130.238.15.114"
    port = 27017
    database = "monad1"
    user = "monadStudent"
    password = "M0nad2015"

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
        db = DB()
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
        #transition matrix
        tmatrix = numpy.zeros((busStops.count(), busStops.count()), dtype=numpy.int)
        #print tmatrix

        reqs = db.getRequestsFromDB(start_date, end_date)
        print "Request len",len(reqs)

        for req in reqs:

            i = routebusstopsdic[db.getBusStopName(req[1])]
            j = routebusstopsdic[db.getBusStopName(req[2])]

            if i != j:
                tmatrix[j][i] += 1
            else:
                tmatrix[j][i] = 0


        maxnumber = max(map(max, tmatrix))
        while maxnumber > 0:
            maxnumber = max(map(max, tmatrix))
            #print "Max is"
            #print maxnumber
            indx = numpy.where(tmatrix == maxnumber)
            #print tmatrix[indx[0][0]][indx[1][0]]
            Start_bus_stop = [key for key, value in routebusstopsdic.iteritems() if value == indx[0][0]]
            End_bus_stop = [key2 for key2, value in routebusstopsdic.iteritems() if value == indx[1][0]]

            try:
                if Start_bus_stop[0]!=End_bus_stop[0]:
                    #print "route from to "
                    #print Start_bus_stop[0], End_bus_stop[0]
                    bus_stops1 = nx.astar_path(DG, "Centralstationen", Start_bus_stop[0])
                    bus_stops2 = nx.astar_path(DG, Start_bus_stop[0], End_bus_stop[0], heuristic=None, weight='distance')
                    bus_stops3 = nx.astar_path(DG, End_bus_stop[0], "Centralstationen")
                    bus_stops = bus_stops1+bus_stops2 +bus_stops3
                    getin = 0
                    getout = 0
                    nbusstops = [bus_stops[0]]
                    intrip = []
                    outtrip = []
                    #process the bus stops remove the smiliar adj name
                    #print "before--------------"
                    #print bus_stops
                    #print "After--------------"
                    #print nbusstops
                    for i in range(1, len(bus_stops)):

                        if bus_stops[i-1] != bus_stops[i]:
                            nbusstops.append(bus_stops[i])
                    routes.append(nbusstops)
                    #print "Routes ",routes
                    for i in range(0, len(nbusstops)):

                        getin = 0
                        getout = 0
                        for j in range(i, len(nbusstops)):

                            getin += tmatrix[routebusstopsdic[nbusstops[i]]][routebusstopsdic[nbusstops[j]]]
                            #print "getin --------------------"
                            #print nbusstops[i], nbusstops[j]
                            intrip.append([nbusstops[i], nbusstops[j], getin])
                            #print tmatrix[routebusstopsdic[nbusstops[i]]][routebusstopsdic[nbusstops[j]]]
                        #print intrip

                        for l in range(0, i+1):
                            getout += tmatrix[routebusstopsdic[nbusstops[l]]][routebusstopsdic[nbusstops[i]]]
                            #print "getout --------------------"
                            #print nbusstops[l],nbusstops[i]
                            #print tmatrix[routebusstopsdic[nbusstops[l]]][routebusstopsdic[nbusstops[i]]]
                            #outtrip.append([nbusstops[l], nbusstops[i], tmatrix[routebusstopsdic[nbusstops[l]]][routebusstopsdic[nbusstops[i]]]])

                        #print intrip.append([nbusstops[i], getin, getout])
                    #print "getin --------------------"
                    #print intrip
                    #print "getout --------------------"
                    #print outtrip
                    #print DG [bus_stops[1]][bus_stops[2]]
                    #for counter in range(0,len(bus_stops)-1):
                    #distance =sum(DG.get_edge_data(DG[bus_stops[1]],DG[bus_stops[2]]))
                    #print tmatrix
                    buscapacity = 100
                    temp =[]
                    bus_free=100
                    #print "intrip len :", len(intrip)
                    for k in range(0, len(intrip)):

                        if intrip[k][2] > 0 and bus_free > 0:
                            if bus_free >= intrip[k][2]:
                                bus_free = bus_free - intrip[k][2]
                                intrip[k][2] = 0
                                #print "matrix before",tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]]
                                tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]] = 0
                                #print "matrix after",tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]]
                                bus_allocated =bus_allocated + bus_free
                            else:
                                bus_free = 0
                                intrip[k][2] =intrip[k][2] - bus_free
                                #print "matrix before",tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]]
                                tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]] = tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]] - bus_free
                                #print "matrix after",tmatrix[routebusstopsdic[intrip[k][0]]][routebusstopsdic[intrip[k][1]]]
                                bus_allocated = bus_allocated + bus_free

                            temp.append([intrip[k][1], bus_free])


                        if intrip[k][0] in temp:
                            bus_free += temp[1]
                            bus_allocated =100 - bus_free
                    #print "temp",temp



            except:nx.NetworkXNoPath

        client = MongoClient()
        client = MongoClient('130.238.15.114',27017)
        for i in routes:

            for j in range(0, len(i)):
                #print i[j]
                #test = dict((n,d['name']) for n,d in DG.nodes(data=True) if n == i[j])

                temp = client.monad1.BusStop.find_one({"name": i[j]})
                tempids.append(temp['_id'])
                1
            routesid.append(tempids)
            tempids = []


        return routesid

    def storeRoutesToDB(self,routes):
        server = "130.238.15.114"
        port = 27017
        database = "monad1"
        user = "monadStudent"
        password = "M0nad2015"
        client = MongoClient("mongodb://" + user + ":" + password + "@" + server, port, maxPoolSize=200, connectTimeoutMS=5000, serverSelectionTimeoutMS=5000)
        db = client[database]
        db.dynamicRoute.remove()
        #routes = testdata()
        #print routes
        duration = 0
        line = 1
        trajectory = []
        tmpList = []
        todayDate = datetime.datetime.now()
        today = datetime.datetime(todayDate.year, todayDate.month, todayDate.day)
        todayRoute = db.dynamicRoute.find({'date': today})
        dictKey = ['interval', 'busStop']
        if todayRoute.count() == 0:
            #print 'todays route is writing'
            for i in range(len(routes)):
                for j in range(len(routes[i])):
                    if j == 0:
                        tmpList.append(0)
                    else:
                        tmpList.append(random.randint(1,4))
                        duration += tmpList[0]
                    tmpList.append(routes[i][j])
                    #print tmpList
                    trajectoryDict = dict(zip(dictKey, tmpList))
                    tmpList = []
                    trajectory.append(trajectoryDict)
                objID = ObjectId()
                route = {"_id": objID, "trajectory": trajectory, "date": today, "duration": duration, "line": line}
                #print "the route is ", route
                db.dynamicRoute.insert_one(route)
                line += 1
                duration = 0
                tmpList = []
                trajectory = []


if __name__ == '__main__':
        DR = DynamicRoutes()
        DG = DR.creategraph()
        startdate = datetime.datetime(2015, 11, 11, 0, 0, 0)
        enddate = datetime.datetime(2015, 11, 12, 0, 0, 0)
        routes = DR.generateRoutes(DG, startdate, enddate)
        #print routes
        DR.storeRoutesToDB(routes)















