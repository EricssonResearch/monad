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

from erlport.erlterms import Atom
from erlport.erlang import set_message_handler, cast
from json import dumps

from router import Map

the_map = Map("../testmap.xml")


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
    #bus_stop_name = the_map.findBusStopName(float(lon), float(lat))
    #bus_stop_name = the_map.testtest(lon, lat)
    longitude = ''.join(chr(i) for i in lon)
    latitude = ''.join(chr(i) for i in lat)
    bus_stop = the_map.findClosestBusStopFromCoordinates(float(longitude),
                                                              float(latitude))
    busStop = {}
    busStop['name'] = bus_stop.name
    busStop['longitude'] = bus_stop.longitude
    busStop['latitude'] = bus_stop.latitude
    response = Atom("ok"), dumps(busStop)
    cast(pid, response)


def address_to_coordinates(address, street_no, pid):
    address_str = ''.join(chr(i) for i in address)
    street_no = ''.join(chr(i) for i in street_no)
    response = ""
    cast(pid, response)
