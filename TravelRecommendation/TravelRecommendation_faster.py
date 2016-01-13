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

import numpy
import math
import datetime
import requests
import json
import re
from operator import itemgetter
from bson.objectid import ObjectId
from pyspark import SparkContext, SparkConf
from pymongo import MongoClient
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from math import sqrt
from geopy.distance import vincenty

# Weights
W_1 = 1.2
W_2 = .8
DISTANCE_THRESHOLD = 0.3
NUM_OF_IT = 8
MIN_LATITUDE = 59.78
MAX_LATITUDE = 59.92
MIN_LONGITUDE = 17.53
MAX_LONGITUDE = 17.75
MIN_COORDINATE = -13750
MAX_COORDINATE = 13750
CIRCLE_CONVERTER = math.pi / 43200
NUMBER_OF_RECOMMENDATIONS = 5
client2 = MongoClient('130.238.15.114')
db2 = client2.monad1
client3 = MongoClient('130.238.15.114')
db3 = client3.monad1
start = datetime.datetime.now()
dontGoBehind = 0

def time_approximation(lat1, lon1, lat2, lon2):
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    distance = vincenty(point1, point2).kilometers
    return int(round(distance / 10 * 60))

def retrieve_requests():
    TravelRequest = db2.TravelRequest
    return TravelRequest

def populate_requests(TravelRequest):
    results = db2.TravelRequest.find()
    for res in results:
        dist = time_approximation(res['startPositionLatitude'],
                                 res['startPositionLongitude'],
                                 res['endPositionLatitude'],
                                 res['endPositionLongitude'])
        if res['startTime'] == "null":
            users.append((res['userID'],(res['startPositionLatitude'],
            res['startPositionLongitude'], res['endPositionLatitude'],
            res['endPositionLongitude'],
            (res['endTime'] - datetime.timedelta(minutes = dist)).time(),
            (res['endTime']).time())))
        elif res['endTime'] == "null":
            users.append((res['userID'],(res['startPositionLatitude'],
            res['startPositionLongitude'], res['endPositionLatitude'],
            res['endPositionLongitude'], (res['startTime']).time(),
            (res['startTime'] + datetime.timedelta(minutes = dist)).time())))
        else:
            users.append((res['userID'],(res['startPositionLatitude'],
            res['startPositionLongitude'], res['endPositionLatitude'],
            res['endPositionLongitude'], (res['startTime']).time(),
            (res['endTime']).time())))

def get_today_timetable():
    TimeTable = db2.TimeTable
    first = datetime.datetime.today()
    first = first.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    route = TimeTable.find({'date': {'$gte': first}})
    return route

def populate_timetable():
    route = get_today_timetable()
    waypoints = []
    for res in route:
        for res1 in res['timetable']:
            for res2 in db2.BusTrip.find({'_id': res1}):
                for res3 in res2['trajectory']:
                    for res4 in db2.BusStop.find({'_id':res3['busStop']}):
                        waypoints.append((res3['time'],res4['latitude'],
                                          res4['longitude'], res4['name']))
                routes.append((res1, waypoints))
                waypoints = []

def iterator(waypoints):
    Waypoints = []
    for res in waypoints:
        Waypoints.append((lat_normalizer(res[1]), lon_normalizer(res[2]),
                        time_normalizer(to_coordinates(to_seconds(res[0]))[0]),
                        time_normalizer(to_coordinates(to_seconds(res[0]))[1]),
                        res[3]))
    return Waypoints

# Converting time object to seconds
def to_seconds(dt):
    total_time = dt.hour * 3600 + dt.minute * 60 + dt.second
    return total_time

# Mapping seconds value to (x, y) coordinates
def to_coordinates(secs):
    angle = float(secs) * CIRCLE_CONVERTER
    x = 13750 * math.cos(angle)
    y = 13750 * math.sin(angle)
    return x, y

# Normalization functions
def time_normalizer(value):
    new_value = float((float(value) - MIN_COORDINATE) /
                      (MAX_COORDINATE - MIN_COORDINATE))
    return new_value /2

def lat_normalizer(value):
    new_value = float((float(value) - MIN_LATITUDE) /
                      (MAX_LATITUDE - MIN_LATITUDE))
    return new_value

def lon_normalizer(value):
    new_value = float((float(value) - MIN_LONGITUDE) /
                      (MAX_LONGITUDE - MIN_LONGITUDE))
    return new_value

