#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import datetime
import bson
from datetime import date
from bson.objectid import ObjectId
from pymongo import MongoClient

line = [1,2,3,4]
YEAR = 2015
MONTH = 10
DAY = 29
BusTrip1 = [ObjectId(),ObjectId(),ObjectId(),ObjectId(),ObjectId()]
BusTrip2 = [ObjectId(),ObjectId(),ObjectId(),ObjectId(),ObjectId()]
BusTrip3 = [ObjectId(),ObjectId(),ObjectId(),ObjectId(),ObjectId()]
BusTrip4 = [ObjectId(),ObjectId(),ObjectId(),ObjectId(),ObjectId()]

BusStops = [ObjectId(),ObjectId(),ObjectId(),ObjectId(),ObjectId(),
            ObjectId(),ObjectId(),ObjectId(),ObjectId(),ObjectId()]
Positions = ['Flogsta','Polacksbacken','Central Station','Granby', 'Gamla Uppsala','Uppsala Science Park','Uppsala Centrum','Carolina Rediviva', 'Uppsala Hospital', 'Kungshögarna', 'Regins väg']

Coordinates = [[59.851252, 17.593290], [59.840427, 17.647628],
[59.858052, 17.644739], [59.875991, 17.674517], [59.897172, 17.636958],
[59.842756, 17.638956], [59.854760, 17.632371], [59.847369, 17.641398],
[59.8974234, 59.8974234], [59.8937918, 59.8937918]]

client = MongoClient()
db = client.monad
TimeTableN = db.TimeTableN
BusStopN = db.BusStopN

today1 = {
    "Line": line[0],
    "Date": datetime.datetime(YEAR, MONTH, DAY),
    "Timetable": BusTrip1
}

today2 = {
    "Line": line[1],
    "Date": datetime.datetime(YEAR, MONTH, DAY),
    "Timetable": BusTrip2
}

today3 = {
    "Line": line[2],
    "Date": datetime.datetime(YEAR, MONTH, DAY),
    "Timetable": BusTrip3
}

today4 = {
    "Line": line[3],
    "Date": datetime.datetime(YEAR, MONTH, DAY),
    "Timetable": BusTrip4
}



busstop1 = {
    "_id": BusStops[0],
    "Name": Positions[0],
    "Latitude": Coordinates[0][0],
    "Longitude": Coordinates[0][1]
}

busstop2 = {
    "_id": BusStops[1],
    "Name": Positions[1],
    "Latitude": Coordinates[1][0],
    "Longitude": Coordinates[1][1]
}

busstop3 = {
    "_id": BusStops[2],
    "Name": Positions[2],
    "Latitude": Coordinates[2][0],
    "Longitude": Coordinates[2][1]
}

busstop4 = {
    "_id": BusStops[3],
    "Name": Positions[3],
    "Latitude": Coordinates[3][0],
    "Longitude": Coordinates[3][1]
}

busstop5 = {
    "_id": BusStops[4],
    "Name": Positions[4],
    "Latitude": Coordinates[4][0],
    "Longitude": Coordinates[4][1]
}

busstop6 = {
    "_id": BusStops[5],
    "Name": Positions[5],
    "Latitude": Coordinates[5][0],
    "Longitude": Coordinates[5][1]
}

busstop7 = {
    "_id": BusStops[6],
    "Name": Positions[6],
    "Latitude": Coordinates[6][0],
    "Longitude": Coordinates[6][1]
}

busstop8 = {
    "_id": BusStops[7],
    "Name": Positions[7],
    "Latitude": Coordinates[7][0],
    "Longitude": Coordinates[7][1]
}

busstop9 = {
    "_id": BusStops[8],
    "Name": Positions[8],
    "Latitude": Coordinates[8][0],
    "Longitude": Coordinates[8][1]
}

busstop10 = {
    "_id": BusStops[9],
    "Name": Positions[9],
    "Latitude": Coordinates[9][0],
    "Longitude": Coordinates[9][1]
}
TimeTableN.insert_many([today1, today2, today3, today4])
BusStopN.insert_many([busstop1, busstop2, busstop3, busstop4, busstop5,
busstop6, busstop7, busstop8, busstop9, busstop10])

minute = 0
bustrip = {
    "_id": BusTrip1[0],
    "line": 1,
    "trajectory": [
        {
            "BusStop": BusStops[0],
            "Capacity": 1,
	    "time": datetime.datetime(YEAR, MONTH, DAY, 10, minute)

        },
	{
            "BusStop": BusStops[1],
            "Capacity": 1,
	    "time": datetime.datetime(YEAR, MONTH, DAY, 10, minute+2)

        },
	{
            "BusStop": BusStops[2],
            "Capacity": 1,
	    "time": datetime.datetime(YEAR, MONTH, DAY, 10, minute+4)

        },
	{
            "BusStop": BusStops[3],
            "Capacity": 1,
	    "time": datetime.datetime(YEAR, MONTH, DAY, 10, minute+8)

        },
	{
            "BusStop": BusStops[4],
            "Capacity": 1,
	    "time": datetime.datetime(YEAR, MONTH, DAY, 10, minute+11)

        }
    ]
    }
db.BusTripN.insert(bustrip)



allIds = []
tt = db.TimeTableN.find()
for i in tt:
    allIds += i["Timetable"]


trips = db.BusTripN.find()
for trip in trips:
    print trip['trajectory']
