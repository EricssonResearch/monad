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
from operator import itemgetter
from bson.objectid import ObjectId
from pyspark import SparkContext, SparkConf
from pymongo import MongoClient
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from math import sqrt
from geopy.distance import vincenty

NUM_OF_IT = 8
MIN_LATITUDE = 59.78
MAX_LATITUDE = 59.92
MIN_LONGITUDE = 17.53
MAX_LONGITUDE = 17.75
MIN_COORDINATE = -13750
MAX_COORDINATE = 13750
CIRCLE_CONVERTER = math.pi / 43200
NUMBER_OF_RECOMMENDATIONS = 2
#client2 = MongoClient('130.238.15.114')
client2 = MongoClient('130.238.15.114')
#client2 = MongoClient()
db2 = client2.monad1
client3 = MongoClient('130.238.15.114')
client3 = MongoClient()
db3 = client3.monad1
start = datetime.datetime.now()
dontGoBehind = 0

def timeApproximation(lat1, lon1, lat2, lon2):
    point1 = (lat1, lon1)
    point2 = (lat2, lon2)
    distance = vincenty(point1, point2).kilometers
    return int(round(distance / 10 * 60))

def retrieveRequests():
    TravelRequest = db2.TravelRequest
    return TravelRequest

def populateRequests(TravelRequest):
    results = db2.TravelRequest.find()
    for res in results:
        dist = timeApproximation(res['startPositionLatitude'],
                                 res['startPositionLongitude'],
                                 res['endPositionLatitude'],
                                 res['endPositionLongitude'])
        if res['startTime'] == "null":
            users.append((res['userID'],(res['startPositionLatitude'], res['startPositionLongitude'],
            res['endPositionLatitude'], res['endPositionLongitude'],
            (res['endTime'] - datetime.timedelta(minutes = dist)).time(),
            (res['endTime']).time())))
        elif res['endTime'] == "null":
            users.append((res['userID'],(res['startPositionLatitude'], res['startPositionLongitude'],
            res['endPositionLatitude'], res['endPositionLongitude'],
            (res['startTime']).time(),
            (res['startTime'] + datetime.timedelta(minutes = dist)).time())))
        else:
            users.append((res['userID'],(res['startPositionLatitude'], res['startPositionLongitude'],
            res['endPositionLatitude'], res['endPositionLongitude'],
            (res['startTime']).time(),
            (res['endTime']).time())))

def getTodayTimeTable():
    TimeTable = db2.TimeTable
    first = datetime.datetime.today()
    first = first.replace(day = 10, hour = 0, minute = 0, second = 0, microsecond = 0)
    route = TimeTable.find({'date': {'$gte': first}})
    return route

def populateTimeTable():
    route = getTodayTimeTable()
    waypoints = []
    for res in route:
        for res1 in res['timetable']:
            for res2 in db2.BusTrip.find({'_id': res1}):
                for res3 in res2['trajectory']:
                    for res4 in db2.BusStop.find({'_id':res3['busStop']}):
                        waypoints.append((res3['time'],res4['latitude'],res4['longitude']))
                routes.append((res1, waypoints))
                waypoints = []

def iterator(waypoints):
  Waypoints = []
  for res in waypoints:
    Waypoints.append((latNormalizer(res[1]), lonNormalizer(res[2]), timeNormalizer(toCoordinates(toSeconds(res[0]))[0]), timeNormalizer(toCoordinates(toSeconds(res[0]))[1])))
  #print Waypoints
  return Waypoints

# Converting time object to seconds
def toSeconds(dt):
    total_time = dt.hour * 3600 + dt.minute * 60 + dt.second
    return total_time

# Mapping seconds value to (x, y) coordinates
def toCoordinates(secs):
    angle = float(secs) * CIRCLE_CONVERTER
    x = 13750 * math.cos(angle)
    y = 13750 * math.sin(angle)
    return x, y

