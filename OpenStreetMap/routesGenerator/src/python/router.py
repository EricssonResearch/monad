# -*- coding: utf-8 -*-
"""
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""

import sys
import math
import time

import Image, ImageDraw
from xml.sax import make_parser, handler
from heapq import heappush, heappop

from busStop import BusStop
from coordinate import Coordinate
from address import Address
import coordinate

# The size width of the produced image in pixels
picSize = 3000
# The max speed on a road that does not have a set max speed.
standardSpeed = 50
# Roads buses can drive on
busRoadTypes = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary',
                'primary_link', 'secondary', 'secondary_link', 'tertiary',
                'tertiary_link', 'unclassified', 'residential', 'service')


# class BusStop:
#    def __init__(self, nodeId, longitude, latitude):
#        self.id = nodeId
#        self.coordinates = (longitude, latitude)
#        self.busStopName = ""
#
#    def addBusStopName(self, name):
#        self.busStopName = name


class RouteHandler(handler.ContentHandler):
    """

    """

    def __init__(self):
        # all nodes in the map
        self.nodes = {}
        # all bus stop nodes
        self.busStops = []

        self.roadMapGraph = {}
        self.roadIntersectionGraph = {}
        # Roads
        self.roads = {}

        self.addresses = {}

        self.index = 0

        # Used as temp
        self.nd = []
        self.tag = {}
        self.node = 0

        self.maxlat = 0.0
        self.maxlon = 0.0
        self.minlat = 0.0
        self.minlon = 0.0

    def startElement(self, name, attributes):
        """
        When a new attribute in the xml file is seen we enter this function.
        E.g <way> or <node>
        """
        if name == 'bounds':
            # Get the size of the map in lon lat
            self.minlat = float(attributes.get('minlat'))
            self.minlon = float(attributes.get('minlon'))
            self.maxlat = float(attributes.get('maxlat'))
            self.maxlon = float(attributes.get('maxlon'))

        elif name == 'node':
            # Add every node
            nodeId = int(attributes.get('id'))
            lat = float(attributes.get('lat'))
            lon = float(attributes.get('lon'))
            self.nodes[nodeId] = Coordinate(latitude=lat, longitude=lon)
            # self.busStops.append(BusStop(nodeId, lon, lat))
            # self.index += 1
            self.node = nodeId
        elif name == 'way':
            self.roadId = int(attributes.get('id'))
        elif name == 'nd':
            # Add the nodes in the temp array, used for way attributes
            # to collect the nodes in that way
            self.nd.append(int(attributes.get('ref')))
        elif name == 'tag':
            # Remember the tag for attributes
            self.tag[attributes.get('k')] = attributes.get('v')
        elif name == 'relation':
            pass

    def endElement(self, name):
        """
        When the parsing reads the end of an attribute, this function is
        called. E.g </way> or </node>
        """
        if name == 'way':
            highway = self.tag.get('highway', '')
            oneway = self.tag.get('oneway', '') in ('yes', 'true', '1')
            maxspeed = self.tag.get('maxspeed', standardSpeed)
            motorcar = self.tag.get('motorcar', '')
            junction = self.tag.get('junction', '')
            roadName = self.tag.get('name', '')
            street = self.tag.get('addr:street', '')
            housenumber = self.tag.get('addr:housenumber', '')

            # If the way is a road and if the bus can drive on it
            if motorcar != 'no':
                if highway in busRoadTypes:
                    roadInt = busRoadTypes.index(highway)
                    # add edges between nodes that can be accessed by a bus
                    for nd in range(len(self.nd) - 1):
                        self.addEdge(self.nd[nd], self.nd[nd + 1], maxspeed,
                                     roadInt, wayID=self.roadId)
                        if not oneway:
                            self.addEdge(self.nd[nd + 1], self.nd[nd],
                                         maxspeed, roadInt, wayID=self.roadId)

                    self.roads[self.roadId] = [(roadName, junction)]

            # Add the name of the road to the address list if it is a road
            # with a name.
            if highway != '' and highway != 'platform' and roadName != '':
                for node in self.nd:
                    self.addAddress(roadName, node)
                    pass

            # Not all house numbers are represented as a nodes. Some are tags
            # on the house ways.
            if street != '' and housenumber != '':
                self.addAddress(street, self.nd[0], housenumber)
                # TODO Add a better thing then nd[0]

        elif name == 'node':
            # Look for nodes that are bus stops
            highway = self.tag.get('highway', '')
            stopName = self.tag.get('name', '')
            street = self.tag.get('addr:street', '')
            housenumber = self.tag.get('addr:housenumber', '')
            if highway == 'bus_stop':
                # self.busStops[self.index - 1].addBusStopName(stopName)
                self.busStops.append(BusStop(stopName,
                                             self.nodes[self.node].longitude,
                                             self.nodes[self.node].latitude))
            if street != '' and housenumber != '':
                self.addAddress(street, self.node, housenumber)
                pass

        # Clean up
        if name in ('node', 'way', 'relation'):
            self.nd = []
            self.tag = {}
            self.node = 0

    def addEdge(self, fromNode, toNode, maxspeed, roadInt, wayID):
        """
        Adds an edge between fromNode to toNode in self.edges with
        attributes maxspeed, roadInt (type of road)
        """
        if fromNode in self.roadMapGraph:
            self.roadMapGraph[fromNode].append((toNode, maxspeed, roadInt,
                                                wayID))
        else:
            self.roadMapGraph[fromNode] = [(toNode, maxspeed, roadInt, wayID)]
        if toNode not in self.roadMapGraph:
            self.roadMapGraph[toNode] = []

    def addAddress(self, street, node, number=None):
        if street in self.addresses:
            if number is None:
                self.addresses[street].addCoordinate(self.nodes[node])
            else:
                self.addresses[street].addNumber(number, self.nodes[node])
        else:
            if number is None:
                self.addresses[street] = Address(street)
                self.addresses[street].addCoordinate(self.nodes[node])
            else:
                self.addresses[street] = Address(street)
                self.addresses[street].addNumber(number, self.nodes[node])


class AStar:
    def __init__(self):
        pass

    def getNodeById(self, nodes, nodeId):
        for nd in nodes:
            if nd.id == nodeId:
                return nd
        return -1

    def findPath(self, nodes, edges, start, goal):
        """
        Finds a path between start and goal using a*. The search is done in the
        graph self.edges.
        """
        openSet = []
        heappush(openSet, (0, start))
        path = {}
        cost = {}
        path[start] = 0
        cost[start] = 0

        if start == goal:
            cost[goal] = 0
            return self.reconstruct_path(path, start, goal), cost

        # A high value that a real path should not have.
        cost[goal] = 300000

        # As long as there are paths to be explored
        while not (len(openSet) == 0):
            current = heappop(openSet)[1]

            # We found the goal, stop searching, we are done.
            if current == goal:
                break

            # For all nodes connected to the one we are looking at for the
            # moment.
            for nextNode, speed, roadInt, _ in edges[current]:
                # How fast you can go on a road matters on the type of the road
                # It can be seen as a penalty for "smaller" roads.
                speedDecrease = (1 - (float(roadInt) / 50))
                fromCoordinate = nodes[current]
                toCoordinate = nodes[nextNode]
                # roadLength = self.measure(fromCoordinate.longitude,
                #                          fromCoordinate.latitude,
                #                          toCoordinate.longitude,
                #                          toCoordinate.latitude)

                roadLength = coordinate.measure(fromCoordinate, toCoordinate)

                timeOnRoad = (roadLength /
                              (speedDecrease * (float(speed) * 1000 / 3600)))

                newCost = cost[current] + timeOnRoad

                if nextNode not in cost or newCost < cost[nextNode]:
                    cost[nextNode] = newCost

                    weight = (newCost + (roadInt ** 1) +
                              (self.heuristic(nodes[nextNode], nodes[goal]) /
                               (float(standardSpeed) * 1000 / 3600)))

                    heappush(openSet, (weight, nextNode))
                    path[nextNode] = current

        return self.reconstruct_path(path, start, goal), cost

    def heuristic(self, node, goal):
        # x1, y1 = node.coordinates
        # x2, y2 = goal.coordinates
        # return self.measure(x1, y1, x2, y2)
        return coordinate.measure(node, goal)

    #    def measure(self, lon1, lat1, lon2, lat2):
    #        """
    #        Measure the distance between to points in lon and lat and returns the
    #        distance in meters.
    #        """
    #        # Radius of the earth in meters
    #        earthRadius = 6371000
    #        dLat = (lat2 - lat1) * math.pi / 180
    #        dLon = (lon2 - lon1) * math.pi / 180
    #
    #        a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
    #             math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) *
    #             math.sin(dLon / 2) * math.sin(dLon / 2))
    #
    #        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    #        meters = earthRadius * c
    #        return meters

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path


