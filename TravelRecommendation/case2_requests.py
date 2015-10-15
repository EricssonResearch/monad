import pymongo
import json
import random
import datetime
import bson

positions = ['Flogsta','Polacksbacken','Central Station','Granby','Gamla Uppsala','Uppsala Science Park','Uppsala Centrum','Carolina Rediviva', 'Uppsala Hospital']
coordinates = [[59.851252, 17.593290], [59.840427, 17.647628], [59.858052, 17.644739], [59.875991, 17.674517], [59.897172, 17.636958], [59.842756, 17.638956], [59.854760, 17.632371], [59.847369, 17.641398]]

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()

db = client.monad

TravelRequest = db.TravelRequest

number = 1
day = 1
seq = [0,1,2,3,4,5,6,7,10,11,12,13,14,15,16,19,20,21,22,23]
for i in range(28):
    first = random.randint(2,7)
    second = random.randint(2,7)
    new_record1 = {"username": "user",
                  "start_time": datetime.datetime(2015, 11, day, 8, random.randint(25,50), random.randint(0,59)),
                  "end_time": datetime.datetime(2015, 11, day, 9, random.randint(0,10), random.randint(0,59)),
                  "start_position_lat": coordinates[0][0],
                  "start_position_lon": coordinates[0][1],
                  "end_position_lat": coordinates[1][0],
                  "end_position_lon": coordinates[1][1],
                  "request_time": datetime.datetime(2015, 11, day, 8, random.randint(0,18), random.randint(0,59))
                  }
    new_record2 = {"username": "user",
                  "start_time": datetime.datetime(2015, 11, day, 17, random.randint(5,20), random.randint(0,59)),
                  "end_time": datetime.datetime(2015, 11, day, 17, random.randint(40,59), random.randint(0,59)),
                  "start_position_lat": coordinates[1][0],
                  "start_position_lon": coordinates[1][1],
                  "end_position_lat": coordinates[0][0],
                  "end_position_lon": coordinates[0][1],
                  "request_time": datetime.datetime(2015, 11, day, 17, random.randint(0,5), random.randint(0,59))
                  }
    TravelRequest.insert_many([new_record1, new_record2])
    day += 1
