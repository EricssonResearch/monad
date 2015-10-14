#!/usr/bin/python
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

# The size width of the produced image in pixels
picSize = 3000
# The max speed on a road that does not have a set max speed.
standardSpeed = 50
# Roads buses can drive on
busRoadTypes = ('motorway','motorway_link','trunk','trunk_link','primary',
                'primary_link','secondary','secondary_link','tertiary',
                'tertiary_link','unclassified','residential','service')

class RouteHandler(handler.ContentHandler):
    def __init__(self):
        # all nodes in the map
        self.nodes = {}
        # all bus stop nodes
        self.busStops = {}
        self.edges = {}        

        # Used as temp
        self.nd = []
        self.tag = {}
        self.stop = 0
   
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
            id = int(attributes.get('id'))
            lat = float(attributes.get('lat'))
            lon = float(attributes.get('lon'))
            self.nodes[id] = (lon,lat)
            self.stop = id            
        elif name == 'way':
            pass
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
            oneway = self.tag.get('oneway', '') in ('yes','true','1')
            maxspeed = self.tag.get('maxspeed', standardSpeed)

            # If the way is a road and if the bus can drive on it 
            if highway in busRoadTypes:
                roadInt = busRoadTypes.index(highway)
                # add edges between nodes that can be accessed by a bus
                for nd in range(len(self.nd)-1):
                    self.addEdge(self.nd[nd], self.nd[nd+1], maxspeed, roadInt)
                    if not oneway:
                        self.addEdge(self.nd[nd+1], self.nd[nd], maxspeed, roadInt)              

        elif name == 'node':
            # Look for nodes that are bus stops
            highway = self.tag.get('highway','')
            stopName = self.tag.get('name','')
            if highway == 'bus_stop':
                self.addBusStop(stopName,self.stop)

        # Clean up
        if name in('node','way','relation'):
            self.nd = []
            self.tag = {}
            self.stop = 0  
            
    def addEdge(self, fromNode, toNode, maxspeed, roadInt):
        """
        Adds an edge between fromNode to toNode in self.edges with 
        attributes maxspeed, roadInt (type of road)
        """
        if fromNode in self.edges:
            self.edges[fromNode].append((toNode, maxspeed, roadInt))
        else:
            self.edges[fromNode] = [(toNode, maxspeed, roadInt)]
        if not toNode in self.edges:
            self.edges[toNode] = []
    
    def addBusStop(self, name, stop):
        if name in self.busStops:
            self.busStops[name].append(stop)
        else:
            self.busStops[name] = [stop]

    def aStar(self, start, goal):
        """
        Finds a path between start and goal using a*. The search is done in the
        graph self.edges.
        """
        openSet = []
        heappush(openSet,(0,start))
        path = {}
        cost = {}
        path[start] = 0
        cost[start] = 0

        if start == goal:
            cost[goal] = 0
            return path, cost

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
            for nextNode, speed, roadInt in self.edges[current]:
                
                speedDecrease = (1-(float(roadInt)/50))
                timeOnRoad = self.heuristic(self.nodes[current], self.nodes[nextNode]) / (speedDecrease* (float(speed)*1000/3600))
                newCost = cost[current] + timeOnRoad

                if nextNode not in cost or newCost < cost[nextNode]:
                    cost[nextNode] = newCost
                    weight = (newCost + (roadInt**1) + self.heuristic(self.nodes[nextNode], self.nodes[goal]) / (float(standardSpeed)*1000/3600))
                    heappush(openSet,(weight,nextNode))
                    path[nextNode] = current

        return path, cost

    def heuristic(self, node, goal):
        x1,y1 = node
        x2,y2 = goal
        return self.measure(x1,y1,x2,y2)

    def measure(self, lon1,lat1, lon2, lat2): # generally used geo measurement function
        R = 6378.137 #Radius of earth in KM
        dLat = (lat2 - lat1) * math.pi / 180
        dLon = (lon2 - lon1) * math.pi / 180
        a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) * math.sin(dLon/2) * math.sin(dLon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = R * c
        #print d * 1000
        return d * 1000 #// meters

    def reconstruct_path(self, came_from, start, goal):
        current = goal
        path = [current]
        while current != start:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def y2lat(self, a):
        return 180.0/math.pi*(2.0*math.atan(math.exp(a*math.pi/180.0))-math.pi/2.0)
    def lat2y(self, a):
        return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))


    def draw(self, path, start, goal):
        sizelon = (self.maxlon - self.minlon)
        sizeScaling = (picSize/sizelon)

        x = picSize
        y1 = self.lat2y(self.minlat)
        y2 = self.lat2y(self.maxlat)
        y = (y2-y1)*sizeScaling
        print " picture size: (%f,%f) scaling: %f " % (x,y, sizeScaling)
        im = Image.new('RGBA', (x, int(y)), 'white')       
        draw = ImageDraw.Draw(im) 
        
        """Draw all nodes"""
        for id,n in self.nodes.items():
            pointX = (n[0]-self.minlon)*sizeScaling 
            pointY = y-((self.lat2y(n[1])-y1)*sizeScaling)
            draw.point((pointX,pointY), (227, 254, 212,255))
        
        """Draw all roads"""
        for id,n in self.edges.items():
            a = self.nodes[id] 
            #pointAX = (a[0]-self.minlon)*sizeScaling
            #pointAY = y-((self.lat2y(a[1])-y1)*sizeScaling)
            for k,z,i in n: 
                b = self.nodes[k]
                #pointBX = (b[0]-self.minlon)*sizeScaling
                #pointBY = y-((self.lat2y(b[1])-y1)*sizeScaling)
                #draw.line((pointAX, pointAY, pointBX, pointBY), 'black')
                colr = 255 - min(int(255*(float(z)/120)), 255)
                if int(z) < 31:
                    colr = 220
                self.drawLine(draw, y,y1,a[0],a[1],b[0],b[1],sizeScaling, (colr,colr,colr,255))            


        #print "No bus stops: %d" % (len(self.busstops))
        """Draw the busstops""" 
        for stopName, stopIDs in self.busStops.items():
            #print "%s : %d " % (stopName, len(stopIDs)), stopIDs[0:len(stopIDs)]
            r = 2
            if stopName == '':
                for bid in stopIDs:
                    bstop = self.nodes[bid]
                    self.drawCircle(draw, y, y1, bstop[0], bstop[1],r,sizeScaling,(110,50,200))     
            bstop = self.nodes[stopIDs[0]]
            self.drawCircle(draw, y, y1, bstop[0], bstop[1],r,sizeScaling,(254,122,85))
             
         
        """Draw found path"""
        if not path == []:
            pp = 0
            meters = 0
            for pid in path:
                c = self.nodes[pid]
                if pp == 0:
                    pp = c
                else:
                    self.drawLine(draw, y, y1, pp[0],pp[1],c[0],c[1], sizeScaling,'red')
                    meters = meters + self.measure(c[0],c[1],pp[0],pp[1])
                    #print meters
                    pp = c

            #print meters

            startNode = self.nodes[start]
            self.drawPoint(draw,y,y1, startNode[0], startNode[1],sizeScaling, 'green')
        
        im.show()
        im.save('mapdata.png')

    def drawPoint(self,draw, y, y1, lon, lat, scale, colour):
        pointPX = (lon-self.minlon)*scale
        pointPY = y-((self.lat2y(lat)-y1)*scale)
        draw.point((pointPX,int(pointPY)), colour)        

    def drawLine(self, draw, y, y1, aLon, aLat, bLon, bLat, scale, colour):
        pointAX = (aLon-self.minlon)*scale
        pointAY = y-((self.lat2y(aLat)-y1)*scale)
        pointBX = (bLon-self.minlon)*scale
        pointBY = y-((self.lat2y(bLat)-y1)*scale)
        draw.line((pointAX, pointAY, pointBX, pointBY), colour)

    def drawCircle(self, draw, y, y1, lon, lat, r, scale, colour):
        pointCX = (lon-self.minlon)*scale
        pointCY = y-((self.lat2y(lat)-y1)*scale)
        draw.ellipse((pointCX-r, pointCY-r, pointCX+r, pointCY+r), fill=colour)

    def inE(self, sid):
        return self.edges.has_key(sid)
        
    def timeBetweenStops(self, stopA, stopB):
        path, cost = self.aStar(stopA, stopB)
        return cost[stopB]

