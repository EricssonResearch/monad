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
import time
import coordinate


class BusNetwork:

    def __init__(self):
        pass

    def busStar(self, nodes, edges, start, goal):
        pass

    def makeBusGraph(self, nodes, busStopNode, edges):

        graph = {}

        i = 0
        l = len(busStopNode)
        timer = time.time()
        for idA, busStopA in busStopNode.items():
            #if busStopA.name not in [u'Akademiska ingång 10', u'Akademiska ingång 30-50']:
            #    continue

            if busStopA.name not in graph:
                graph[busStopA.name] = {}

            i += 1
            print "\n%f s\n (%d / %d) - %s" % (time.time() - timer, i, l, busStopA.name)
            timer = time.time()
            for idB, busStopB in busStopNode.items():

                if busStopB.name not in graph[busStopA.name] and busStopA != busStopB:

                    print '\033[91m' + '.' + '\033[0m',

                    path, cost = self.findPath(nodes, edges, graph, idA, idB, busStopNode)

                    start = busStopA.name
                    startID = idA
                    _cameFrom = []
                    for node in path[1:]:
                        id = node

                        if id in busStopNode:
                            b = busStopNode[id].name

                            if start not in graph:
                                graph[start] = {}

                            graph[start][b] = (cost[id] - cost[startID], True)

                            if b not in graph[busStopA.name]:
                                graph[busStopA.name][b] = (cost[id] - cost[idA], False)
                                if busStopA.name in [u'Akademiska ingång 10']:
                                    print "!",
                                pass
                            if busStopB.name not in graph[start]:
                                graph[start][busStopB.name] = (cost[id] - cost[idA], False)
                                if start in [u'Akademiska ingång 10']:
                                    print "!",
                                pass

                            for Cid in _cameFrom:
                                if b not in graph[busStopNode[Cid].name]:
                                    graph[busStopNode[Cid].name][b] = (cost[id] - cost[Cid], False)
                                    if busStopNode[Cid].name in [u'Akademiska ingång 10']:
                                        print "!",
                                    pass

                            _cameFrom.append(startID)
                            start = b
                            startID = id

        for nodeA in graph:
            for nodeB in graph[nodeA]:
                if graph[nodeA][nodeB][1]:
                    print nodeA, "->", nodeB, " : ", graph[nodeA][nodeB]

        return graph


    def findPath(self, nodes, edges, graph, start, goal, busStops):
        """

        """

        standardSpeed = 50
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


            if current in busStops and busStops[current].name in graph:
                if busStops[goal].name in graph[busStops[current].name]:
                    c, _ = graph[busStops[current].name][busStops[goal].name]
                    # TODO
                    #cost[goal] = cost[current] + c
                    #path[goal] = current
                    goal = current
                    break

            # For all nodes connected to the one we are looking at for the
            # moment.
            for nextNode, speed, roadInt, _ in edges[current]:
                # How fast you can go on a road matters on the type of the road
                # It can be seen as a penalty for "smaller" roads.
                speedDecrease = (1 - (float(roadInt) / 50))
                fromCoordinate = nodes[current]
                toCoordinate = nodes[nextNode]

                roadLength = coordinate.measure(fromCoordinate, toCoordinate)

                timeOnRoad = (roadLength /
                              (speedDecrease * (float(speed) * 1000 / 3600)))

                newCost = cost[current] + timeOnRoad

                if nextNode not in cost or newCost < cost[nextNode]:
                    cost[nextNode] = newCost

                    weight = (newCost + (roadInt ** 1) +
                              (self.heuristic(nodes[nextNode], nodes[goal])*2 /
                               (float(standardSpeed) * 1000 / 3600)))

                    heappush(openSet, (weight, nextNode))
                    path[nextNode] = current

        return self.reconstruct_path(path, start, goal), cost

    def heuristic(self, node, goal):
        return coordinate.measure(node, goal)

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path