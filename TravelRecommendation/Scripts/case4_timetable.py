import pymongo
import bson
import random
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

busStops = ['Flogsta','Polacksbacken','Central Station','Granby','Gamla Uppsala','Uppsala Science Park','Uppsala Centrum','Carolina Rediviva', 'Uppsala Hospital']
coordinates = [[59.851252, 17.593290], [59.840427, 17.647628], [59.858052, 17.644739], [59.875991, 17.674517], [59.897172, 17.636958], [59.842756, 17.638956], [59.854760, 17.632371], [59.847369, 17.641398]]
NUM_OF_ENTRIES = 10
YEAR = 2015
MONTH = 11
DAY = 30
TRIP_DURATION = 30
MIN_10 = datetime.timedelta(minutes = 10)
MIN_20 = datetime.timedelta(minutes = 20)
MIN_25 = datetime.timedelta(minutes = 25)

def createRoute(start, end):
    wp1 = random.choice(busStops)
    while (wp1 == start or wp1 == end):
        wp1 = random.choice(busStops)
    wp2 = random.choice(busStops)
    while (wp2 == start or wp2 == end or wp2 == wp1):
        wp2 = random.choice(busStops)
    wp3 = random.choice(busStops)
    while (wp3 == start or wp3 == end or wp3 == wp1 or wp3 == wp2):
        wp3 = random.choice(busStops)
    return [busStops.index(start), busStops.index(wp1), busStops.index(wp2),
        busStops.index(wp3), busStops.index(end)]


client = MongoClient()

db = client.monad

for i in range(28):
    original_id = ObjectId()
    hour = 8
    minute = random.randint(25, 50)
    st = 0
    ed = 1
    start = busStops[0]
    start_position_lat = coordinates[st][0]
    start_position_lon = coordinates[st][1]
    end_position_lat = coordinates[ed][0]
    end_position_lon = coordinates[ed][1]
    end = busStops[1]
    route = createRoute(start, end)
    startTime = datetime.datetime(YEAR, MONTH, DAY, hour, minute, 0)
    endTime = datetime.datetime(
        YEAR, MONTH, DAY, 9, random.randint(0, 10), 0)

    new_record1 = {
                 "_id": original_id,
                 #"BusNo": random.randint(0, 59),
                 "StartTime": startTime,
                 "StartBusstop": start,
                 "EndTime": endTime,
                 "EndBusstop": end,
                 "start_position_lat": start_position_lat,
                 "start_position_lon": start_position_lon,
                 "end_position_lat": end_position_lat,
                 "end_position_lon": end_position_lon,
                 "Waypoints": [
                     {"BusStopID": route[0], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[1], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[2], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[3], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                     {"BusStopID": route[4], "DptTime": endTime,
                         "PsgGetOn": 0, "PsgGetOff": 5, "latitude": end_position_lat,
                         "longitude": end_position_lon}],
                 "GeneratedTime": 0,
                 "VehicleID": random.randint(0, 59),
                 "DriverID": random.randint(0, 59)
                }


    for i in range(28):
        original_id = ObjectId()
        hour = 17
        minute = random.randint(5,20)
        st = 1
        ed = 0
        start = busStops[1]
        start_position_lat = coordinates[st][0]
        start_position_lon = coordinates[st][1]
        end_position_lat = coordinates[ed][0]
        end_position_lon = coordinates[ed][1]
        end = busStops[0]
        route = createRoute(start, end)
        startTime = datetime.datetime(YEAR, MONTH, DAY, hour, minute, 0)
        endTime = datetime.datetime(
            YEAR, MONTH, DAY, 17, random.randint(40, 59), 0)

        new_record2 = {
                 "_id": original_id,
                 #"BusNo": random.randint(0, 59),
                 "StartTime": startTime,
                 "StartBusstop": start,
                 "EndTime": endTime,
                 "EndBusstop": end,
                 "start_position_lat": start_position_lat,
                 "start_position_lon": start_position_lon,
                 "end_position_lat": end_position_lat,
                 "end_position_lon": end_position_lon,
                 "Waypoints": [
                     {"BusStopID": route[0], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[1], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[2], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[3], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                     {"BusStopID": route[4], "DptTime": endTime,
                         "PsgGetOn": 0, "PsgGetOff": 5, "latitude": end_position_lat,
                         "longitude": end_position_lon}],
                 "GeneratedTime": 0,
                 "VehicleID": random.randint(0, 59),
                 "DriverID": random.randint(0, 59)
                }


    for i in range(28):
        original_id = ObjectId()
        hour = random.randint(0, 22)
        minute = random.randint(0, 59)
        st = random.randint(0,7)
        ed = random.randint(0,7)
        start = random.choice(busStops)
        start_position_lat = coordinates[st][0]
        start_position_lon = coordinates[st][1]
        end_position_lat = coordinates[ed][0]
        end_position_lon = coordinates[ed][1]
        end = random.choice(busStops)
        route = createRoute(start, end)
        startTime = datetime.datetime(YEAR, MONTH, DAY, hour, minute, 0)
        endTime = datetime.datetime(
            YEAR, MONTH, DAY, hour+1, minute, 0)

        new_record3 = {
                 "_id": original_id,
                 #"BusNo": random.randint(0, 59),
                 "StartTime": startTime,
                 "StartBusstop": start,
                 "EndTime": endTime,
                 "EndBusstop": end,
                 "start_position_lat": start_position_lat,
                 "start_position_lon": start_position_lon,
                 "end_position_lat": end_position_lat,
                 "end_position_lon": end_position_lon,
                 "Waypoints": [
                     {"BusStopID": route[0], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[1], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[2], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[3], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                     {"BusStopID": route[4], "DptTime": endTime,
                         "PsgGetOn": 0, "PsgGetOff": 5, "latitude": end_position_lat,
                         "longitude": end_position_lon}],
                 "GeneratedTime": 0,
                 "VehicleID": random.randint(0, 59),
                 "DriverID": random.randint(0, 59)
                }

    for i in range(28):
        original_id = ObjectId()
        hour = random.randint(0, 22)
        minute = random.randint(0, 59)
        st = 3
        ed = 4
        start = busStops[st]
        start_position_lat = coordinates[st][0]
        start_position_lon = coordinates[st][1]
        end_position_lat = coordinates[ed][0]
        end_position_lon = coordinates[ed][1]
        end = busStops[ed]
        route = createRoute(start, end)
        startTime = datetime.datetime(YEAR, MONTH, DAY, 12, minute, 0)
        endTime = datetime.datetime(
            YEAR, MONTH, DAY, 12, minute, 0)

        new_record4 = {
                 "_id": original_id,
                 #"BusNo": random.randint(0, 59),
                 "StartTime": startTime,
                 "StartBusstop": start,
                 "EndTime": endTime,
                 "EndBusstop": end,
                 "start_position_lat": start_position_lat,
                 "start_position_lon": start_position_lon,
                 "end_position_lat": end_position_lat,
                 "end_position_lon": end_position_lon,
                 "Waypoints": [
                     {"BusStopID": route[0], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[1], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[2], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[3], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                     {"BusStopID": route[4], "DptTime": endTime,
                         "PsgGetOn": 0, "PsgGetOff": 5, "latitude": end_position_lat,
                         "longitude": end_position_lon}],
                 "GeneratedTime": 0,
                 "VehicleID": random.randint(0, 59),
                 "DriverID": random.randint(0, 59)
                }

    result = db.TimeTable.insert_many([new_record1, new_record2, new_record3, new_record4])
