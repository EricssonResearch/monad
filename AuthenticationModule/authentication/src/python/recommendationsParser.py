# from pymongo import MongoClient
# from bson.json_util import dumps
#
# client = MongoClient("localhost", 27017)
# db = client.monad
# rec_collection = db.TravelRecommendation
# ut_collection = db.UserTrip
# bs_collection = db.BusStop
#
# def parse(user_id):
#     recommendations = list(rec_collection.find({"userId" : user_id}))
#     recommendation_list = list()
#     for recommendation in recommendations:
#         user_trip_ref = recommendation['userTrip']
#         user_trip = ut_collection.find({"_id" : user_trip_ref})
#         user_trips = list()
#         user_trips = parseUserTrip(user_trip, user_trips)
#         recommendation['userTrip'] = user_trips
#         recommendation_list.append(recommendation)
#
#     return dumps(recommendation_list)
#
# def parseUserTrip(user_trip, user_trip):
#     start_bus_stop_ref = user_trip['startBusStop']
#     start_bus_stop_info = bs_collection.find({"_id" : start_bus_stop_ref})
#     user_trip['startBusStop'] = start_bus_stop_info['name']
#
#     end_bus_stop_ref = user_trip.get['endBusStop']
#     end_bus_stop_info = bs_collection.find({"_id" : end_bus_stop_ref})
#     user_trip_results['endBusStop'] = end_bus_stop_info['name']
#
#     trajectory_refs = user_trip['trajectory']
#     trajectory = list()
#     for bus_stop_ref in trajectory_refs:
#         bus_stop_info = list(bs_collection.find({"_id" : bus_stop_ref}))
#         trajectory.append(bus_stop_info['name'])
#     user_trip['trajectory'] = trajectory
#     user_trips.append(user_trip)
#     next_ref = user_trip['next']
#
#     if next_ref != "null":
#         return user_trips
#     else:
#         return parseUserTrip(next_ref)
#
# # def test():
# #     results = collection.find()
# #     L = list(results)
# #     file = open('test.json', 'w')
# #     file.write(dumps(L))
# #     file.close()
#
# # if __name__ == '__main__':
# #     parse(1003634)
#     # test()
