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

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime
import requests
import json

def start(host, port):
    global mongo_client
    global db
    global recommendations_collection
    global user_trips_collection
    global bus_stop_collection
    global notifications_collection
    global bookings_collection
    mongo_client = MongoClient(host, port)
    db = mongo_client.monad1
    recommendations_collection = db.TravelRecommendation
    user_trips_collection = db.UserTrip
    bus_stop_collection = db.BusStop
    notifications_collection = db.Notifications
    bookings_collection = db.BookedTrip

def parse_recommendations(user_id):
    initially_formatted_recommendations = list(recommendations_collection.find({'userID' : user_id}))
    final_recommendations = list()

    for recommendation in initially_formatted_recommendations:
        user_trip_reference = recommendation['userTrip']
        user_trip = user_trips_collection.find_one({'_id' : ObjectId(user_trip_reference)})
        user_trips_list = parse_user_trip(list(), user_trip)
        recommendation['userTrip'] = user_trips_list
        final_recommendations.append(recommendation)

    return dumps(final_recommendations)

def parse_user_trip(user_trips_list, user_trip):
    if 'next' in user_trip.keys():
        user_trips_list.append(user_trip)
        return parse_user_trip(user_trips_list,
                               user_trips_collection.find_one({'_id' : ObjectId(user_trip['next'])}))
    else:
        user_trips_list.append(user_trip)
        return user_trips_list

def parse_notifications(user_id):
    notifications_list = list(notifications_collection.find({'userID' : user_id}))
    return dumps(notifications_list)

def create_notification(user_id, partial_trips, icon_id):
    notification = {}
    notification['userID'] = user_id
    notification['partialTrips'] = partial_trips
    notification['text'] = 'Booking Confirmation: Enjoy your trip to ' + str(partial_trips[0]['endBusStop'])
    notification['time'] = datetime.datetime.now() - datetime.timedelta(hours = 2)
    notification['iconID'] = icon_id
    return notification

def remove_notification(notification_id_binary):
    notification_id = ''.join([chr(c) for c in notification_id_binary])
    notifications_collection.remove({'_id' : ObjectId(notification_id)})
    return '1'

def generate_notification(user_id, token, booked_trip_id_binary):
    booked_trip_id = ''.join([chr(c) for c in booked_trip_id_binary])
    booking = bookings_collection.find_one({'_id' : ObjectId(booked_trip_id)})
    partial_trips = list()
    partial_trip_ids = booking['partialTrips']

    for partial_trip_id in partial_trip_ids:
        partial_trip = user_trips_collection.find_one({'_id' : partial_trip_id})
        partial_trips.append(partial_trip)

    notifications_collection.insert_one(create_notification(user_id, partial_trips, 1))
    text = 'Booking Confirmation: Enjoy your trip to ' + str(partial_trips[0]['endBusStop'])
    send_notification(token, 'MoNAD', text)
    return 'ok'

def surround_in_quotes(astring):
    return "'%s'" % astring

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
        response = requests.post(url, headers = custom_header, data = json.dumps(message_body))

        if (response.status_code == 200):
            print(response.content)
            print(response.status_code)
        else:
            print("Error with http status_code " + str(response.status_code))
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message

def get_bus_stops():
    bus_stops = list(bus_stop_collection.find())
    return dumps(bus_stops)
