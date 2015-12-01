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
from heapq import heappop, heappush
import threading
import sys
# import math
import time

# import Image
# import ImageDraw
from xml.sax import make_parser, handler
# from Tkinter import Tk, Canvas, Frame, BOTH
from multiprocessing import Process

from aStar import AStar
from busStop import BusStop
from coordinate import Coordinate
from address import Address
import coordinate
from mapDrawing import DrawImage
from busNetwork import BusNetwork


# The size width of the produced image in pixels
picSize = 3000
# The max speed on a road that does not have a set max speed.
standardSpeed = 50
# Roads buses can drive on
busRoadTypes = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary',
                'primary_link', 'secondary', 'secondary_link', 'tertiary',
                'tertiary_link', 'unclassified', 'residential')
# , 'service')


class RouteHandler(handler.ContentHandler):
    """

    """

    def __init__(self):

        # all nodes in the map with Id as key
        self.nodes = {}
        # all nodes with coord as key id as value
        self.nodeID = {}
        # all bus stop nodes
        self.busStops = []
        self.busStopNode = {}

        self.roadMapGraph = {}
        self.roadIntersectionGraph = {}

        # Roads
        self.roads = {}

        self.addresses = {}

        # self.index = 0

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
            self.nodeID[(lon, lat)] = nodeId
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
            # motorVehicle = self.tag.get('motor_vehicle', '')
            junction = self.tag.get('junction', '')
            roadName = self.tag.get('name', '')
            street = self.tag.get('addr:street', '')
            housenumber = self.tag.get('addr:housenumber', '')

            # If the way is a road and if the bus can drive on it
            if motorcar != 'no':
                if highway in busRoadTypes:
                    roadTypeIndex = busRoadTypes.index(highway)

                    # add edges between nodes that can be accessed by a bus
                    for nd in range(len(self.nd) - 1):
                        self.addEdge(self.nd[nd], self.nd[nd + 1], maxspeed,
                                     roadTypeIndex, wayID=self.roadId)
                        if not oneway:
                            self.addEdge(self.nd[nd + 1], self.nd[nd],
                                         maxspeed, roadTypeIndex,
                                         wayID=self.roadId)

                    self.roads[self.roadId] = [roadName, junction, self.nd,
                                               oneway]

            # Add the name of the road to the address list if it is a road
            # with a name.
            if highway != '' and highway != 'platform' and roadName != '':
                for node in self.nd:
                    self.addAddress(roadName, node)

            # Not all house numbers are represented as a nodes. Some are tags
            # on the house ways.
            if street != '' and housenumber != '':
                self.addAddress(street, self.nd[0], housenumber)
                # TODO Add a better thing then nd[0]

        elif name == 'node':
            # Look for nodes that are bus stops
            # highway = self.tag.get('highway', '')
            bus = self.tag.get('bus', '')
            public_transport = self.tag.get('public_transport', '')

            stopName = self.tag.get('name', '')
            street = self.tag.get('addr:street', '')
            housenumber = self.tag.get('addr:housenumber', '')
            if bus == 'yes' and public_transport == 'stop_position' and stopName != '':
                busStop = BusStop(stopName,
                                  longitude=self.nodes[self.node].longitude,
                                  latitude=self.nodes[self.node].latitude)
                self.busStops.append(busStop)
                self.busStopNode[self.node] = busStop
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
        key = street.lower()
        if key in self.addresses:
            if number is None:
                self.addresses[key].addCoordinate(self.nodes[node])
            else:
                self.addresses[key].addNumber(number, self.nodes[node])
        else:
            if number is None:
                self.addresses[key] = Address(street)
                self.addresses[key].addCoordinate(self.nodes[node])
            else:
                self.addresses[key] = Address(street)
                self.addresses[key].addNumber(number, self.nodes[node])

    def rmEdge(self, edgeList, id):
        for x in edgeList:
            if x[0] == id:
                edgeList.remove(x)
                break

    def makeRoadIntersectionGraph(self):
        """
        myRoad = dict(self.roads)
        nodeList = []

        i = len(myRoad)
        for road in myRoad:
            print i,
            i -= 1
            if i == 6000:
                break

            nodeList.append(myRoad[road][2][0])

            for nodeID in myRoad[road][2][1:]:

                for road2 in myRoad:
                    if nodeID == myRoad[road2][2][0] or nodeID == myRoad[road2][2][-1]:
                        nodeList.append(nodeID)


        self.NOD = nodeList
        """
        pass


