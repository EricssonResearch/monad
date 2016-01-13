# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
import bson
from bson.objectid import ObjectId
import datetime, sys

SERVER = False
YEAR  = 2015
MONTH = 11
DAY   = 10

client = MongoClient()
db = client.monad

def writeToDB():
    print('Do you really want to change the TimeTable collection on ' + str(client) + '? ')
    sys.stdin.read(1)
    db.TimeTable.insert_many(routes1_101)
    db.TimeTable.insert_many(routes2_102)
    db.TimeTable.insert_many(routes3_103)
    db.TimeTable.insert_many(routes5_105)
    db.TimeTable.insert_many(routes14_114)

routes1_101 = [
{
    "_id" : ObjectId(),
    "line" : 101,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
},
{
    "_id" : ObjectId(),
    "line" : 1,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
} ]
routes2_102 = [
{
    "_id" : ObjectId(),
    "line" : 2,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
},
{
    "_id" : ObjectId(),
    "line" : 102,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
} ]
routes3_103 = [
{
    "_id" : ObjectId(),
    "line" : 3,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
},
{
    "_id" : ObjectId(),
    "line" : 103,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
} ]
routes5_105 = [
{
    "_id" : ObjectId(),
    "line" : 5,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
},
{
    "_id" : ObjectId(),
    "line" : 105,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
} ]
routes14_114 = [
{
    "_id" : ObjectId(),
    "line" : 114,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
},
{
    "_id" : ObjectId(),
    "line" : 14,
    "date" : datetime.datetime(YEAR, MONTH, DAY),
    "timetable" : []
} ]

writeToDB()