class AStar:
    pass

class Map:
    
    def __init__(self, omsfilepath):
        self.omsfile = omsfilepath
    
    def parsData(self):
        print "Loading data... (parsing xml)"
        handler = RouteHandler()
        parser = make_parser()
        parser.setContentHandler(handler)
        parser.parse(self.omsfile)
        

    def draw(self, imageName):                                               
        print "draw map!! NO"

    def 

if __name__ == '__main__':
    """
    If the program is run by it self and not used as a library.It will take a 
    osm-file as the first argument, img-file name,  and too IDs of points on
    roads.
    -- python router.py map.png map.osm <ID> <ID>
    If the IDs are left out it will only drae the map.
    """
    print "router.py"


    myMap = Map(sys.argv[2])

    omsfilepath = sys.argv[2]
    print "file: " + omsfilepath 
    timer = time.time()
    print "Loading data ..."
    #handler = RouteHandler()
    #parser = make_parser()
    #parser.setContentHandler(handler)
    #parser.parse(omsfilepath)
    myMap.parsData()
    print "Data loaded in: %f sec" % (time.time() - timer)
    
    print "Draw image ..."
    
    myMap.draw(sys.argv[1])
    # check if the 
    if len(sys.argv) < 5:
        #handler.draw([],0,0)
        myMap.draw("2.png")
    else:
        busstopa = int(sys.argv[3])
        busstopb = int(sys.argv[4])

        if handler.inE(busstopa) and handler.inE(busstopb):

            print "doing path finding ..."
            path, cost = handler.aStar(busstopa, busstopb)
            print "draw ..."
            handler.draw(handler.reconstruct_path(path, busstopa, busstopb),
                         busstopa, busstopb)
        else:
            print "bad match on edges"
    print "Image done"

