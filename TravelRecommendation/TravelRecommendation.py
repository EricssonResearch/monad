import numpy
from pyspark import SparkContext
from pymongo import MongoClient
from pyspark.mllib.clustering import KMeans, KMeansModel
from numpy import array
from math import sqrt

# Initializing connection with MongoDB
client = MongoClient()

db = client.monad

TravelRequest = db.TravelRequest
TimeTable = db.TimeTable

#sc = SparkContext()

# TODO Specify the user we want to look for
results = TravelRequest.find()

users = []

# Number of iterations to find the best k
NUM_OF_IT = 8
MIN_LATITUDE = 59.78
MAX_LATITUDE = 59.92
MIN_LONGITUDE = 17.53
MAX_LONGITUDE = 17.75
MIN_TIME = 0
MAX_TIME = 43200

# Creates a list with the data retrieved from MongoDB for the selected user
for res in results:
    users.append((res['start_position_lat'], res['start_position_lon'],
    res['end_position_lat'], res['end_position_lon'])) #(res['start_time']).time(),
    #(res['end_time']).time())

# TODO Connect MongoDB with Spark, so we can directly distribute the data
# we retrieved from Mongo in a RDD

# Creating the RDD based ot the data retrieved from MongoDB

myRdd = sc.parallelize(users).cache()

'''
mapRdd = myRdd.map(lambda x: (x, 1))
counts = mapRdd.reduceByKey(lambda a, b: a + b)
frequent = counts.filter(lambda (a, b): b > 3)
#frequent.collect()
'''

# Function that implements the kmeans algorithm to group users requests
def kmeans(NUM_OF_IT):
    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x**2 for x in (point - center)]))
    clusters = KMeans.train(myRdd, NUM_OF_IT, maxIterations=10,
            runs=10, initializationMode="random")
    WSSSE = myRdd.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    return WSSSE, clusters

# Function that runs iteratively the kmeans algorithm to find the best number
# of clusters to group the user's request
def optimalk(results, NUM_OF_IT):
    results = []
    for i in range(NUM_OF_IT):
        results.append(kmeans(i+2)[0])
    optimal = []
    for i in range(NUM_OF_IT-1):
        optimal.append(results[i] - results[i+1])
    return (optimal.index(max(optimal)) + 3)

# Printing the clusters
# TODO Maybe we need an RDD for that
selected_centroids = kmeans(optimalk(results, NUM_OF_IT))[1].centers

# TODO Retrieves the whole timetable as desired. However has to be done
# directly from MongoDB
route = TimeTable.find()

routes = []

# Creation of route tuples of type (ID,(start, end))
for res in route:
    routes.append([res['_id'], (res['start_position_lat'],
    res['start_position_lon'],  res['end_position_lat'],
    res['end_position_lon'])])

myRoutes = sc.parallelize(routes).cache()

# The function that calculate the distance from the given tuple to all the
# cluster centroids and returns the minimum disstance
def calculateDistance(tup1):
    current_route = numpy.array(tup1)
    distances = []
    for i in selected_centroids:
        centroid = numpy.array(i)
        distances.append(numpy.linalg.norm(current_route - centroid))
    return min(distances)

# Calculating all the distances and sorting the results by ascending value
# therefore smallest distance comes first
routesDistances = myRoutes.map(lambda x: (x[0], calculateDistance(x[1])))
sortRoute = routesDistances.map(lambda (x,y): (y,x)).sortByKey()
finalArray = sortRoute.map(lambda (x,y): (y,x))

top5Suggestions = finalArray.take(30)

for sug in top5Suggestions:
    print sug

#print routes 561652b473b2392c6954fb48
             #561652b473b2392c6954fb48







































'''
def main():
    conf = SparkConf().setAppName("pyspark test")
    sc = SparkContext(conf=conf)

    # Create an RDD backed by the MongoDB collection.
    # MongoInputFormat allows us to read from a live MongoDB instance.
    # We could also use BSONFileInputFormat to read BSON snapshots.
    rdd = sc.newAPIHadoopRDD(
        inputFormatClass='com.mongodb.hadoop.MongoInputFormat',
        keyClass='org.apache.hadoop.io.Text',
        valueClass='org.apache.hadoop.io.MapWritable',
        conf={
            'mongo.input.uri': 'mongodb://localhost:27017/monad.TravelRequest'
        }
    )

    # Save this RDD as a Hadoop "file".
    # The path argument is unused; all documents will go to "mongo.output.uri".
    rdd.saveAsNewAPIHadoopFile(
        path='file:///this-is-unused',
        outputFormatClass='com.mongodb.hadoop.MongoOutputFormat',
        keyClass='org.apache.hadoop.io.Text',
        valueClass='org.apache.hadoop.io.MapWritable',
        conf={
            'mongo.output.uri': 'mongodb://localhost:27017/output.collection'
        }
    )

    # We can also save this back to a BSON file.
    rdd.saveAsNewAPIHadoopFile(
        path='hdfs://localhost:8020/user/spark/bson-demo',
        outputFormatClass='com.mongodb.hadoop.BSONFileOutputFormat',
        keyClass='org.apache.hadoop.io.Text',
        valueClass='org.apache.hadoop.io.MapWritable'
    )

if __name__ == '__main__':
    main()
'''
