#!/usr/bin/python
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
import ast
import multiprocessing
import requests
import six

ROUTES_GENERATOR_HOST = 'http://130.238.15.241:'
ROUTES_GENERATOR_PORT = '9998'

headers = {'Content-type': 'application/x-www-form-urlencoded'}
print_lock = multiprocessing.Lock()


def string_to_coordinates(string):
    """
    Translates a string to a bus stop or address. If there is no address or
    bus stop with that name, both address and bus_stop are False and longitude
    and latitude have the value None.

    :param string: Name of a bus stop or an address
    :return: a dictionary, {_id: integer
                            address: True|False
                            bus_stop: True|False
                            latitude: float|None
                            longitude: float|None
                            }
    """
    if not isinstance(string, six.string_types):
        raise ValueError("%r is not a string." % (string,))

    url = (ROUTES_GENERATOR_HOST +
           ROUTES_GENERATOR_PORT +
           '/get_coordinates_from_string')

    data = {'string': string}
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 500:
        response = {'error': "Yes"}
    else:
        response = response.json()

    return response


def coordinates_to_nearest_stops(longitude, latitude, distance):
    """
    Finds the nearest bus stops according to the coordinates supplied and the
    maximum distance.

    :param longitude: float
    :param latitude: float
    :return: a dictionary: {_id: integer
                            name: String, name of the bus stop
                            latitude: float
                            longitude: float
                            distance: float
                            }
    """
    url = (ROUTES_GENERATOR_HOST +
           ROUTES_GENERATOR_PORT +
           '/get_nearest_stops_from_coordinates')

    data = {'lat': float(latitude), 'lon': float(longitude),
            'distance': float(distance)}
    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 500:
        response = {'error': "Yes"}
    else:
        response = response.json()
        response['bus_stops'] = ast.literal_eval(response['bus_stops'])

    return response


def coordinates_to_nearest_stop(longitude, latitude):
    """

    :param longitude:
    :param latitude:
    :return:
    """
    url = (ROUTES_GENERATOR_HOST +
           ROUTES_GENERATOR_PORT +
           '/get_nearest_stops_from_coordinates')

    data = {'lat': float(latitude), 'lon': float(longitude), 'distance': 0.0}
    response = requests.post(url, data=data, headers=headers)

    busStop = {}

    if response.status_code == 500:
        busStop = {'error': "Yes"}
    else:

        response = response.json()
        response['bus_stops'] = ast.literal_eval(response['bus_stops'])

        busStop['_id'] = response['_id']
        busStop['name'] = response['bus_stops'][0][0]
        busStop['longitude'] = response['bus_stops'][0][1][0]
        busStop['latitude'] = response['bus_stops'][0][1][1]

    return busStop


def get_route(coordinates_list):
    """
    Finds the route from a list of destinations. The first element is the
    starting point and the last element is the ending point. Other coordinates
    in the list are intermediate point to visit in increasing order.

    :param coordinates_list: list of coordinates [(longitude, latitude)]
    :return: dict, {_id: integer
                    points: coordinates_list
                    route: list of coordinates, [(longitude, latitude)] the
                        route.
                    start: coordinates_list[0]
                    end: coordinates_list[-1]
                    cost: [float], the cost in sec to get between two points on
                        the route. cost[0] = cost for route between points[0]
                        and points[1].
                    }
    """
    for item in coordinates_list:
        if not len(item) == 2:
            raise ValueError("Not a tuple of two")
        a, b = item
        if not abs(float(a)) < 181 and not abs(float(b)) < 181:
            raise ValueError("Out of range")

    url = (ROUTES_GENERATOR_HOST +
           ROUTES_GENERATOR_PORT +
           '/get_route_from_coordinates')

    data = {'list': str(coordinates_list)}


    response = requests.post(url, data=data, headers=headers)

    if response.status_code == 500:
        response = {'error': "Yes"}
    else:
        response = response.json()
        response['route'] = ast.literal_eval(response['route'])
        response['end'] = ast.literal_eval(response['end'])
        response['points'] = ast.literal_eval(response['points'])
        response['start'] = ast.literal_eval(response['start'])
        response['cost'] = ast.literal_eval(response['cost'])

    return response


if __name__ == '__main__':
    print string_to_coordinates("Polacksbacken 10")
    print string_to_coordinates("SernandeRs VäG 10")
    print get_route([(17.6130204, 59.8545318),
                     (17.5817552, 59.8507556),
                     (17.6476356, 59.8402173)])
    print get_route([])
    print coordinates_to_nearest_stops(latitude=59.8710848,
                                       longitude=17.6546528,
                                       distance=300.0)
