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
import Image
import ImageDraw
# from Tkinter import Tk, Canvas, Frame, BOTH
import coordinate


class DrawImage:
    # Contains some drawing functions that can/should be left out. They are
    # mainly used for testing the other functions.

    def __init__(self, imageWidth, minlon, minlat, maxlon, maxlat):
        self.minlon = minlon
        self.maxlon = maxlon
        self.minlat = minlat
        self.maxlat = maxlat

        self.lonLength = (self.maxlon - self.minlon)
        self.imgScaling = (imageWidth / self.lonLength)

        imageHight = ((coordinate.lat2y(self.maxlat) -
                       coordinate.lat2y(self.minlat)) *
                      self.imgScaling)

        self.im = Image.new('RGBA', (imageWidth, int(imageHight)), 'white')
        self.draw = ImageDraw.Draw(self.im)


    def drawSave(self, name):
        self.im.show()
        self.im.save(name)

    def drawNodes(self, nodes, colour):
        y1 = coordinate.lat2y(self.minlat)
        y2 = coordinate.lat2y(self.maxlat)
        y = (y2 - y1) * self.imgScaling

        for id, n in nodes.items():
            pointX = (n.longitude - self.minlon) * self.imgScaling
            pointY = y - (coordinate.lat2y(n.latitude) - y1) * self.imgScaling
            self.draw.point((pointX, pointY), colour)

    """
    def drawNodeIds(self, nodeIds, colour):
        y1 = coordinate.lat2y(self.minlat)
        y2 = coordinate.lat2y(self.maxlat)
        y = (y2 - y1) * self.imgScaling

        for nd in nodeIds:
            n = self.nodes[nd].coordinates
            pointX = (n[0] - self.minlon) * self.imgScaling
            pointY = y - (coordinate.lat2y(n[1]) - y1) * self.imgScaling
            self.draw.point((pointX, pointY), colour)
    """

    def drawRoads(self, edges, nodes):
        y1 = coordinate.lat2y(self.minlat)
        y2 = coordinate.lat2y(self.maxlat)
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
        y1 = coordinate.lat2y(self.minlat)
        y2 = coordinate.lat2y(self.maxlat)
        y = (y2 - y1) * self.imgScaling

        for stop in busStops:
            radius = 2
            if stop.name == '':
                self.drawCircle(y, y1, stop.longitude, stop.latitude,
                                radius, self.imgScaling, (110, 50, 200))
            else:
                self.drawCircle(y, y1, stop.longitude, stop.latitude, radius,
                                self.imgScaling, (254, 122, 85))

    """
    def drawPath(self, path, colour):
        y1 = coordinate.lat2y(self.minlat)
        y2 = coordinate.lat2y(self.maxlat)
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
    """

    def drawPoint(self, y, y1, lon, lat, scale, colour):
        pointPX = (lon - self.minlon) * scale
        pointPY = y - ((coordinate.lat2y(lat) - y1) * scale)
        self.draw.point((pointPX, int(pointPY)), colour)

    def drawLine(self, y, y1, aLon, aLat, bLon, bLat, scale, colour):
        pointAX = (aLon - self.minlon) * scale
        pointAY = y - ((coordinate.lat2y(aLat) - y1) * scale)
        pointBX = (bLon - self.minlon) * scale
        pointBY = y - ((coordinate.lat2y(bLat) - y1) * scale)
        self.draw.line((pointAX, pointAY, pointBX, pointBY), colour)

    def drawCircle(self, y, y1, lon, lat, r, scale, colour):
        pointCX = (lon - self.minlon) * scale
        pointCY = y - ((coordinate.lat2y(lat) - y1) * scale)
        self.draw.ellipse((pointCX - r, pointCY - r, pointCX + r, pointCY + r),
                          fill=colour)


#class Example(Frame):
#    def __init__(self, parent):
#        Frame.__init__(self, parent)
#        self.parent = parent
#        self.canvas = Canvas(self)
#
#        self.initUI()
#
#    def initUI(self):
#        self.parent.title("Lines")
#        self.pack(fill=BOTH, expand=1)
#
#        self.canvas.create_line(15, 25, 200, 25)
#        self.canvas.create_line(55, 85, 155, 85, 105, 180, 55, 85)
#
#        self.canvas.pack(fill=BOTH, expand=1)
#
#    def add(self):
#        self.canvas.create_line(300, 35, 300, 200, dash=(4, 2))