class Map:
    """
    The main class for the routing.

    """

    def __init__(self, omsfilepath):
        self.omsfile = omsfilepath
        self.astar = AStar(standardSpeed)
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
        self.handler.makeRoadIntersectionGraph()

    def getNodeIdFromCoordinates(self, coordinates):
        """
        :param coordinates: (longitude, latitude)
        :return: nodeID
        """
        if coordinates in self.handler.nodeID and self.inEdgeList(
                self.handler.nodeID[coordinates]):

            return self.handler.nodeID[coordinates]
        else:
            return self.closestRoadNode(coordinates)
    """
    def makeBusGraph(self):

        graph = {}

        i = 0
        l = len(self.busStopList)
        timer = time.time()
        for busStopA in self.handler.busStops:

            if busStopA.name not in graph:
                graph[busStopA.name] = {}

            i = i + 1
            print "\n%f s\n (%d / %d) - %s" % (time.time() - timer, i, l, busStopA.name)
            timer = time.time()
            for busStopB in self.handler.busStops:

                if busStopB.name not in graph[busStopA.name] and busStopA != busStopB:
                    print '\033[91m' + '.' + '\033[0m',
                    path, cost = self.findRouteFromCoordinateList([
                        busStopA.coordinates,
                        busStopB.coordinates])

                    start = busStopA.name
                    _cameFrom = []
                    for node in path[1:]:
                        id = self.handler.nodeID[node]

                        if id in self.handler.busStopNode:
                            b = self.handler.busStopNode[id].name

                            if start not in graph:
                                graph[start] = {}

                            graph[start][b] = []
                            graph[busStopA.name][b] = False
                            graph[start][busStopB.name] = False

                            for name in _cameFrom:
                                graph[name][b] = False

                            _cameFrom.append(start)
                            start = b

        return graph
    """
    def getNodeIdFromCoordinatesList(self, coordinatesList):
        """
        :param coordinates: [(longitude, latitude)]
        :return: nodeID
        """
        nodeIdList = []
        for coordinates in coordinatesList:
            nodeIdList.append(self.getNodeIdFromCoordinates(coordinates))
        return nodeIdList

    def closestRoadNode(self, coordinates):
        coord = Coordinate(longitude=coordinates[0], latitude=coordinates[1])
        node = self.edges.keys()[0]
        dist = coordinate.measure(coord, self.nodes[node])
        for nd in self.edges.keys():
            if dist > coordinate.measure(coord, self.nodes[nd]):
                dist = coordinate.measure(coord, self.nodes[nd])
                node = nd
        return node

    def findBusStopName(self, lon, lat):
        for nd in self.busStopList:
            if nd.longitude == lon and nd.latitude == lat:
                return nd.name
        return None

    def findBusStopPosition(self, name):
        name = name.decode('utf-8').lower()
        for nd in self.busStopList:
            if nd.name.lower() == name:
                return nd.coordinates
        return None

    def findClosestBusStopFromCoordinates(self, lon, lat):
        """
        Finds the closest bus stop to the position of (lon, lat).

        :param lon: longitude
        :param lat: latitude
        :return: BusStop object
        """
        stop = self.busStopList[0]
        position = Coordinate(latitude=lat, longitude=lon)
        dist = coordinate.measure(stop, position)

        for _stop in self.busStopList:
            _dist = coordinate.measure(_stop, position)
            if _dist < dist:
                stop = _stop
                dist = _dist

        return stop

    def findBusStopsFromCoordinates(self, lon, lat, distance):
        """
        Find the bus stops to the position of (lon, lat) and that is in the
        radius of distance.

        :param lon: longitude float
        :param lat: latitude float
        :param distance: meters float
        :return: list of tuples [(name, coordinates, distance)]
        """

        position = Coordinate(longitude=lon, latitude=lat)
        busStops = []

        for _stop in self.busStopList:
            _dist = coordinate.measure(_stop, position)
            if _dist <= distance:
                busStops.append((_stop.name, _stop.coordinates, _dist))

        if not busStops:
            _closest = self.findClosestBusStopFromCoordinates(lon, lat)
            _cdist = coordinate.measure(_closest, position)
            busStops.append((_closest.name, _closest.coordinates, _cdist))
        return busStops

    def findCoordinatesFromAdress(self, address, number=None):
        """
        Translates an address into coordinates.
        """
        # TODO Add fuzzy logic
        address = address.decode('utf-8').lower()
        if address in self.handler.addresses:
            if number is None:
                coordinateList = self.handler.addresses[address].coordinates
                center = coordinate.center(coordinateList)
                # addressCoord = coordinate.closestTo(center, coordinateList)
                return center

            else:
                if number in self.handler.addresses[address].numbers:
                    noCoord = self.handler.addresses[address].numbers[number]
                    # coordList = self.handler.addresses[address].coordinates
                    # addressCoord = coordinate.closestTo(noCoord, coordList)
                    return noCoord
                else:
                    # TODO Find closest housenumber to number
                    return self.findCoordinatesFromAdress(address)
        else:
            return None

    def findRoute(self, startNode, endNode):
        """
        Finds a route between two points in the map. Uses the A* algorithm to
        find this path.

        :param startNode: id of the starting node
        :param endNode: id of the ending node
        :return: a path between the start and ending point and the to take that
                path
        """
        path, cost = self.astar.findPath(self.nodes, self.edges, startNode,
                                         endNode)
        return path, cost[endNode]

    def findRouteFromCoordinateList(self, coordinateList):
        """
        Finds the paths path between points in a list of coordinates. The path
        through an increasing order of indexes. Index 0 is the starting point
        and N-1 is the end point where N is the length of the list.

        Coordinates are represented as a tuple with (longitude, latitude)

        :param coordinateList: [coordinates]
        :return:
        """
        # Get the node IDs of the coordinates.
        nodeIDList = self.getNodeIdFromCoordinatesList(coordinateList)
        path = []
        cost = [0]
        # If at least one coordinates does not have an ID
        if None in nodeIDList:
            return [None], None
        # If there is only one element there is no path
        if len(nodeIDList) == 1:
            path.append(nodeIDList[0])
        elif len(nodeIDList) > 1:
            path.append(nodeIDList[0])
            for n in range(0, len(nodeIDList) - 1):
                _path, _cost = self.findRoute(nodeIDList[n], nodeIDList[n + 1])
                [path.append(x) for x in _path[1:]]
                cost.append(_cost)

        coordinatePath = []

        # Translate back the node IDs to coordinates
        for id in path:
            coordinatePath.append(self.nodes[id].coordinates)

        return coordinatePath, cost

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
                nPath, _ = self.findRoute(nodeList[n], nodeList[n + 1])
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

    def getBusStopConnections(self):
        bus_stop_connections = {}
        bus_stop_ids = []
        for busStop in self.busStopList:
            bus_stop_ids.append(self.handler.nodeID[busStop.coordinates])
        for busStop in bus_stop_ids:
            pass

    def inEdgeList(self, sid):
        return self.handler.roadMapGraph.has_key(sid)

    def timeBetweenStops(self, stopA, stopB):
        path, cost = self.astar.findRoute(stopA, stopB)
        return cost[stopB]


