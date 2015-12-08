from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime
import requests
import json
import time

AUTHENTICATION_MODULE_HOST = 'http://130.238.15.114:'
AUTHENTICATION_MODULE_PORT = '9999'

def send_notification_to_authentication(user_id, message_title, message_body):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    url = AUTHENTICATION_MODULE_HOST + AUTHENTICATION_MODULE_PORT + '/send_notification'
    data = {'user_id': user_id, 'message_title': message_title, 'message_body': message_body}
    requests.post(url, headers = headers, data = data)

def parse_user_trip(user_trips_list, user_trip):
    if 'next' in user_trip.keys():
        user_trips_list.append(user_trip)
        return parse_user_trip(user_trips_list,
                               user_trips.find_one({'_id' : ObjectId(user_trip['next'])}))
    else:
        user_trips_list.append(user_trip)
        return user_trips_list
    requests.post(url, headers = headers, data = data)

def create_notification(user_id, partial_trips, icon_id):
    notification = {}
    notification['userID'] = user_id
    trip = user_trips.find_one({'_id': partial_trips[0]})
    line = trip['line']
    start_time = trip['startTime']
    user_trip = user_trips.find_one({'_id' : partial_trips[0]})
    # print user_trip
    user_trips_list = parse_user_trip(list(), user_trip)
    notification['partialTrips'] = user_trips_list
    notification['text'] = "Alert: Bus {} is arriving at {}".format(line,
                            start_time)
    notification['time'] = datetime.datetime.now()
    notification['iconID'] = icon_id
    print notification['userID'] , start_time
    return notification

def main():
    global mongo_client
    mongo_client = MongoClient('130.238.15.114', 27017)
    global db
    db = mongo_client.monad1
    global bookings_collection
    bookings_collection = db.BookedTrip
    global notifications_collection
    notifications_collection = db.Notifications
    global user_trips
    user_trips = db.UserTrip
    
    while True:
        now = datetime.datetime.now()

        for booking in bookings_collection.find({'notified' : False}):
            list_trips = booking['partialTrips']
            trip = user_trips.find_one({'_id' : list_trips[0]})
            user_id = trip['userID']
            start_time = trip['startTime']
            dif = datetime.timedelta(minutes = 30)

            if start_time - now < dif and start_time > now:
                notification = create_notification(user_id, list_trips, 3)
                try:
                    notifications_collection.insert_one(notification)
                    send_notification_to_authentication(user_id, 'MoNAD', notification['text'])
                    bookings_collection.update_one({'_id' : booking['_id']}, {'$set' : {'notified' : True}})
                except pymongo.errors.PyMongoError as e:
                    print e

        time.sleep(60)

if __name__ == '__main__':
    main()