class Map:
    """
    The main class for the routing.

    """

    def __init__(self, omsfilepath):
        self.omsfile = omsfilepath
        self.astar = AStar()
        self.handler = RouteHandler()
        self.nodes = {}
        self.busStopList = []
        self.edges = {}

    def parsData(self):
        """
        Called when it is time to pars the osm map file. The map is supplied
        when initializing the class.
        """
        self.handler = RouteHandler()
        parser = make_parser()
        parser.setContentHandler(self.handler)
        parser.parse(self.omsfile)
        self.nodes = self.handler.nodes
        self.busStopList = self.handler.busStops
        self.edges = self.handler.roadMapGraph

    def findBusStopName(self, lon, lat):
        for nd in self.busStopList:
            if nd.longitude == lon and nd.latitude == lat:
                return nd.busStopName
        return "no stop found"

    def findBusStopPosition(self, name):
        for nd in self.busStopList:
            if nd.busStopName == name:
                return nd.coordinates
        return "no such stop name"

    def findClosestBusStopFromCoordinates(self, lon, lat):

        dist = self.astar.measure(self.busStopList[0].longitude,
                                  self.busStopList[0].latitude,
                                  lon,
                                  lat)
        theBus = self.busStopList[0]
        for bus in self.busStopList:
            if self.astar.measure(bus.longitude, bus.latitude, lon,
                                  lat) < dist:
                theBus = bus
        return theBus

    def findCoordinatesFromAdress(self, address, number=None):
        """
        Translates an address into coordinates.
        """
        # TODO Add fuzzy logic

        if address in self.handler.addresses:
            if number is None:
                coordinateList = self.handler.addresses[address].coordinates
                center = coordinate.center(coordinateList)
                #addressCoord = coordinate.closestTo(center, coordinateList)
                return center

            else:
                if number in self.handler.addresses[address].numbers:
                    noCoord = self.handler.addresses[address].numbers[number]
                    #coordList = self.handler.addresses[address].coordinates
                    #addressCoord = coordinate.closestTo(noCoord, coordList)
                    return noCoord
                else:
                    # TODO Find closest housenumber to number
                    return self.findCoordinatesFromAdress(address)
        else:
            return None

    # def getNodebyId(self, nodeId):
    #   return
    #    for nd in self.busStopList:
    #       #print nd.id
    #        if nd.id == nodeId:
    #            return nd
    #    return -1

    def findRoute(self, startNode, endNode):
        """
        Finds a route between two points in the map. Uses the A* algorithm to
        find this path.

        :param startNode: id of the starting node
        :param endNode: id of the ending node
        :return: a path between the start and ending point
        """
        path, cost = self.astar.findPath(self.nodes, self.edges, startNode,
                                         endNode)
        return path

    def findWayPoints(self, startNode, endNode):
        """
        Finds path and way points between two nodes. Used for finding the route
        between two points (nodes) in the road map. The points have to be
        located on the road.
        """
        route = self.findRoute(startNode, endNode)
        return route, self.getWayPointsFromPath(route)

    def findWayPointsFromList(self, nodeList):
        """
        Finds the path and way points between multiple points (intermediate
        points). The path will go from N to N+1. list[0] is the starting point
        the last element of the list will be the ending point.
        """
        path = []
        waypoints = []
        if len(nodeList) > 1:
            path.append(nodeList[0])
            for n in range(0, len(nodeList) - 1):
                nPath = self.findRoute(nodeList[n], nodeList[n + 1])
                [path.append(x) for x in nPath[1:]]
            waypoints = self.getWayPointsFromPath(path)

        return path, waypoints

    def getWayPointsFromPath(self, path):
        """
        Given a path it will return the way points on that path.
        """
        nodeList = []
        for n in range(1, len(path) - 2):

            roadIDfrom = ([item for item in self.edges[path[n - 1]]
                           if item[0] == path[n]][0][3])
            roadIDto = ([item for item in self.edges[path[n]]
                         if item[0] == path[n + 1]][0][3])

            if roadIDfrom != roadIDto:
                nodeList.append(path[n])
        return nodeList

    def inEdgeList(self, sid):
        return self.handler.roadMapGraph.has_key(sid)

    def timeBetweenStops(self, stopA, stopB):
        path, cost = self.astar.findRoute(stopA, stopB)
        return cost[stopB]

    def y2lat(self, a):
        return 180.0 / math.pi * (2.0 *
                                  math.atan(math.exp(a * math.pi / 180.0)) -
                                  math.pi / 2.0)

    def lat2y(self, a):
        return 180.0 / math.pi * (math.log(math.tan(math.pi / 4.0 + a *
                                                    (math.pi / 180.0) / 2.0)))

    # Contains some drawing functions that can/should be left out. They are
    # mainly used for testing the other functions.
    def drawInit(self, x):
        self.lonLength = (self.handler.maxlon - self.handler.minlon)
        self.imgScaling = (x / self.lonLength)

        y = ((self.lat2y(self.handler.maxlat) -
              self.lat2y(self.handler.minlat)) *
             self.imgScaling)

        self.im = Image.new('RGBA', (x, int(y)), 'white')
        self.draw = ImageDraw.Draw(self.im)

    def drawSave(self, name):
        self.im.show()
        self.im.save(name)

    def drawNodes(self, nodes, colour):
        y1 = self.lat2y(self.handler.minlat)
        y2 = self.lat2y(self.handler.maxlat)
        y = (y2 - y1) * self.imgScaling

        for id, n in nodes.items():
            pointX = (n.longitude - self.handler.minlon) * self.imgScaling
            pointY = y - (self.lat2y(n.latitude) - y1) * self.imgScaling
            self.draw.point((pointX, pointY), colour)

    def drawNodeIds(self, nodeIds, colour):
        y1 = self.lat2y(self.handler.minlat)
        y2 = self.lat2y(self.handler.maxlat)
        y = (y2 - y1) * self.imgScaling

        for nd in nodeIds:
            n = self.nodes[nd].coordinates
            pointX = (n[0] - self.handler.minlon) * self.imgScaling
            pointY = y - (self.lat2y(n[1]) - y1) * self.imgScaling
            self.draw.point((pointX, pointY), colour)

    def drawRoads(self, edges, nodes):
        y1 = self.lat2y(self.handler.minlat)
        y2 = self.lat2y(self.handler.maxlat)
        y = (y2 - y1) * self.imgScaling

        for id, n in edges.items():
            a = nodes[id].coordinates

            for k, z, i, _ in n:
                b = nodes[k].coordinates

                colr = 255 - min(int(255 * (float(z) / 120)), 255)
                if int(z) < 31:
                    colr = 220
                self.drawLine(y, y1, a[0], a[1], b[0], b[1], self.imgScaling,
                              (colr, colr, colr, 255))

    def drawBusStops(self, busStops, nodes):
        y1 = self.lat2y(self.handler.minlat)
        y2 = self.lat2y(self.handler.maxlat)
        y = (y2 - y1) * self.imgScaling

        for stopName, stopIDs in busStops.items():
            radius = 2
            if stopName == '':
                for bid in stopIDs:
                    stop = nodes[bid]
                    self.drawCircle(y, y1, stop[0], stop[1], radius,
                                    self.imgScaling, (110, 50, 200))
            else:
                stop = nodes[stopIDs[0]]
                self.drawCircle(y, y1, stop[0], stop[1], radius,
                                self.imgScaling, (254, 122, 85))

    def drawPath(self, path, colour):
        y1 = self.lat2y(self.handler.minlat)
        y2 = self.lat2y(self.handler.maxlat)
        y = (y2 - y1) * self.imgScaling

        fromNode = 0
        for pid in path:
            toNode = self.nodes[pid].coordinates
            if fromNode == 0:
                fromNode = toNode
            else:
                self.drawLine(y, y1, fromNode[0], fromNode[1], toNode[0],
                              toNode[1], self.imgScaling, colour)

                fromNode = toNode

    def drawPoint(self, y, y1, lon, lat, scale, colour):
        pointPX = (lon - self.minlon) * scale
        pointPY = y - ((self.lat2y(lat) - y1) * scale)
        self.draw.point((pointPX, int(pointPY)), colour)

    def drawLine(self, y, y1, aLon, aLat, bLon, bLat, scale, colour):
        pointAX = (aLon - self.handler.minlon) * scale
        pointAY = y - ((self.lat2y(aLat) - y1) * scale)
        pointBX = (bLon - self.handler.minlon) * scale
        pointBY = y - ((self.lat2y(bLat) - y1) * scale)
        self.draw.line((pointAX, pointAY, pointBX, pointBY), colour)

    def drawCircle(self, y, y1, lon, lat, r, scale, colour):
        pointCX = (lon - self.handler.minlon) * scale
        pointCY = y - ((self.lat2y(lat) - y1) * scale)
        self.draw.ellipse((pointCX - r, pointCY - r, pointCX + r, pointCY + r),
                          fill=colour)