#class drawApp(threading.Thread):
#    def __init__(self):
#        threading.Thread.__init__(self)
#
#    def run(self):
#        print "Starting thread"
#        root = Tk()
#        ex = Example(root)
#        root.geometry("400x250+300+300")
#        ex.mainloop()


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
    print "\nLoading data ..."
    myMap.parsData()
    print "Data loaded in: %f sec\n" % (time.time() - timer)

    print "We have " + str(len(myMap.nodes)) + " nodes in total"
    print "We have " + str(len(myMap.busStopList)) + " bus stops in total\n"


    print "Draw image ..."
    img = DrawImage(10000,
                    myMap.handler.minlon,
                    myMap.handler.minlat,
                    myMap.handler.maxlon,
                    myMap.handler.maxlat)

    img.drawRoads(myMap.edges, myMap.nodes)
    # img.drawNodeList(myMap.nodes, 'blue')
    # img.drawNodeList([myMap.nodes[x] for x in myMap.handler.NOD], 'red')
    img.drawBusStops(myMap.busStopList, myMap.nodes)
    img.drawSave(sys.argv[1])
    
    # b = BusNetwork()
    # b.makeBusGraph(myMap.handler.nodes, myMap.handler.busStopNode, myMap.edges)
    # myMap.makeBusGraph()
