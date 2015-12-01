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

import json
import requests
import multiprocessing
# from multiprocessing import Pool

ROUTES_ADMINISTRATOR_HOST = 'http://localhost:'
ROUTES_ADMINISTRATOR_PORT = '9997'

# url = 'http://localhost:8888/get_nearest_stop'
headers = {'Content-type': 'application/x-www-form-urlencoded'}
print_lock = multiprocessing.Lock()

def vehicle_get_next_trip(vehicle_id):
    url = ROUTES_ADMINISTRATOR_HOST + ROUTES_ADMINISTRATOR_PORT + '/vehicle_get_next_trip'
    data = {"vehicle_id" : vehicle_id}
    data_json = json.dumps(data)
    response = requests.post(url, data = data, headers = headers)
    # if response.status_code == 200:
    print_lock.acquire()
    print '\nRequest: vehicle_get_next_trip' \
          '\nData: ', data, \
          '\nResponse status: ', response.status_code, \
          '\nResponse: ', response.text, '\n'
    print_lock.release()

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes = 1)
    pool.map(vehicle_get_next_trip, [1])
    # pool.map(vehicle_get_next_trip, [i for i in range(0, 1000)])
