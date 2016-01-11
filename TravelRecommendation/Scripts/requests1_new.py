#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymongo
import json
import random
import datetime
import bson

#               0           1                   2           3          4                   5                    6                   7                  8                  9                10         11              12              13            14                15                 16               17             18             19             20                 21                 22             23           24          25           
positions = ['Flogsta','Polacksbacken','Central Station','Granby','Gamla Uppsala','Uppsala Science Park','Uppsala Centrum','Carolina Rediviva', 'Uppsala Hospital', 'Kungshögarna', 'Regins väg', 'Valhalls väg', 'Huges väg', 'Topeliusgatan', 'Värnlundsgatan', 'Ferlinsgatan', 'Heidenstamstorg', 'Kantorsgatan', 'Djäknegatan', 'Portalgatan', 'Höganäsgatan', 'Väderkvarnsgatan', 'Vaksala torg', 'Stadshuset', 'Skolgatan', 'Götgatan',
#     26              27             28
'Ekonomikum', 'Studentstaden', 'Rickomberga']
coordinates = [[59.851252, 17.593290], [59.840427, 17.647628], [59.858052, 17.644739], [59.875991, 17.674517], [59.897172, 17.636958], [59.842756, 17.638956], [59.854760, 17.632371], [59.847369, 17.641398], [59.8974234, 59.8974234], [59.8937918, 59.8937918], [59.8936454, 17.6447512], [59.8933053, 17.6495062], [59.8882135,17.6487986], [59.8865786,17.6454077], [59.8810458,17.649195], [59.8774538,17.6455243], [59.8745815,17.644333], [59.8680373,17.6395483], [59.8683433,17.6374992], [59.8647133,17.6405612], [59.8618897,17.6479104], [59.86142145, 17.6470993259306], [59.8604317,17.6404847], [59.8591773,17.625467],
[59.8650401,17.6250933], [59.85941415,17.6197556556358], [59.8576671,17.6131367], [59.8559593,17.6031045]]

from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()

db = client.monad

TravelRequest = db.TravelRequestNew

number = 1
seq = [0,1,2,3,4,5,6,7,10,11,12,13,14,15,16,19,20,21,22,23]
for j in range(28):
    day = 1
    first = random.randint(2,7)
    second = random.randint(2,7)
    new_record1 = {
                  "userId": 1,
                  "startTime": datetime.datetime(2015, 11, day, 8, random.randint(25,50), random.randint(0,59)),
                  "endTime": datetime.datetime(2015, 11, day, 9, random.randint(0,10), random.randint(0,59)),
                  "startPositionLatitude": coordinates[0][0],
                  "startPositionLongitude": coordinates[0][1],
                  "endPositionLatitude": coordinates[1][0],
                  "endPositionLongitude": coordinates[1][1],
                  "requestTime": datetime.datetime(2015, 11, day, 8, random.randint(0,18), random.randint(0,59))
                  }
    new_record2 = {
                  "userId": 1,
                  "startTime": datetime.datetime(2015, 11, day, 17, random.randint(5,20), random.randint(0,59)),
                  "endTime": datetime.datetime(2015, 11, day, 17, random.randint(40,59), random.randint(0,59)),
                  "startPositionLatitude": coordinates[1][0],
                  "startPositionLongitude": coordinates[1][1],
                  "endPositionLatitude": coordinates[0][0],
                  "endPositionLongitude": coordinates[0][1],
                  "requestTime": datetime.datetime(2015, 11, day, 17, random.randint(0,5), random.randint(0,59))
                  }
    TravelRequest.insert_many([new_record1, new_record2])
    day += 1