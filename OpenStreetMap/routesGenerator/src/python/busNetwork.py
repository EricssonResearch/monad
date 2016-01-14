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

from heapq import heappush, heappop
import numpy as np

import coordinate
import aStar


class BusNetwork:

    def __init__(self):
        self.graph = {}
        self.busStopDict = []
        pass


    def makeBusStopDict(self, busStops):
        """
        Makes a bus stop dictionary from a list of bus stops. The key is the
        coordinates to the bus stop. The values is the bus stop.

        :param busStops: the list of bus stops, [<busstop>]
        :return: dictonary,
        """
        dict = {}

        for busstop in busStops:
            dict[busstop.coordinates] = busstop

        return dict

    def addEdges(self, path, cost):
        """
        Added edges to the bus stop graph. Uses the self.graph.

        :param path: A path of coordinates.
        """

        for idxA, from_stop_coord_A in enumerate(path):

            if from_stop_coord_A in self.busStopDict:
                from_bus = self.busStopDict[from_stop_coord_A]

                if from_bus not in self.graph:
                    self.graph[from_bus] = {}

                next_stop = True
                pass_through = None

                for idxB in range(idxA+1, len(path)):

                    if path[idxB] not in self.busStopDict:
                        continue

                    to_bus = self.busStopDict[path[idxB]]

                    if to_bus not in self.graph[from_bus]:

                        if next_stop:
                            _tuple = (True, path[idxA:(idxB+1)],
                                      cost[idxA:(idxB+1)] - cost[idxA])

                            self.graph[from_bus][to_bus] = _tuple

                        else:
                            _tuple = (False, pass_through, None)
                            self.graph[from_bus][to_bus] = _tuple

                        if next_stop:
                            next_stop = False
                            pass_through = [to_bus]

    def edgeInGraph(self, frm, to):
        """
        Checks if an edge is in self.graph.

        :param frm: Coordinate
        :param to: Coordinate
        :return: True | False
        """
        val = False
        if frm in self.graph:
            if to in self.graph[frm]:
                val = True

        return val

    def makeBusGraph(self, busStops, edges):
        """
        Creates the bus network as a graph.
        """

        self.busStopDict = self.makeBusStopDict(busStops)

        for busStopA in busStops:

            for busStopB in busStops:

                if not self.edgeInGraph(busStopA, busStopB) and busStopA != busStopB:

                    path, cost = self.findPath(edges, busStopA, busStopB)
                    self.addEdges(path, cost)

        return self.graph

    def findPath(self, edges, startBusStop, goalBusStop):
        """
        A*, with the added search in the self.graph to speed up the process
        of creating the graph.
        """
        start = startBusStop.coordinates
        goal = goalBusStop.coordinates

        standardSpeed = 50
        openSet = []
        heappush(openSet, (0, start))
        path = {}
        cost = {}
        # A value that a real path does not have.
        cost[goal] = np.asarray([float('Inf'), float('Inf')])
        path[start] = 0
        cost[start] = np.asarray([0, 0])

        # As long as there are paths to be explored
        while not (len(openSet) == 0):
            current = heappop(openSet)[1]

            # We found the goal, stop searching, we are done.
            if current == goal:
                break

            if current in self.busStopDict and self.busStopDict[current] in self.graph:
                if self.busStopDict[goal] in self.graph[self.busStopDict[current]]:

                    openSet = []

                    if not self.graph[self.busStopDict[current]][self.busStopDict[goal]][0]:

                        sub_station = self.graph[self.busStopDict[current]][goalBusStop]
                        sub_station = sub_station[1]

                        sub_path = self.graph[self.busStopDict[current]][sub_station[0]]
                        sub_path = sub_path[1]
                    else:
                        sub_path = self.graph[self.busStopDict[current]][self.busStopDict[goal]][1]

                    previous_node = sub_path[0]
                    for node in sub_path:

                        if node not in path:
                            path[node] = previous_node

                            newCost = cost[previous_node] + [1, 1]
                            cost[node] = newCost

                        previous_node = node

                    heappush(openSet, (0, previous_node))
                    continue

            # For all nodes connected to the one we are looking at for the
            # moment.
            for nextCoord, speed, roadInt, _ in edges[current]:
                # How fast you can go on a road matters on the type of the road
                # It can be seen as a penalty for "smaller" roads.
                speedDecrease = (1 - (float(roadInt) / 50))

                roadLength = coordinate.measure(current, nextCoord)

                timeOnRoad = (roadLength /
                              (speedDecrease * (float(speed) * 1000 / 3600)))

                newCost = cost[current] + [timeOnRoad, roadLength]

                if nextCoord not in cost or newCost[0] < cost[nextCoord][0]:
                    cost[nextCoord] = newCost

                    weight = (newCost[0] + (roadInt ** 2) +
                              (self.heuristic(nextCoord, goal)*2 /
                               (float(standardSpeed) * 1000 / 3600)))

                    heappush(openSet, (weight, nextCoord))
                    path[nextCoord] = current

        _path = aStar.reconstruct_path(path, start, goal)

        _keys = []
        for k in cost:
            if k not in _path:
                _keys.append(k)
        for k in _keys:
            cost.pop(k)

        return _path, self.reconstruct_cost(_path, cost)

    def heuristic(self, node, goal):
        return coordinate.measure(node, goal)

    def reconstruct_cost(self, path, cost):
        """
        Makes a list corresponding to the cost to take the steps in the list
        path.

        :param path: list of coordinates
        :param cost: the cost dictionary from finding the path
        :return: list of costs
        """
        _cost = []

        for coord in path:
            _cost.append(cost[coord])

        return np.asarray(_cost)


def graphData(path, cost, a, b, direct):
    """
    Arranges data in the right format for the graph.
    """
    if direct:
        pass
    subpath = path[path.index(a):path.index(b) + 1]
    subcost = {}

    startCost = cost[subpath[0]]
    for nd in subpath:
        subcost[nd] = cost[nd] - startCost

    return direct, subpath, subcost

