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

import math
import numpy as np


class Coordinate(object):
    """
    A geographic coordinate on a map represented by Latitude and Longitude.

    Longitude and Latitude are floating point values in degrees.
    """

    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    @property
    def coordinates(self):
        return (self.longitude, self.latitude)

    def longitude(self):
        return self.longitude

    def latitude(self):
        return self.latitude


# def measure(lon1, lat1, lon2, lat2):
def measure(coordinate1, coordinate2):
    """
    Measure the distance between to points in lon and lat and returns the
    distance in meters.
    """
    if isinstance(coordinate1, Coordinate):
        lon1, lat1 = coordinate1.coordinates
    else:
        lon1, lat1 = coordinate1

    if isinstance(coordinate2, Coordinate):
        lon2, lat2 = coordinate2.coordinates
    else:
        lon2, lat2 = coordinate2

    # Radius of the earth in meters
    earthRadius = 6371000
    dLat = (lat2 - lat1) * math.pi / 180
    dLon = (lon2 - lon1) * math.pi / 180

    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(lat1 * math.pi / 180) * math.cos(lat2 * math.pi / 180) *
         math.sin(dLon / 2) * math.sin(dLon / 2))

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    meters = earthRadius * c

    return meters


def average(coordinateList):
    """
    Finds the average value for the longitude and latitude values in the
    coordinateList.

    :param coordinateList: [Coordinate]
    :return: Coordinate
    """
    tuplelist = [coordinate.coordinates for coordinate in coordinateList]
    avg = [sum(y) / len(y) for y in zip(*tuplelist)]

    return Coordinate(avg[0], avg[1])


def center(coordinateList):
    """
    Finds the center of multiple geographic coordinates.

    :param coordinateList: [Coordinate]
    :return: Coordinate
    """
    tuplelist = [coordinate.coordinates for coordinate in coordinateList]
    _max = reduce(lambda x, y: (max(x[0], y[0]), max(x[1], y[1])), tuplelist)
    _min = reduce(lambda x, y: (min(x[0], y[0]), min(x[1], y[1])), tuplelist)
    longitude = _max[0] - ((_max[0] - _min[0]) / 2)
    latitude = _max[1] - ((_max[1] - _min[1]) / 2)

    return Coordinate(longitude=longitude, latitude=latitude)


def closestTo(coord, coodinateList):
    """
    Finds the closest coordinate to the coordinate coord in a coordinate list.

    :param coord: tuple of two floats, (longitude, latitude)
    :param coordinateList: list of tuples of two floats, [(lon, lat)]
    :return: tuple of two floats, an element in coordinateList
    """
    coordinates = np.asarray(coodinateList)
    deltas = coordinates - coord
    dist = np.einsum('ij,ij->i', deltas, deltas)

    return coodinateList[np.argmin(dist)]


def y2lat(y):
    """
    Translates a y-axis coordinate to longitude geographic coordinate, assuming
    a spherical Mercator projection.

    :param y: float
    :return: float
    """
    return 180.0 / math.pi * (2.0 * math.atan(math.exp(y * math.pi / 180.0)) -
                              math.pi / 2.0)


def lat2y(latitude):
    """
    Translates a latitude coordinate to a projection on the y-axis, using
    spherical Mercator projection.

    :param latitude: float
    :return: float
    """
    return 180.0 / math.pi * (math.log(math.tan(math.pi / 4.0 + latitude *
                                                (math.pi / 180.0) / 2.0)))
