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


class AStar:
    standardSpeed = 50

    def __init__(self, standardSpeed):
        self.standardSpeed = standardSpeed

#    def getNodeById(self, nodes, nodeId):
#        for nd in nodes:
#            if nd.id == nodeId:
#                return nd
#        return -1

    def findPath(self, edges, start, goal):
        """
        Finds a path between start and goal using A*. The search is done in the
        graph self.edges.
        """
        openSet = []
        heappush(openSet, (0, start))
        path = {}
        cost = {}
        path[start] = 0
        cost[start] = np.asarray([0, 0])

        # A value that a real path should not have.
        cost[goal] = np.asarray([float('Inf'), float('Inf')])

        if start == goal:
            cost[goal] = np.asarray([0, 0])
            openSet = []

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
                #fromCoordinate = nodes[current]
                #toCoordinate = nodes[nextNode]

                roadLength = coordinate.measure(current, nextNode)

                timeOnRoad = (roadLength /
                              (speedDecrease * (float(speed) * 1000 / 3600)))

                newCost = cost[current] + [timeOnRoad, roadLength]

                if nextNode not in cost or (newCost[0] < cost[nextNode][0]):
                    cost[nextNode] = newCost

                    weight = (newCost[0] + (roadInt ** 1) +
                              (heuristic(nextNode, goal) /
                               (float(self.standardSpeed) * 1000 / 3600)))

                    heappush(openSet, (weight, nextNode))
                    path[nextNode] = current

        # Is there a shortest path
        if cost[goal][0] is float('Inf'):
            shortestpath = []
        else:
            shortestpath = reconstruct_path(path, start, goal)

        return shortestpath, cost


def heuristic(node, goal):
    """
    The heuristic used by A*. It measures the length between node and goal
    in meters.
    :param node a Coordinate object
    :param goal a Coordinate object
    :return the distance in meters
    """
    return coordinate.measure(node, goal)


def reconstruct_path(came_from, start, goal):
    """

    """
    current = goal
    path = [current]
    while current != start:
        if current not in came_from:
            current = start
            path = []
        else:
            current = came_from[current]
            path.append(current)
    path.reverse()
    return path


def pathLenght(path):
    l = 0
    for n in range(len(path) - 2):
        l += coordinate.measure(path[n], path[n+1])

    return l
