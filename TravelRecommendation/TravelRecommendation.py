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
from pyspark import SparkContext, SparkConf
from pymongo import MongoClient
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from math import sqrt
from geopy.distance import vincenty

START = datetime.datetime.now()

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
#client2 = MongoClient('130.238.15.114')
client2 = MongoClient()
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
    position_departure = []
    for i in selected_centroids:
        position = -1
        min_value = 1000000000
        min_position = 0
        centroid_departure = (i[0], i[1],i[4], i[5])
        centroid_departure = numpy.array(centroid_departure)
        temp_dist = []
        for l in range(len(tup1)-1):
            current_stop = numpy.array(tup1[l])
            distance = numpy.linalg.norm(current_stop - centroid_departure)
            #temp_dist.append(a)
            position = position + 1
            if (distance < min_value):
                min_value = distance
                min_position = position
                #result = min(temp_dist)
                #dontGoBehind = min_position #Need to create a 'dontGoBehind' Global variable
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
        centroid_arrival = (i[2], i[3], i[6], i[7])
        centroid_arrival = numpy.array(centroid_arrival)
        temp_dist = []
        counter = counter + 1
        position = position_departure[counter]
        for l in range(position_departure[counter]+1, len(tup1)):
            current_stop = numpy.array(tup1[l])
            distance = numpy.linalg.norm(current_stop - centroid_arrival)
            position = position + 1
            if (distance < min_value):
                min_value = distance
                min_position = position
        result = min_value
        distances_arrival.append(result)
        position_arrival.append(min_position)
    return {"distances_arrival":distances_arrival,"position_arrival":position_arrival}

#------------------------------------------------------------------

def removeDuplicates(alist):
    return list(set(map(lambda (w, x, y, z): (w, y, z), alist)))

# Return user trip information
def recommendationsToReturn(alist):
    result = getTodayTimeTable()
    trajectory = []
    to_return1 = []
    for res in result:
        for res1 in res['timetable']:
            if res1 in alist:
                start_index = alist.index(res1)+2
                end_index = alist.index(res1)+3
                for res2 in db2.BusTrip.find({'_id': res1}):
                    for i in range(alist.index(res1)+2, alist.index(res1)+4):
                        trajectory.append(res2['trajectory'][i]['busStop'])
                        #trajectory.append(res3['busStop'])
                    for res4 in db2.BusStop.find({'_id': res2['trajectory'][start_index]['busStop']}):
                        for res5 in db2.BusStop.find({'_id': res2['trajectory'][end_index]['busStop']}):
                            to_return1.append((res2['line'], res2['busID'], res4['name'], res5['name'], res2['trajectory'][start_index]['time'],
                                              res2['trajectory'][end_index]['time'],'null', 'null', 'null', 'null', 'false'))
                    to_return.append((to_return1, trajectory))


# Added user as argument
def recommendationsToDB(user, alist):
    rec_list = []
    for item in alist:
      #route_id not needed anymore in user trip
      #route_id = item[0]
      line = item[0][0][0]
      bus_id = item[0][0][1]
      start_place = item[0][0][2]
      end_place = item[0][0][3]
      start_time = item[0][0][4]
      end_time = item[0][0][5]
      request_time = item[0][0][6]
      feedback = item[0][0][7]
      request_id = item[0][0][8]
      next_trip = item[0][0][9]
      booked = item[0][0][10]
      trajectory = item[1]
      new_record = {
          #"routeID" : route_id,               NOT NEEDED ANYMORE IN USER TRIP.
          "userID" : user,
          "line" : line,
          "busID" : bus_id,
          "startPlace" : start_place,
          "endPlace" : end_place,
          "startTime" : start_time,
          "endTime" : end_time,
          "requestTime" : request_time,
          "feedback" : -1,
          "trajectory" : trajectory,
          "requestID" : request_id,
          #"next" : next_trip,
          "booked" : False
      }
      rec_list.append(new_record)
    return rec_list

# Insertion in User Trip Collection
def insertUserTripToDB(user, recs):
    #db.TravelRecommendation.delete_many({"userId": user})
    #db2.TravelRecommendation.delete_many({"userId": user})
    '''o = ObjectId()
    #oo = str(o),                NOT NEEDED ANYMORE IN TRAVEL RECOMMENDATION.
    new_record = {
        "_id" : o,
        #"recId" : oo,               NOT NEEDED ANYMORE IN TRAVEL RECOMMENDATION.
        "userID" : user,
        "line": recs
    }'''
    usertrip_ids = []
    for i in range(len(recs)):
        object_id = db.UserTrip.insert(recs[i])
        usertrip_ids.append(object_id)
    return usertrip_ids
    #db2.TravelRecommendation.insert(new_record)

# Insertion in Travel Recommendation Collection
def insertTravelRecommendationToDB(user, usertrip_ids):
    db.TravelRecommendation.delete_many({"userId": user})
    #db2.TravelRecommendation.delete_many({"userId": user})
    #o = ObjectId()
    #oo = str(o),                NOT NEEDED ANYMORE IN TRAVEL RECOMMENDATION.
    for i in range(len(usertrip_ids)):
        new_record = {
            "userID" : user,
            "userTrip": usertrip_ids[i]
        }
        db.TravelRecommendation.insert(new_record)


def emptyPastRecommendations():
    db.TravelRecommendation.drop()
    #db2.TravelRecommendation.drop()

if __name__ == "__main__":

userIds = []
users = []
routes = []
userIds = []

conf = SparkConf().setAppName("final_version").setMaster("spark://130.238.15.246:7077")
sc = SparkContext(conf = conf)

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
    print user

for user in userIdsRdd:
    userIds.append(user[0])


emptyPastRecommendations()

    for userId in userIds:
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
selected_centroids = kmeans(3, myRdd)[1].centers
routesDistances = myRoutes.map(lambda x: (x[0], calculateDistanceDeparture(x[1])['distances_departure'],
                                          calculateDistanceArrival(x[1],
                                          calculateDistanceDeparture(x[1])['position_departure'])['distances_arrival'],
                                          calculateDistanceDeparture(x[1])['position_departure'],
                                          calculateDistanceArrival(x[1], calculateDistanceDeparture(x[1])['position_departure'])['position_arrival']))
#coucou = routesDistances
for i in range(len(selected_centroids)):
    sortRoute = (routesDistances.map(lambda (v, w, x, y, z): (v, w[i] + x[i], y[i], z[i]))
                                 .sortBy(lambda x:x[1]))
    finalRecommendation.append(sortRoute.take(NUMBER_OF_RECOMMENDATIONS))
for sug in finalRecommendation:
    for i in range(len(sug)):
        for j in range(len(sug[i])):
            recommendations.append(sug[i][j])

# UNTIL HERE IT WORKS

#recommendations = removeDuplicates(recommendations)
recommendationsToReturn(recommendations)
recs = recommendationsToDB(userId, to_return)
usertrip_ids = insertUserTripToDB(userId, recs)
insertTravelRecommendationToDB(userId, usertrip_ids)


END = datetime.datetime.now()

print (END-START)
