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
from bson.objectid import ObjectId
from pyspark import SparkContext
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
NUMBER_OF_RECOMMENDATIONS = 1
client = MongoClient()
db = client.monad
client2 = MongoClient('130.238.15.114')
db2 = client2.monad1
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
    results = TravelRequest.find()
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
    first = first.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
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
def calculateDistance(tup1):
    current_route = numpy.array(tup1)
    distances = []
    for i in selected_centroids:
        centroid = numpy.array(i)
        distances.append(numpy.linalg.norm(current_route - centroid))
    return distances

'''def calculateDistanceDeparture(tup1):
  distances_departure = []
  for i in selected_centroids:
      centroid_departure = (i[0], i[1],i[4], i[5])
      centroid_departure = numpy.array(centroid_departure)
      temp_dist = []
      for l in range(len(tup1)-1):
        current_stop = numpy.array(tup1[l])
        temp_dist.append(numpy.linalg.norm(current_stop - centroid_departure))
      result = min(temp_dist)
      distances_departure.append(result)
  #print distances_departure
  return distances_departure

  def calculateDistanceArrival(tup1):
  distances_arrival = []
  for i in selected_centroids:
        centroid_arrival = (i[2], i[3], i[6], i[7])
        centroid_arrival = numpy.array(centroid_arrival)
        temp_dist = []
        for l in range(1, len(tup1)):
          current_stop = numpy.array(tup1[l])
          temp_dist.append(numpy.linalg.norm(current_stop - centroid_arrival))
        result = min(temp_dist)
        distances_arrival.append(result)
  return distances_arrival'''
#-------------------------------------------------------------------
def calculateDistanceDeparture(tup1):
    distances_departure = []
    position = -1
    min_value = 1000000000
    min_position = 0
    for i in selected_centroids:
      centroid_departure = (i[0], i[1],i[4], i[5])
      centroid_departure = numpy.array(centroid_departure)
      temp_dist = []
      for l in range(len(tup1)-2):
        current_stop = numpy.array(tup1[l])
        distance = numpy.linalg.norm(current_stop - centroid_departure)
        #temp_dist.append(a)
        position = position + 1
        if (distance < min_value):
            min_value = distance
            min_position = position
      #result = min(temp_dist)
      dontGoBehind = min_position #Need to create a 'dontGoBehind' Global variable
      result = min_value
      distances_departure.append(result)
    return distances_departure

def calculateDistanceArrival(tup1):
  distances_arrival = []
  for i in selected_centroids:
        centroid_arrival = (i[2], i[3], i[6], i[7])
        centroid_arrival = numpy.array(centroid_arrival)
        temp_dist = []
        for l in range(dontGoBehind+1, len(tup1)):
          current_stop = numpy.array(tup1[l])
          temp_dist.append(numpy.linalg.norm(current_stop - centroid_arrival))
        result = min(temp_dist)
        distances_arrival.append(result)
  return distances_arrival

#------------------------------------------------------------------

def removeDuplicates(alist):
    return list(set(map(lambda (x, y): x, alist)))

def recommendationsToReturn(alist):
    result = getTodayTimeTable()
    for res in result:
        for res1 in res['timetable']:
            if res1 in alist: 
                for res2 in db2.BusTrip.find({'_id': res1}):
                    #for res3 in res2['trajectory']:
                        for res4 in db2.BusStop.find({'_id': res2['trajectory'][0]['busStop']}):
                            for res5 in db2.BusStop.find({'_id': res2['trajectory'][len(res2['trajectory'])-1]['busStop']}):
                                to_return.append((res1, res4['name'], res5['name'], res2['trajectory'][0]['time'],
                                                  res2['trajectory'][len(res2['trajectory'])-1]['time'], res2['busID']))
                            
def recommendationsToDB(alist):
    rec_list = []
    for item in alist:
      route_id = item[0]
      start_place = item[1]
      end_place = item[2]
      start_time = item[3]
      end_time = item[4]
      vehicle_no = item[5]
      new_record = {
          "routeID" : route_id,
          "startPlace" : start_place,
          "endPlace" : end_place,
          "startTime" : start_time,
          "endTime" : end_time,
          "vehicleNo" : vehicle_no
      }
      rec_list.append(new_record)
    return rec_list

def insertToDB(user, recs):
    db.TravelRecommendation.delete_many({"userId": user})
    #db2.TravelRecommendation.delete_many({"userId": user})
    o = ObjectId()
    oo = str(o)
    new_record = {
        "_id" : o,
        "recId" : oo,
        "userId" : user,
        "recommendations": recs
    }
    db.TravelRecommendation.insert(new_record)
    #db2.TravelRecommendation.insert(new_record)

def emptyPastRecommendations():
    db.TravelRecommendation.drop()
    #db2.TravelRecommendation.drop()

if __name__ == "__main__":

    userIds = []
    users = []
    routes = []
    userIds = []

    sc = SparkContext()

    #time_t = getTodayTimeTable()
    populateTimeTable()
    myRoutes = sc.parallelize(routes).cache()
    coucou = myRoutes
    
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

    for userId in userIds:
        recommendations = []
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
        selected_centroids = kmeans(optimalk(myRdd), myRdd)[1].centers
        routesDistances = myRoutes.map(lambda x: (x[0], calculateDistanceDeparture(x[1]), calculateDistanceArrival(x[1])))
        for i in range(len(selected_centroids)):
            sortRoute = (routesDistances.map(lambda (x, y, z): (x, y[i] + z[i]))
                                        .map(lambda (x,y): (y,x)).sortByKey()
                                        .map(lambda (x,y): (y,x)))
            finalRecommendation.append(sortRoute.take(NUMBER_OF_RECOMMENDATIONS))
        for sug in finalRecommendation:
            for i in range(len(sug)):
                recommendations.append(sug[i])

        recommendations = removeDuplicates(recommendations)
        recommendationsToReturn(recommendations)
        recs = recommendationsToDB(to_return)
        insertToDB(userId, recs)

       