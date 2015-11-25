from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

def start(host):
    global mongo_client
    global db
    global bus_trip_collection
    global bus_stop_collection
    
    mongo_client = MongoClient(host, 27017)
    db = mongo_client.monad1
    bus_trip_collection = db.BusTrip
    bus_stop_collection = db.BusStop

def vehicle_get_next_trip(bus_id):
    trips = list(bus_trip_collection.find({'busID' : bus_id}))
    now = datetime.datetime.now()# - datetime.timedelta(days = 1)

    min = datetime.timedelta(weeks = 1)

    for trip in trips:
        if now < trip['startTime']:

            if trip['startTime'] - now < min:
                min = trip['startTime'] - now
                nearest_trip = trip

    # print min
    # print nearest_trip['startTime']

    if nearest_trip is None:
        return -1

    trajectory = nearest_trip['trajectory']

    # print trajectory[0]['busStop']
    # print bus_stop_collection.find_one({'_id' : ObjectId(trajectory[0]['busStop'])})

    for trajectory_point in trajectory:
        trajectory_point['busStop']= bus_stop_collection.find_one({'_id' : ObjectId(trajectory_point['busStop'])})

    # print nearest_trip['trajectory']

    return dumps(nearest_trip)

# if __name__ == "__main__":
#     start("130.238.15.114")
#     get_current_bus_trip(1)
