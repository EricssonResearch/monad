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

import json
import requests
import multiprocessing
# from multiprocessing import Pool

ROUTES_GENERATOR_HOST = 'http://localhost:'
ROUTES_GENERATOR_PORT = '9998'

# url = 'http://localhost:8888/get_nearest_stop'
headers = {'Content-type': 'application/x-www-form-urlencoded'}
print_lock = multiprocessing.Lock()

def get_nearest_stop(address):
    url = ROUTES_GENERATOR_HOST + ROUTES_GENERATOR_PORT + '/get_nearest_stop'
    data = {"address" : address}
    data_json = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    # if response.status_code == 200:
    print_lock.acquire()
    print '\nRequest: get_nearest_stop' \
          '\nData: ', data, \
          '\nResponse status: ', response.status_code, \
          '\nResponse: ', response.text, '\n'
    print_lock.release()

def get_nearest_stop_from_coordinates():
    url = ROUTES_GENERATOR_HOST + ROUTES_GENERATOR_PORT + '/get_nearest_stop_from_coordinates'
    #data = {'lon': 17.6666581, 'lat': 59.8556742}
    data = {'lat': 59.8578199, 'lon': 17.6093985}
    data_json = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    print_lock.acquire()
    print '\nRequest: get_nearest_stop_from_coordinates' \
          '\nData: ', data, \
          '\nResponse status: ', response.status_code, \
          '\nResponse: ', response.text, '\n'
    print_lock.release()

def get_route():
    url = ROUTES_GENERATOR_HOST + ROUTES_GENERATOR_PORT + '/get_route_from_coordinates'
    data = {'list': "[(17.6130204, 59.8545318), (17.5817552, 59.8507556), (17.6476356, 59.8402173)]"}
    #data = {'list': 17.6666581, 'lat': 59.8556742}
    data_json = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    print_lock.acquire()
    print '\nRequest: get_route_from_coordinates' \
          '\nData: ', data, \
          '\nResponse status: ', response.status_code, \
          '\nResponse: ', response.text, '\n'
    print_lock.release()


def get_coordinates(address, street_no=u'None'):
    url = ROUTES_GENERATOR_HOST + ROUTES_GENERATOR_PORT + '/get_coordinates_from_address'
    data = {'address': address, 'street_no': street_no}
    data_json = json.dumps(data)
    response = requests.post(url, data=data, headers=headers)
    print_lock.acquire()
    print '\nRequest: get_coordinates_from_address' \
          '\nData: ', data, \
          '\nResponse status: ', response.status_code, \
          '\nResponse: ', response.text, '\n'
    print_lock.release()

def get_coordinates_string(string):
    url = ROUTES_GENERATOR_HOST + ROUTES_GENERATOR_PORT + '/get_coordinates_from_string'
    data = {'string': string}
    response = requests.post(url, data=data, headers=headers)
    print_lock.acquire()
    print '\nRequest: get_coordinates_from_string' \
          '\nData: ', data, \
          '\nResponse status: ', response.status_code, \
          '\nResponse: ', response.text, '\n'
    print_lock.release()

if __name__ == '__main__':
    #pool = multiprocessing.Pool(processes = 5)
    #pool.map(get_nearest_stop, [i for i in range(0, 1000)])
    print "----- test1 -----"
    get_nearest_stop_from_coordinates()
    print "----- test2 -----"
    get_nearest_stop(1)
    print "----- test3 -----"
    get_route()
    print "----- test4 -----"
    get_coordinates("Nordengatan")
    print "----- test5 -----"
    get_coordinates("Studentvägen", u'20')
    print "----- test6 -----"
    get_coordinates_string("Studentvägen")
    print "----- test7 -----"
    get_coordinates_string("Studentvägen 4")
    print "----- test8 -----"
    get_coordinates_string("Sernanders väg")
