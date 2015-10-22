import numpy
import math
import datetime
from pyspark import SparkContext
from pymongo import MongoClient
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from math import sqrt

NUM_OF_IT = 8
MIN_LATITUDE = 59.78
MAX_LATITUDE = 59.92
MIN_LONGITUDE = 17.53
MAX_LONGITUDE = 17.75
MIN_COORDINATE = -13750
MAX_COORDINATE = 13750
CIRCLE_CONVERTER = math.pi / 43200
NUMBER_OF_RECOMMENDATIONS = 1
users = []
routes = []
recommendations = []
finalRecommendation = []
selected_centroids = []
routesDistances = []
to_return = []
userId = 123
client = MongoClient()
db = client.monad

def dataBaseConnection():
    # TODO Connect MongoDB with Spark, so we can directly distribute the data
    # we retrieved from Mongo in a RDD
    #client = MongoClient("130.238.15.114",27017)
    TravelRequest = db.TravelRequest
    TimeTable = db.TimeTable
    return TravelRequest, TimeTable

def populateFromDatabase(TravelRequest, TimeTable):
    results = TravelRequest.find()
    for res in results:
        #if res['start_time'] == "":
            #res['start_time'] = datetime.datetime.utcnow()
            #st_weight = 0
        users.append((res['start_position_lat'], res['start_position_lon'],
        res['end_position_lat'], res['end_position_lon'],
        (res['start_time']).time(), (res['end_time']).time()))
    route = TimeTable.find()
    for res in route:
        for i in range(len(res['Waypoints']) - 1):
            for j in range(i+1,len(res['Waypoints'])):
                routes.append([res['_id'], (res['Waypoints'][i]['latitude'],
                res['Waypoints'][i]['longitude'],
                res['Waypoints'][j]['latitude'],
                res['Waypoints'][j]['longitude'],
                res['Waypoints'][i]['DptTime'],
                res['Waypoints'][j]['DptTime'])])

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
def kmeans(iterations):
    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x**2 for x in (point - center)]))
    clusters = KMeans.train(myRdd, iterations, maxIterations=10,
            runs=10, initializationMode="random")
    WSSSE = myRdd.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    return WSSSE, clusters

# Function that runs iteratively the kmeans algorithm to find the best number
# of clusters to group the user's request
def optimalk():
    results = []
    for i in range(NUM_OF_IT):
        results.append(kmeans(i+1)[0])
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

def removeDuplicates(alist):
    return list(set(map(lambda x: x[0], alist)))

def recommendationsToReturn(alist):
    for sug in alist:
        to_return.append( time_t.find_one({"_id": sug},
                                 {"StartBusstop":1, "EndBusstop":1,
                                  "StartTime":1, "EndTime":1, "VehicleID":1}))

def recommendationsToDB(alist):
    rec_list = []
    for item in alist:
        route_id = item['_id']
        start_place = item['StartBusstop']
        end_place = item['EndBusstop']
        start_time = item['StartTime']
        end_time = item['EndTime']
        vehicle_no = item['VehicleID']
        new_record = {
            "routeId" : route_id,
            "startPlace" : start_place,
            "endPlace" : end_place,
            "startTime" : start_time,
            "endTime" : end_time,
            "vehicleNo" : vehicle_no
        }
        rec_list.append(new_record)
    return rec_list

def insertToDB(user, recs):
    new_record = {
        "userId" : user,
        "recommendations": recs
    }
    db.TravelRecommendation.insert(new_record)

if __name__ == "__main__":
    sc = SparkContext()
    req, time_t = dataBaseConnection()
    populateFromDatabase(req, time_t)

    myRdd = sc.parallelize(users).cache()
    myRoutes = sc.parallelize(routes).cache()

    myRdd = (myRdd.map(lambda x: (x[0], x[1], x[2], x[3],
                                 toCoordinates(toSeconds(x[4])),
                                 toCoordinates(toSeconds(x[5]))))
                  .map(lambda (x1, x2, x3, x4, (x5, x6), (x7, x8)):
                                (latNormalizer(x1), lonNormalizer(x2),
                                 latNormalizer(x3), lonNormalizer(x4),
                                 timeNormalizer(x5), timeNormalizer(x6),
                                 timeNormalizer(x7), timeNormalizer(x8))))

    myRoutes = (myRoutes.map(lambda (y,x): (y, (x[0], x[1], x[2], x[3],
                                 toCoordinates(toSeconds(x[4])),
                                 toCoordinates(toSeconds(x[5])))))
                       .map(lambda (y, (x1, x2, x3, x4, (x5, x6), (x7, x8))):
                                 (y, (latNormalizer(x1), lonNormalizer(x2),
                                 latNormalizer(x3), lonNormalizer(x4),
                                 timeNormalizer(x5),timeNormalizer(x6),
                                 timeNormalizer(x7),timeNormalizer(x8)))))

    selected_centroids = kmeans(optimalk())[1].centers
    routesDistances = myRoutes.map(lambda x: (x[0], calculateDistance(x[1])))

    for i in range(len(selected_centroids)):
        sortRoute = (routesDistances.map(lambda (x, y): (x, y[i]))
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