# Normalization functions
def timeNormalizer(value):
    new_value = float((float(value) - MIN_COORDINATE) /
                      (MAX_COORDINATE - MIN_COORDINATE))
    return new_value /2

def latNormalizer(value):
    new_value = float((float(value) - MIN_LATITUDE) /
                      (MAX_LATITUDE - MIN_LATITUDE))
    return new_value

def lonNormalizer(value):
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

# The function that calculate the distance from the given tuple to all the
# cluster centroids and returns the minimum disstance
def calculateDistanceDeparture(tup1):
    distances_departure = []
    position_departure = []
    for i in selected_centroids:
        position = -1
        min_value = 1000000000
        min_position = 0
        centroid_departure = (i[0]*1.2, i[1]*1.2,i[4]*.8, i[5]*.8)
        centroid_departure = numpy.array(centroid_departure)
        temp_dist = []
        for l in range(len(tup1)-1):
            current_stop = numpy.array(tup1[l]) * numpy.array((1.2,1.2,.8,.8))
            distance = numpy.linalg.norm(centroid_departure - current_stop)
            position = position + 1
            if (distance < min_value):
                min_value = distance
                min_position = position
        result = min_value
        distances_departure.append(result)
        position_departure.append(min_position)
    return {"distances_departure":distances_departure,"position_departure":position_departure}

def calculateDistanceArrival(tup1,position_departure):
    distances_arrival = []
    position_arrival = []
    counter=-1
    for i in selected_centroids:
        min_value = 1000
        min_position = 0
        centroid_arrival = (i[2]*1.2, i[3]*1.2, i[6]*0.8, i[7]*0.8)
        centroid_arrival = numpy.array(centroid_arrival)
        temp_dist = []
        counter = counter + 1
        position = position_departure[counter]
        for l in range(position_departure[counter]+1, len(tup1)):
            current_stop = numpy.array(tup1[l]) * numpy.array((1.2,1.2,.8,.8))
            distance = numpy.linalg.norm(centroid_arrival - current_stop)
            position = position + 1
            if (distance < min_value):
                min_value = distance
                min_position = position
        result = min_value
        distances_arrival.append(result)
        position_arrival.append(min_position)
    return {"distances_arrival":distances_arrival,"position_arrival":position_arrival}

def removeDuplicates(alist):
    return list(set(map(lambda (w, x, y, z): (w, y, z), alist)))

def recommendationsToReturn(alist):
    for rec in alist:
        trip = db2.BusTrip.find_one({'_id': rec[0]})
        traj = trip['trajectory'][rec[2]:rec[3]+1]
        trajectory = []
        for stop in traj:
            name_and_time = db2.BusStop.find_one({"_id": stop['busStop']})['name'], stop['time']
            trajectory.append(name_and_time)
        busid = 1.0
        line = trip['line']
        result = (int(line), int(busid), trajectory[0][0], trajectory[-1][0], trajectory)
        to_return.append(result)
'''
rec = [ObjectId('5644682daa47f84111bd68fd'), 0.016041332059576831, 7, 17]
rec = [ObjectId('5644682caa47f84111bd68dc'), 0.018165826645569837, 7, 17]
rec = [ObjectId('5644682caa47f84111bd68d8'), 0.020546534066310275, 7, 17]
rec = [ObjectId('5644682daa47f84111bd6907'), 0.022553008925461027, 7, 17]
rec = [ObjectId('5644a1f0351b6b2ed5fc6e77'), 0.16710056328081246, 15, 22]
rec = [ObjectId('5645f7d755915436044f8f70'), 0.16719833039535051, 15, 22]


trip = db2.BusTrip.find_one({'_id': rec[0]})
busid = trip['busID']
print busid
'''
# Added user as argument
def recommendationsToDB(user, alist):
    rec_list = []
    for item in alist:
      #route_id not needed anymore in user trip
      #route_id = item[0]
      o_id = ObjectId()
      line = item[0]
      bus_id = item[1]
      start_place = item[2]
      end_place = item[3]
      start_time = item[4][0][1]
      end_time = item[4][-1][1]
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
          "startPlace" : start_place,
          "endPlace" : end_place,
          "startTime" : start_time,
          "endTime" : end_time,
          "feedback" : feedback,
          "trajectory" : trajectory,
          "booked" : booked
      }
      new_recommendation = {
      "userID": user,
      "userTrip": o_id
      }
      db3.UserTripFromRecommendation.insert(new_user_trip)
      db3.TravelRecommendationFromRecommendation.insert(new_recommendation)

