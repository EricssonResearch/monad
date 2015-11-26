from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

import requests
import json

AUTHENTICATION_MODULE_HOST = 'http://130.238.15.114:'
AUTHENTICATION_MODULE_PORT = '9999'

def send_notification_to_authentication(user_id, message_title, message_body):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    url = AUTHENTICATION_MODULE_HOST + AUTHENTICATION_MODULE_PORT + '/send_notification'
    data = {'user_id': user_id, 'message_title': message_title, 'message_body': message_body}
    requests.post(url, headers = headers, data = data)

def create_notification(user_id, partial_trips, icon_id):
    notification = {}
    notification['userID'] = user_id
    trip = user_trips.find_one({'_id': partial_trips[0]})
    line = trip['line']
    start_time = trip['startTime']
    notification['partialTrips'] = partial_trips

    notification['text'] = "Alert: Bus {} is arriving at {}".format(line, 
                            start_time)
    notification['time'] = datetime.datetime.now()
    notification['iconID'] = icon_id
    print notification
    return notification

def main():
    global user
    global mongo_client
    global db
    global bookings_collection
    global notifications_collection
    global user_trips
    mongo_client = MongoClient('130.238.15.114', 27017)
    db = mongo_client.monad1
    bookings_collection = db.BookedTrip
    user_trips = db.UserTrip
    notifications_collection = db.Notifications
    now = datetime.datetime.now()
    for booking in bookings_collection.find({'userID' : 1}):
        list_trips = booking['partialTrips']
        trip = user_trips.find_one({'_id' : list_trips[0]})
        user_id = trip['userID']
        start_time = trip['startTime']
        dif = datetime.timedelta(minutes = 30)
        if start_time - now < dif and start_time > now:
            notification = create_notification(user_id, list_trips, 3)
            try: 
                notifications_collection.insert_one(notification)
            except pymongo.errors.PyMongoError as e:
                print e
                
            send_notification_to_authentication(user_id, 'MoNAD', notification['text'])

if __name__ == '__main__':
    main()