if __name__ == '__main__':
    """
    If the program is run by it self and not used as a library.It will take a
    osm-file as the first argument, img-file name,  and too IDs of points on
    roads.
    -- python router.py map.png map.osm
    If the IDs are left out it will only draw the map.
    """
    print "router.py"

    myMap = Map(sys.argv[2])
    print "file: " + myMap.omsfile

    timer = time.time()
    print "Loading data ..."
    myMap.parsData()
    print "Data loaded in: %f sec" % (time.time() - timer)
    # print "We have " + str(len(myMap.nodes)) + " nodes in total"
    # print "We have " + str(myMap.handler.index) + " bus stops in total"

    # print "Finding path... "
    ## flogsta vardcentral
    # nTo = 2198905720
    ## polacksbacken
    # nFrom = 1125461154

    ## print "Find a bus stop name: " + myMap.findBusStopName(17.6666581,
    ##                                                       59.8556742)
    ## print "Find a bus stop position: " + str(myMap.findBusStopPosition("Danmarksgatan"))

    # timer = time.time()
    # myPath = myMap.findRoute(nFrom, nTo)
    # print "Found path in: %f sec" % (time.time() - timer)

    # wayP = myMap.getWayPointsFromPath(myPath)

    # print "Finding path with four points"
    ## Flogsta vardcentral
    # nTo = 2198905720
    ## Kungsgatan
    # nThrough = 25734373
    ## Bruno Liljeforsgata
    # nThrough2 = 31996288
    ## Polacksbacken
    # nFrom = 1125461154

    # timer = time.time()
    # my4Path, _ = myMap.findWayPointsFromList([nFrom, nThrough, nThrough2, nTo])
    # print "Found path in: %f sec" % (time.time() - timer)

    # print "Draw image ..."
    # myMap.drawInit(3000)
    # myMap.drawNodes(myMap.nodes, (227, 254, 212, 255))
    # myMap.drawRoads(myMap.edges, myMap.nodes)
    ##    myMap.drawBusStops(myMap.handler.busStops, myMap.nodes)
    # myMap.drawPath(myPath, 'red')
    ## myMap.drawNodeIds(wayP, 'blue')
    ## myMap.drawPath(my4Path, 'green')
    # myMap.drawSave(sys.argv[1])
    # print "Image done,", sys.argv[1]

    # print myMap.handler.addresses[u'Rackarbergsgatan']
    # print myMap.handler.addresses[u'Studentvägen']
    print myMap.findCoordinatesFromAdress(u'Studentvägen').coordinates
    print myMap.findCoordinatesFromAdress(u'Luthagsesplanaden').coordinates
    print myMap.findCoordinatesFromAdress(u'Flogstavägen').coordinates
    # for ke in myMap.handler.addresses.keys():
    #    print ke, myMap.handler.addresses[ke].nodes

    # print coordinate.average(myMap.findCoordinatesFromAdress(u'Studentvägen'))