def emptyPastRecommendations():
    db3.UserTripFromRecommendation.drop()
    db3.TravelRecommendationFromRecommendation.drop()
    #db2.TravelRecommendation.drop()

if __name__ == "__main__":

    userIds = []
    users = []
    routes = []
    userIds = []

    #conf = SparkConf().setAppName("final_version").setMaster("spark://130.238.15.246:7077")
    #sc = SparkContext(conf = conf)
    sc = SparkContext()
    #time_t = getTodayTimeTable()
    populateTimeTable()
    myRoutes = sc.parallelize(routes).cache()

    myRoutes = myRoutes.map(lambda (x,y): (x, iterator(y)))

    req = retrieveRequests()
    populateRequests(req)
    initialRdd = sc.parallelize(users).cache()
    userIdsRdd = (initialRdd.map(lambda (x,y): (x,1))
                            .reduceByKey(lambda a, b: a + b)
                            .collect())

    for user in userIdsRdd:
        userIds.append(user[0])

    emptyPastRecommendations()

    #for userId in userIds:
    userId = 1
    recommendations = []
    transition = []
    finalRecommendation = []
    selected_centroids = []
    routesDistances = []
    to_return = []
    myRdd = initialRdd.filter(lambda (x,y): x == userId).map(lambda (x,y): y)
    myRdd = (myRdd.map(lambda x: (x[0], x[1], x[2], x[3],
                                 toCoordinates(toSeconds(x[4])),
                                 toCoordinates(toSeconds(x[5]))))
                  .map(lambda (x1, x2, x3, x4, (x5, x6), (x7, x8)):
                                (latNormalizer(x1), lonNormalizer(x2),
                                 latNormalizer(x3), lonNormalizer(x4),
                                 timeNormalizer(x5), timeNormalizer(x6),
                                 timeNormalizer(x7), timeNormalizer(x8))))

    selected_centroids = kmeans(5, myRdd)[1].centers

    routesDistances = myRoutes.map(lambda x: (x[0], calculateDistanceDeparture(x[1])['distances_departure'],
                                              calculateDistanceArrival(x[1], calculateDistanceDeparture(x[1])['position_departure'])['distances_arrival'],
                                              calculateDistanceDeparture(x[1])['position_departure'],
                                              calculateDistanceArrival(x[1], calculateDistanceDeparture(x[1])['position_departure'])['position_arrival']))

    for i in range(len(selected_centroids)):
        sortRoute = (routesDistances.map(lambda (v, w, x, y, z): (v, w[i] + x[i], y[i], z[i]))
                                     .sortBy(lambda x:x[1]))
        finalRecommendation.append(sortRoute.take(NUMBER_OF_RECOMMENDATIONS))

    for sug in finalRecommendation:
        for i in range(len(sug)):
            temp = []
            for j in range(len(sug[i])):
                temp.append(sug[i][j])
            recommendations.append(temp)

    recommendations.sort(key=lambda x: x[1])
    recommendations_final = []
    for rec in recommendations:
        if abs(rec[2] - rec[3]) > 3 and rec[1] < 0.3:
            recommendations_final.append(rec)

    recommendations = recommendations_final[:10]

    # UNTIL HERE IT WORKS
    #recommendations = removeDuplicates(recommendations)
    recommendationsToReturn(recommendations)
    recommendationsToDB(userId, to_return)
        #usertrip_ids = insertUserTripToDB(userId, recs)
        #insertTravelRecommendationToDB(userId, usertrip_ids)
