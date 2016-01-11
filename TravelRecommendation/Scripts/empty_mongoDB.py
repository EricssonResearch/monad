import pymongo

from pymongo import MongoClient

client = MongoClient()

db = client.monad

db.TravelRequest.remove({})
db.TimeTable.remove({})
