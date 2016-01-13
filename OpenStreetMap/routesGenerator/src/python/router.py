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
import time

from xml.sax import make_parser, handler

from aStar import AStar
from busStop import BusStop
from coordinate import Coordinate
from address import Address
import coordinate
from mapDrawing import DrawImage
from busNetwork import BusNetwork


# The size width of the produced image in pixels
# picSize = 3000
# The max speed on a road that does not have a set max speed.
standardSpeed = 50
# Roads buses can drive on
busRoadTypes = ('motorway', 'motorway_link', 'trunk', 'trunk_link', 'primary',
                'primary_link', 'secondary', 'secondary_link', 'tertiary',
                'tertiary_link', 'unclassified', 'residential', 'bus_road')
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

        self.roadMapGraph = {}

        # Roads
        self.roads = {}

        self.addresses = {}

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
            # self.nodeID[(lon, lat)] = nodeId
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
            if motorcar != 'no' and highway in busRoadTypes:
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
        fromCoord = self.nodes[fromNode].coordinates
        toCoord = self.nodes[toNode].coordinates

        if fromCoord in self.roadMapGraph:
            self.roadMapGraph[fromCoord].append((toCoord, maxspeed, roadInt, wayID))
        else:
            self.roadMapGraph[fromCoord] = [(toCoord, maxspeed, roadInt, wayID)]

        if toCoord not in self.roadMapGraph:
            self.roadMapGraph[toCoord] = []

    def addAddress(self, street, node, number=None):
        """
        """
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
        self.roadNodes = []

    def parsData(self):
        """
        Called when it is time to pars the osm map file. The map is supplied
        when initializing the class.
        """
        self.handler = RouteHandler()
        parser = make_parser()
        parser.setContentHandler(self.handler)
        parser.parse(self.omsfile)
        self.handler.nodes = None

        self.busStopList = self.handler.busStops
        self.edges = self.handler.roadMapGraph

    def checkCoordinateList(self, coordinatesList):
        """

        :param coordinatesList: [(longitude, latitude)]
        :return:
        """

        for idx, coordinates in enumerate(coordinatesList):
            if not self.inEdgeList(coordinates):
                coordinatesList[idx] = self.closestRoadCoordinate(coordinates)

        return coordinatesList

    def closestRoadCoordinate(self, coordinates):
        """

        :param coordinates:
        :return:
        """
        coordinates = coordinate.closestTo(coordinates, self.handler.roadMapGraph.keys())

        return coordinates

    def findBusStopName(self, lon, lat):
        """

        :param lon:
        :param lat:
        :return:
        """
        for nd in self.busStopList:
            if nd.longitude == lon and nd.latitude == lat:
                return nd.name
        return None

    def findBusStopPosition(self, name):
        """

        :param name:
        :return:
        """
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
                return center

            else:
                if number in self.handler.addresses[address].numbers:
                    noCoord = self.handler.addresses[address].numbers[number]
                    return noCoord
                else:
                    # TODO Find closest housenumber to number
                    return self.findCoordinatesFromAdress(address)
        else:
            return None

    def findRoute(self, startCoord, endCoord):
        """
        Finds a route between two points in the map. Uses the A* algorithm to
        find this path.

        :param startCoord: id of the starting node
        :param endCoord: id of the ending node
        :return: a path between the start and ending point and the to take that
                path
        """

        if not self.inEdgeList(startCoord):
            startCoord = self.closestRoadCoordinate(startCoord)

        if not self.inEdgeList(endCoord):
            print "NOOO!"

        path, cost = self.astar.findPath(self.edges, startCoord, endCoord)

        travelTime = cost[endCoord][0]
        return path, travelTime

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
        coordList = self.checkCoordinateList(coordinateList)

        path = []
        cost = [0]

        if len(coordList) == 1:
            path.append(coordList[0])
        elif len(coordList) > 1:
            path.append(coordList[0])
            for n in range(0, len(coordList) - 1):
                _path, _cost = self.findRoute(coordList[n], coordList[n + 1])
                [path.append(x) for x in _path[1:]]
                cost.append(_cost)

        return path, cost

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

    def inEdgeList(self, sid):
        """

        """
        return sid in self.handler.roadMapGraph

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

    print "We have " + str(len(myMap.handler.roadMapGraph)) + " nodes in total"
    print "We have " + str(len(myMap.busStopList)) + " bus stops in total\n"

    print "\nFinding path... "
    # Flogsta vårdcentral
    nTo = (17.5817552, 59.8507556)
    # Polacksbacken
    nFrom = (17.6476356, 59.8402172)

    """
    timer = time.time()
    myPath, cost = myMap.findRoute(nFrom, nTo)
    print "Found path in: %f sec, cost: %f sec\n" % (
        (time.time() - timer), cost)

    print "Draw image ..."
    img = DrawImage(3000,
                    myMap.handler.minlon,
                    myMap.handler.minlat,
                    myMap.handler.maxlon,
                    myMap.handler.maxlat)

    img.drawRoads(myMap.handler.roadMapGraph)
    # img.drawNodes(myMap.nodes, 'green')
    # img.drawNodeList(myMap.nodes, 'blue')
    # img.drawNodeList([myMap.nodes[x] for x in myMap.handler.NOD], 'red')
    img.drawPath(myPath, 'red')
    img.drawBusStops(myMap.busStopList)
    img.drawSave(sys.argv[1])
    """
    b = BusNetwork()
    b.makeBusGraph(myMap.handler.busStops, myMap.handler.roadMapGraph)

