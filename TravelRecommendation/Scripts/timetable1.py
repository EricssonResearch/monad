#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pymongo
import bson
import random
import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId
#               0           1                   2           3          4                   5                    6                   7                  8                  9                10         11              12              13            14                15                 16               17             18             19             20                 21                 22             23           24          25           
busStops = ['Flogsta','Polacksbacken','Central Station','Granby','Gamla Uppsala','Uppsala Science Park','Uppsala Centrum','Carolina Rediviva', 'Uppsala Hospital', 'Kungshögarna', 'Regins väg', 'Valhalls väg', 'Huges väg', 'Topeliusgatan', 'Värnlundsgatan', 'Ferlinsgatan', 'Heidenstamstorg', 'Kantorsgatan', 'Djäknegatan', 'Portalgatan', 'Höganäsgatan', 'Väderkvarnsgatan', 'Vaksala torg', 'Stadshuset', 'Skolgatan', 'Götgatan',
#     26              27             28
'Ekonomikum', 'Studentstaden', 'Rickomberga']
coordinates = [[59.851252, 17.593290], [59.840427, 17.647628], [59.858052, 17.644739], [59.875991, 17.674517], [59.897172, 17.636958], [59.842756, 17.638956], [59.854760, 17.632371], [59.847369, 17.641398], [59.8974234, 59.8974234], [59.8937918, 59.8937918], [59.8936454, 17.6447512], [59.8933053, 17.6495062], [59.8882135,17.6487986], [59.8865786,17.6454077], [59.8810458,17.649195], [59.8774538,17.6455243], [59.8745815,17.644333], [59.8680373,17.6395483], [59.8683433,17.6374992], [59.8647133,17.6405612], [59.8618897,17.6479104], [59.86142145, 17.6470993259306], [59.8604317,17.6404847], [59.8591773,17.625467],
[59.8650401,17.6250933], [59.85941415,17.6197556556358], [59.8576671,17.6131367], [59.8559593,17.6031045]]
NUM_OF_ENTRIES = 10
YEAR = 2015
MONTH = 11
DAY = 30
TRIP_DURATION = 30
MIN_10 = datetime.timedelta(minutes = 10)
MIN_20 = datetime.timedelta(minutes = 20)
MIN_25 = datetime.timedelta(minutes = 25)
client = MongoClient()
db = client.monad
TimeTable = db.TimeTable

