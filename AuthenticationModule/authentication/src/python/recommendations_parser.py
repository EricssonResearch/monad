from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

def start(host):
    global mongo_client
    global db
    global recommendations_collection
    global user_trips_collection
    global bus_stop_collection
    mongo_client = MongoClient(host, 27017)
    db = mongo_client.monad1
    recommendations_collection = db.TravelRecommendation
    user_trips_collection = db.UserTrip
    bus_stops_collection = db.BusStop

def parse_recommendations(user_id):
    print user_id
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