# Function that implements the kmeans algorithm to group users requests
def kmeans(iterations, theRdd):
    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x**2 for x in (point - center)]))
    clusters = KMeans.train(theRdd, iterations, maxIterations=10,
            runs=10, initializationMode="random")
    WSSSE = theRdd.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    return WSSSE, clusters

# Function that runs iteratively the kmeans algorithm to find the best number
# of clusters to group the user's request
def optimalk(theRdd):
    results = []
    for i in range(NUM_OF_IT):
        results.append(kmeans(i+1, theRdd)[0])
    optimal = []
    for i in range(NUM_OF_IT-1):
        optimal.append(results[i] - results[i+1])
    optimal1 = []
    for i in range(NUM_OF_IT-2):
        optimal1.append(optimal[i] - optimal[i+1])
    return (optimal1.index(max(optimal1)) + 2)

def back_to_coordinates(lat, lon):
    new_lat = (lat * (MAX_LATITUDE - MIN_LATITUDE)) + MIN_LATITUDE
    new_lon = (lon * (MAX_LONGITUDE - MIN_LONGITUDE)) + MIN_LONGITUDE
    return new_lat, new_lon

def nearest_stops(lat, lon, dist):
    stops = []
    url = "http://130.238.15.114:9998/get_nearest_stops_from_coordinates"
    data = {'lon': lon, 'lat': lat, 'distance': dist}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    answer = requests.post(url, data = data, headers = headers)
    p = re.compile("(u'\w*')")
    answer = p.findall(answer.text)
    answer = [x.encode('UTF8') for x in answer]
    answer = [x[2:-1] for x in answer]
    answer = list(set(answer))
    return answer

# The function that calculate the distance from the given tuple to all the
# cluster centroids and returns the minimum disstance
def calculate_distance_departure(tup1):
    dist_departure = []
    pos_departure = []
    cent_num = 0
    for i in selected_centroids:
        position = -1
        min_value = 1000
        min_position = 0
        centroid_departure = (i[0]*W_1, i[1]*W_1,i[4]*W_2, i[5]*W_2)
        centroid_departure = numpy.array(centroid_departure)
        trajectory = []
        for l in range(len(tup1)-1):
            position = position + 1
            if(tup1[l][4] in nearest_stops_dep[cent_num]):
                current_stop = (numpy.array(tup1[l][:4])
                                * numpy.array((W_1,W_1,W_2,W_2)))
                distance = numpy.linalg.norm(centroid_departure - current_stop)
                if (distance < min_value):
                    min_value = distance
                    min_position = position
        result = min_value
        dist_departure.append(result)
        pos_departure.append(min_position)
        cent_num += 1
    return {"dist_departure":dist_departure,"pos_departure":pos_departure}

def calculate_distance_arrival(tup1,pos_departure):
    dist_arrival = []
    pos_arrival = []
    counter=-1
    cent_num = 0
    for i in selected_centroids:
        min_value = 1000
        min_position = 0
        centroid_arrival = (i[2]*W_1, i[3]*W_1, i[6]*W_2, i[7]*W_2)
        centroid_arrival = numpy.array(centroid_arrival)
        counter = counter + 1
        position = pos_departure[counter]
        for l in range(pos_departure[counter]+1, len(tup1)):
            position = position + 1
            if(tup1[l][4] in nearest_stops_arr[cent_num]):
                current_stop = (numpy.array(tup1[l][:4])
                                * numpy.array((W_1,W_1,W_2,W_2)))
                distance = numpy.linalg.norm(centroid_arrival - current_stop)
                if (distance < min_value):
                    min_value = distance
                    min_position = position
        result = min_value
        dist_arrival.append(result)
        pos_arrival.append(min_position)
        cent_num += 1
    return {"dist_arrival":dist_arrival,"pos_arrival":pos_arrival}

def remove_duplicates(alist):
    return list(set(map(lambda (w, x, y, z): (w, y, z), alist)))

def recommendations_to_return(alist):
    for rec in alist:
        trip = db2.BusTrip.find_one({'_id': rec[0]})
        traj = trip['trajectory'][rec[2]:rec[3]+1]
        trajectory = []
        names_only = []
        for stop in traj:
            name_and_time = (db2.BusStop.find_one({"_id": stop['busStop']})
                                                  ['name']), stop['time']
            trajectory.append(name_and_time)
            names_only.append(name_and_time[0])
        busid = 1.0
        line = trip['line']
        result = (int(line), int(busid), names_only[0], names_only[-1],
                  names_only, trajectory[0][1], trajectory[-1][1], rec[0])
        to_return.append(result)

