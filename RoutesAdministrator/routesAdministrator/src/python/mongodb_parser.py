'''
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the 'License'); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
'''
import json
import datetime
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import urllib2, urllib
import string
import xml.etree.ElementTree
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree

def start(host):
    global mongo_client
    mongo_client = MongoClient(host, 27017)
    global db
    db = mongo_client.monad1
    global bus_trip_collection
    bus_trip_collection = db.BusTrip
    global bus_stop_collection
    bus_stop_collection = db.BusStop
    global user_trip_collection
    user_trip_collection = db.UserTrip
    global secure_key
    secure_key = 'AvlEK4dxNCW1GZRjhXQq1S57gprUKWV2-DXms3TrExBfxO1vSxLDoYxSDDLBFcMp'

def vehicle_get_next_trip(bus_id):
    trips = list(bus_trip_collection.find({'busID' : bus_id}))
    now = datetime.datetime.now()# - datetime.timedelta(days = 1)
    min = datetime.timedelta(weeks = 1)

    for trip in trips:
        if now < trip['startTime']:
            if trip['startTime'] - now < min:
                min = trip['startTime'] - now
                nearest_trip = trip

    if nearest_trip is None:
        return -1

    trajectory = nearest_trip['trajectory']

    for trajectory_point in trajectory:
        trajectory_point['busStop']= bus_stop_collection.find_one({'_id' : ObjectId(trajectory_point['busStop'])})

    return dumps(nearest_trip)

def send_notification_binary(user_to_send_to, message_title, message_body):
	message_title_to_send = ''.join([chr(c) for c in message_title])
	message_body_to_send = ''.join([chr(c) for c in message_body])
	send_notification(user_to_send_to, message_title_to_send, message_body_to_send)

def send_notification(user_to_send_to, message_title_to_send, message_body_to_send):
    API_KEY='key=AIzaSyAPIZuvmfsf8TZHz3q09G_9evAmGUekdrI'
    url = 'https://gcm-http.googleapis.com/gcm/send'

    message_title_to_send = surround_in_quotes(message_title_to_send)
    message_body_to_send = surround_in_quotes(message_body_to_send)
    user_to_send_to = surround_in_quotes(user_to_send_to)
    user_to_send_to = user_to_send_to[1:-1]

    custom_header = {
        'Content-Type' : 'application/json',
        'Authorization' : API_KEY
    }

    message_payload = {
        'title' : message_title_to_send,
        'message' : message_body_to_send
    }

    message_body = {
        'to' : user_to_send_to,
        'data' : message_payload
    }

    try:
        response = requests.post(url, headers = custom_header, data = dumps(message_body))

        if (response.status_code == 200):
            print(response.content)
            print(response.status_code)
        else:
            print("Error with http status_code " + str(response.status_code))
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message

def get_passengers(bus_trip_id, current_bus_stop, next_bus_stop):
    boarding = 0
    departing = 0
    user_trips = user_trip_collection.find({'busTripID' : ObjectId(bus_trip_id)})

    for user_trip in user_trips:
        if user_trip['startBusStop'] == next_bus_stop:
            boarding = boarding + 1
        elif user_trip['endBusStop'] == current_bus_stop:
            departing = departing + 1

    response = {'boarding' : boarding, 'deparing' : departing}
    return dumps(response)

def get_traffic_information():
    south_latitude = '59.818882'
    west_longitude = '17.472703'
    north_latitude = '59.949800'
    east_longitude = '17.818773'
    URL = 'http://dev.virtualearth.net/REST/V1/Traffic/Incidents/' + \
          south_latitude + ',' + \
          west_longitude + ',' + \
          north_latitude + ',' + \
          east_longitude + \
          '/true?t=9&s=2,3&o=xml&key=' + \
          secure_key

    response = urllib.urlopen(URL).read()
    root = ET.fromstring(response)
    return parse_root(root)

def get_traffic_information_with_params(south_latitude, west_longitude, north_latitude, east_longitude):
    URL = 'http://dev.virtualearth.net/REST/V1/Traffic/Incidents/' + \
          south_latitude + ',' + \
          west_longitude + ',' + \
          north_latitude + ',' + \
          east_longitude + \
          '/true?t=9&s=2,3&o=xml&key=' + \
          secure_key

    response = urllib.urlopen(URL).read()
    root = ET.fromstring(response)
    return parse_root(root)

def parse_root(root):
    traffic_dic = {}
    index = 0

    for traffic_incident in root.iter('{http://schemas.microsoft.com/search/local/ws/rest/v1}TrafficIncident'):
        traffic_dic[index] = {}
        traffic_dic[index]['StartPointLatitude'] = traffic_incident[0][0].text
        traffic_dic[index]['StartPointLongitude'] = traffic_incident[0][1].text
        traffic_dic[index]['LastModifiedUTC'] = traffic_incident[3].text
        traffic_dic[index]['StartTimeUTC'] = traffic_incident[4].text
        traffic_dic[index]['EndTimeUTC'] = traffic_incident[5].text
        traffic_dic[index]['IncidentType'] = traffic_incident[6].text
        traffic_dic[index]['IncidentSeverity'] = traffic_incident[7].text
        traffic_dic[index]['RoadClosed'] = traffic_incident[9].text
        traffic_dic[index]['Description'] = traffic_incident[10].text
        traffic_dic[index]['StopPointLatitude'] = traffic_incident[11][0].text
        traffic_dic[index]['StopPointLongitude'] = traffic_incident[11][1].text
        index = index + 1

    return dumps(traffic_dic)
