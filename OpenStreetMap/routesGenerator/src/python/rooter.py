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

from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, cast
from json import dumps
import re

from router import Map

#the_map = Map("testmap.xml")
the_map = Map("../UppsalaTest.osm")


def start():
    set_message_handler(message_handler)
    the_map.parsData()


def stop():
    print 'Stop'


def message_handler(message):
    if isinstance(message, tuple):
        message_length = len(message)
        if message[0] == Atom('get_nearest_stop') and message_length == 3:
            address = message[1]
            pid = message[2]
            get_nearest_stop(address, pid)
        elif message[0] == Atom('get_nearest_stop_from_coordinates'):
            lon = message[1]
            lat = message[2]
            pid = message[3]
            get_nearest_stop_from_coordinates(lon, lat, pid)
        elif message[0] == Atom('get_route_from_coordinates'):
            list = message[1]
            pid = message[2]
            get_route_from_coordinates(list, pid)
        elif message[0] == Atom('get_coordinates_from_address'):
            address = message[1]
            street_no = message[2]
            pid = message[3]
            get_coordinates_from_address(address, street_no, pid)
        elif message[0] == Atom('get_coordinates_from_string'):
            string = message[1]
            pid = message[2]
            get_coordinates_from_string(string, pid)
        else:
            print message[0]
    else:
        print 'No'


def get_nearest_stop(address, pid):
    # Initially address is in binary list format thus, needs processing
    address_str = ''.join(chr(i) for i in address)
    busStop = {}
    busStop['_id'] = "1234"
    busStop['name'] = "foo"
    busStop['latitude'] = 100.00
    busStop['longitude'] = 200.00
    busStop['address'] = address_str
    response = Atom("ok"), dumps(busStop)
    cast(pid, response)


def get_nearest_stop_from_coordinates(lon, lat, pid):
    longitude = ''.join(chr(i) for i in lon)
    latitude = ''.join(chr(i) for i in lat)
    bus_stop = the_map.findClosestBusStopFromCoordinates(float(longitude),
                                                         float(latitude))
    busStop = {}
    busStop['_id'] = "1234"
    busStop['name'] = bus_stop.name
    busStop['longitude'] = bus_stop.longitude
    busStop['latitude'] = bus_stop.latitude
    response = Atom("ok"), dumps(busStop)
    cast(pid, response)


def get_coordinates_from_address(address, street_no, pid):
    address_str = ''.join(chr(i) for i in address)
    num_str = ''.join(chr(i) for i in street_no)
    if num_str == 'None':
        num_str = None
    addressCoordinate = the_map.findCoordinatesFromAdress(address_str, num_str)
    addr = {}
    addr['_id'] = "4321"
    addr['address'] = address
    addr['street_no'] = num_str
    if addressCoordinate is not None:
        lon, lat = addressCoordinate.coordinates
        addr['longitude'] = lon
        addr['latitude'] = lat
    else:
        addr['longitude'] = None
        addr['latitude'] = None

    response = Atom("ok"), dumps(addr)
    cast(pid, response)


def get_route_from_coordinates(coordinates_str_list, pid):
    coordinate_str = ''.join(chr(i) for i in coordinates_str_list)
    coordinates_list = ast.literal_eval(coordinate_str)
    route, cost = the_map.findRouteFromCoordinateList(coordinates_list)
    if not route:
        route = [None]
    path = {}
    path['_id'] = 1212
    path['points'] = coordinate_str
    path['route'] = str(route)
    path['start'] = str(route[0])
    path['end'] = str(route[-1])
    path['cost'] = str(cost)

    response = Atom("ok"), dumps(path)
    cast(pid, response)


def get_coordinates_from_string(string, pid):
    string_str = ''.join(chr(i) for i in string)
    data = {}
    data['_id'] = 12312
    addr = False
    busStop = False
    coordinates = None
    searchObject = re.search('\d+[a-zA-Z]*', string_str)
    if searchObject is not None:
        address = re.sub('\d+[a-zA-Z]*', "", string_str).strip()
        num = searchObject.group()
        coordinates_obj = the_map.findCoordinatesFromAdress(address, num)
        if coordinates_obj is not None:
            addr = True
            coordinates = coordinates_obj.coordinates
    else:
        coordinates = the_map.findBusStopPosition(string_str)
        if coordinates is not None:
            busStop = True
        else:
            coordinates_obj = the_map.findCoordinatesFromAdress(string_str)
            if coordinates_obj is not None:
                addr = True
                coordinates = coordinates_obj.coordinates

    data['address'] = addr
    data['bus_stop'] = busStop
    if coordinates is not None:
        data['longitude'] = coordinates[0]
        data['latitude'] = coordinates[1]
    else:
        data['longitude'] = None
        data['latitude'] = None

    response = Atom("ok"), dumps(data)
    cast(pid, response)
