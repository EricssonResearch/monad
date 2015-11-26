from pymongo import MongoClient
import math
import datetime
import csv

def define_user_info(user):
    global userId 
    global user_longitude 
    global user_latitude 
    global time
    userId = user[0]
    user_longitude = float(user[1])
    user_latitude = float(user[2])
    time = datetime.datetime.now()

def check_geofences():
    global geofence_threshold 
    geofence_threshold = 0.006
    cursor = bus_stop_collection.find()

    for bus_stop in cursor:
        stop_longitude = bus_stop['longitude']
        stop_latitude = bus_stop['latitude']
        distance = math.sqrt((user_longitude - stop_longitude) ** 2 +
                             (user_latitude - stop_latitude) ** 2)
        if distance < geofence_threshold:
            return 1
    return 0

def main():
    global mongo_client
    global db
    global bookings_collection
    global bus_stop_collection
    mongo_client = MongoClient('130.238.15.114', 27017)
    db = mongo_client.monad1
    bookings_collection = db.BookedTrip
    bus_stop_collection = db.BusStop
    reader = csv.reader(open('passengers.csv', 'rb'))
    writer = csv.writer(open('results.csv','wb'))
    for row in reader :
        define_user_info(row)
        user_in_geofence = check_geofences()
        if user_in_geofence: 
            writer.writerow([userId, user_longitude, user_latitude, time])

if __name__ == '__main__':
    main()