def recommendations_to_db(user, alist):
    rec_list = []
    for item in to_return:
        o_id = ObjectId()
        line = item[0]
        bus_id = item[1]
        start_place = item[2]
        end_place = item[3]
        start_time = item[5]
        end_time = item[6]
        bus_trip_id = item[7]
        request_time = "null"
        feedback = -1
        request_id = "null"
        next_trip = "null"
        booked = False
        trajectory = item[4]
        new_user_trip = {
          "_id":o_id,
          "userID" : user,
          "line" : line,
          "busID" : bus_id,
          "startBusStop" : start_place,
          "endBusStop" : end_place,
          "startTime" : start_time,
          "busTripID" : bus_trip_id,
          "endTime" : end_time,
          "feedback" : feedback,
          "trajectory" : trajectory,
          "booked" : booked
        }
        new_recommendation = {
        "userID": user,
        "userTrip": o_id
        }
        db3.UserTrip.insert(new_user_trip)
        db3.TravelRecommendation.insert(new_recommendation)

def empty_past_recommendations():
    db3.TravelRecommendation.drop()

if __name__ == "__main__":

    user_ids = []
    users = []
    routes = []
    user_ids = []

    sc = SparkContext()
    populate_timetable()
    my_routes = sc.parallelize(routes, 8)

    my_routes = my_routes.map(lambda (x,y): (x, iterator(y))).cache()

    req = retrieve_requests()
    populate_requests(req)

    start = datetime.datetime.now()

    initial_rdd = sc.parallelize(users, 4).cache()
    user_ids_rdd = (initial_rdd.map(lambda (x,y): (x,1))
                            .reduceByKey(lambda a, b: a + b)
                            .collect())
    '''
    for user in user_ids_rdd:
        user_ids.append(user[0])
    '''
    empty_past_recommendations()

    user_ids = []
    user_ids.append(1)

    for userId in user_ids:
        userId = 1
        recommendations = []
        transition = []
        final_recommendation = []
        selected_centroids = []
        routes_distances = []
        to_return = []
        nearest_stops_dep = []
        nearest_stops_arr = []

        my_rdd = (initial_rdd.filter(lambda (x,y): x == userId)
                           .map(lambda (x,y): y)).cache()
        my_rdd = (my_rdd.map(lambda x: (x[0], x[1], x[2], x[3],
                                     to_coordinates(to_seconds(x[4])),
                                     to_coordinates(to_seconds(x[5]))))
                      .map(lambda (x1, x2, x3, x4, (x5, x6), (x7, x8)):
                                    (lat_normalizer(x1), lon_normalizer(x2),
                                     lat_normalizer(x3), lon_normalizer(x4),
                                     time_normalizer(x5), time_normalizer(x6),
                                     time_normalizer(x7), time_normalizer(x8))))

        selected_centroids = kmeans(4, my_rdd)[1].centers

        for i in range(len(selected_centroids)):
            cent_lat, cent_long = back_to_coordinates(selected_centroids[i][0],
                                                    selected_centroids[i][1])
            nearest_stops_dep.append(nearest_stops(cent_lat, cent_long, 200))
            cent_lat, cent_long = back_to_coordinates(selected_centroids[i][2],
                                                    selected_centroids[i][3])
            nearest_stops_arr.append(nearest_stops(cent_lat, cent_long, 200))

        routes_distances = my_routes.map(lambda x: (x[0],
        calculate_distance_departure(x[1])['dist_departure'],
        calculate_distance_arrival(x[1],
        calculate_distance_departure(x[1])['pos_departure'])['dist_arrival'],
        calculate_distance_departure(x[1])['pos_departure'],
        calculate_distance_arrival(x[1],
        calculate_distance_departure(x[1])['pos_departure'])['pos_arrival']))

        for i in range(len(selected_centroids)):
            sort_route = (routes_distances.map(lambda (v, w, x, y, z):
                                                (v, w[i] + x[i], y[i], z[i]))
                                         .sortBy(lambda x:x[1]))
            final_recommendation.append((sort_route
                                        .take(NUMBER_OF_RECOMMENDATIONS)))

        for sug in final_recommendation:
            for i in range(len(sug)):
                temp = []
                for j in range(len(sug[i])):
                    temp.append(sug[i][j])
                recommendations.append(temp)

        recommendations.sort(key=lambda x: x[1])
        recommendations_final = []
        for rec in recommendations:
            if abs(rec[2] - rec[3]) > 1 and rec[1] < DISTANCE_THRESHOLD:
                recommendations_final.append(rec)

        recommendations = recommendations_final[:10]
        recommendations_to_return(recommendations)
        recommendations_to_db(userId, to_return)