def createRoute(start, end):
    wp = []
    wp.append(start)
    wp.append(end)
    wp1 = random.choice(busStops)
    while (wp1 in wp):
        wp1 = random.choice(busStops)
    wp.append(wp1)
    wp2 = random.choice(busStops)
    while (wp2 in wp):
        wp2 = random.choice(busStops)
    wp.append(wp2)
    wp3 = random.choice(busStops)
    while (wp3 in wp):
        wp3 = random.choice(busStops)
    wp.append(wp3)
    wp4 = random.choice(busStops)
    while (wp4 in wp):
        wp4 = random.choice(busStops)
    wp.append(wp4)
    wp5 = random.choice(busStops)
    while (wp5 in wp):
        wp5 = random.choice(busStops)
    wp.append(wp5)
    wp6 = random.choice(busStops)
    while (wp6 in wp):
        wp6 = random.choice(busStops)
    wp.append(wp6)
    wp7 = random.choice(busStops)
    while (wp7 in wp):
        wp7 = random.choice(busStops)
    wp.append(wp7)
    wp8 = random.choice(busStops)
    while (wp8 in wp):
        wp8 = random.choice(busStops)
    wp.append(wp8)
    wp9 = random.choice(busStops)
    while (wp9 in wp):
        wp9 = random.choice(busStops)
    wp.append(wp9)
    wp10 = random.choice(busStops)
    while (wp10 in wp):
        wp10 = random.choice(busStops)
    wp.append(wp10)
    wp10 = random.choice(busStops)
    while (wp10 in wp):
        wp10 = random.choice(busStops)
    wp.append(wp10)
    wp10 = random.choice(busStops)
    while (wp10 in wp):
        wp10 = random.choice(busStops)
    wp.append(wp10)
    wp11 = random.choice(busStops)
    while (wp11 in wp):
        wp11 = random.choice(busStops)
    wp.append(wp11)
    wp12 = random.choice(busStops)
    while (wp12 in wp):
        wp12 = random.choice(busStops)
    wp.append(wp12)
    wp13 = random.choice(busStops)
    while (wp13 in wp):
        wp13 = random.choice(busStops)
    wp.append(wp13)
    wp14 = random.choice(busStops)
    while (wp14 in wp):
        wp14 = random.choice(busStops)
    wp.append(wp14)
    wp15 = random.choice(busStops)
    while (wp15 in wp):
        wp15 = random.choice(busStops)
    wp.append(wp15)
    wp16 = random.choice(busStops)
    while (wp16 in wp):
        wp16 = random.choice(busStops)
    wp.append(wp16)
    wp17 = random.choice(busStops)
    while (wp17 in wp):
        wp17 = random.choice(busStops)
    wp.append(wp17)
    wp18 = random.choice(busStops)
    while (wp18 in wp):
        wp18 = random.choice(busStops)
    wp.append(wp18)
    wp19 = random.choice(busStops)
    while (wp19 in wp):
        wp19 = random.choice(busStops)
    wp.append(wp19)
    wp20 = random.choice(busStops)
    while (wp20 in wp):
        wp20 = random.choice(busStops)
    wp.append(wp20)
    wp21 = random.choice(busStops)
    while (wp21 in wp):
        wp21 = random.choice(busStops)
    wp.append(wp21)
    wp22 = random.choice(busStops)
    while (wp22 in wp):
        wp22 = random.choice(busStops)
    wp.append(wp22)
    wp23 = random.choice(busStops)
    while (wp23 in wp):
        wp23 = random.choice(busStops)
    wp.append(wp23)
    wp24 = random.choice(busStops)
    while (wp24 in wp):
        wp24 = random.choice(busStops)
    wp.append(wp24)
    '''wp25 = random.choice(busStops)
    while (wp25 in wp):
        wp25 = random.choice(busStops)
    wp.append(wp25)
    wp26 = random.choice(busStops)
    while (wp26 in wp):
        wp26 = random.choice(busStops)
    wp.append(wp26)
    wp27 = random.choice(busStops)
    while (wp27 in wp):
        wp27 = random.choice(busStops)
    wp.append(wp27)
    wp28 = random.choice(busStops)
    while (wp28 in wp):
        wp28 = random.choice(busStops)
    wp.append(wp28)
    wp29 = random.choice(busStops)
    while (wp29 in wp):
        wp29 = random.choice(busStops)
    wp.append(wp29)
    wp30 = random.choice(busStops)
    while (wp30 in wp):
        wp30 = random.choice(busStops)
    wp.append(wp30)'''
    del wp[1]
    wp.append(end)
    return wp



for i in range(500):
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
                     {"BusStopID": route[4], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[5], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[6], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[7], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                      {"BusStopID": route[8], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[9], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[10], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[11], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                     {"BusStopID": route[12], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[13], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[14], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[15], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},   
                      {"BusStopID": route[16], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[17], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                      {"BusStopID": route[18], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[19], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[20], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[21], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                     {"BusStopID": route[22], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[23], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[24], "DptTime": endTime,
                         "PsgGetOn": 0, "PsgGetOff": 5, "latitude": end_position_lat,
                         "longitude": end_position_lon}],
                 "GeneratedTime": 0,
                 "VehicleID": random.randint(0, 59),
                 "DriverID": random.randint(0, 59)
                }



    for i in range(500):
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
        endTime = datetime.datetime(YEAR, MONTH, DAY, 17, random.randint(40, 59), 0)

        new_record2 = {
                 "_id": original_id,
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
                     {"BusStopID": route[4], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[5], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[6], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[7], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                      {"BusStopID": route[8], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[9], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[10], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[11], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                     {"BusStopID": route[12], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[13], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[14], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[15], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},   
                      {"BusStopID": route[16], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[17], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                      {"BusStopID": route[18], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[19], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[20], "DptTime": startTime + MIN_20,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.002,
                         "longitude": start_position_lon + 0.002},
                     {"BusStopID": route[21], "DptTime": startTime + MIN_25,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.003,
                         "longitude": start_position_lon + 0.003},
                     {"BusStopID": route[22], "DptTime": startTime,
                         "PsgGetOn": 5, "PsgGetOff": 0, "latitude": start_position_lat,
                         "longitude": start_position_lon},
                     {"BusStopID": route[23], "DptTime": startTime + MIN_10,
                         "PsgGetOn": 5, "PsgGetOff": 5, "latitude": start_position_lat + 0.001,
                         "longitude": start_position_lon + 0.001},
                     {"BusStopID": route[24], "DptTime": endTime,
                         "PsgGetOn": 0, "PsgGetOff": 5, "latitude": end_position_lat,
                         "longitude": end_position_lon}],
                 "GeneratedTime": 0,
                 "VehicleID": random.randint(0, 59),
                 "DriverID": random.randint(0, 59)
                }
    TimeTable.insert_many([new_record1, new_record2])