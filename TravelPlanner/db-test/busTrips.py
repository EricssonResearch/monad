# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
import bson
from bson.objectid import ObjectId
import datetime, sys
import random

SERVER = False
YEAR  = 2015
MONTH = 11
DAY   = 10
DATE  = datetime.datetime(YEAR, MONTH, DAY)

client = MongoClient()
db = client.monad

def mins(minIN):
    return datetime.timedelta(minutes = minIN)
def hmin(hourIN, minIN):
    return datetime.timedelta(hours = hourIN, minutes = minIN)

def writeInDB():
    print('Do you really want to change the BusTrip collection on ' + str(client) + '? ')
    sys.stdin.read(1)
    line1TT = db.TimeTable.find_one({"line": 1, "date": DATE})
    timetable_l1 = line1TT["_id"]
    db.BusTrip.insert_many(line1)
    db.TimeTable.update_one({"_id": timetable_l1}, {"$set": {"timetable": line1IDs}})

    line101TT = db.TimeTable.find_one({"line": 101, "date": DATE})
    timetable_l101 = line101TT["_id"]
    db.BusTrip.insert_many(line101)
    db.TimeTable.update_one({"_id": timetable_l101}, {"$set": {"timetable": line101IDs}})

    line2TT = db.TimeTable.find_one({"line": 2, "date": DATE})
    timetable_l2 = line2TT["_id"]
    db.BusTrip.insert_many(line2)
    db.TimeTable.update_one({"_id": timetable_l2}, {"$set": {"timetable": line2IDs}})

    line102TT = db.TimeTable.find_one({"line": 102, "date": DATE})
    timetable_l102 = line102TT["_id"]
    db.BusTrip.insert_many(line102)
    db.TimeTable.update_one({"_id": timetable_l102}, {"$set": {"timetable": line102IDs}})

    line3TT = db.TimeTable.find_one({"line": 3, "date": DATE})
    timetable_l3 = line3TT["_id"]
    db.BusTrip.insert_many(line3)
    db.TimeTable.update_one({"_id": timetable_l3}, {"$set": {"timetable": line3IDs}})

    line103TT = db.TimeTable.find_one({"line": 103, "date": DATE})
    timetable_l103 = line103TT["_id"]
    db.BusTrip.insert_many(line103)
    db.TimeTable.update_one({"_id": timetable_l103}, {"$set": {"timetable": line103IDs}})

    line5TT = db.TimeTable.find_one({"line": 5, "date": DATE})
    timetable_l5 = line5TT["_id"]
    db.BusTrip.insert_many(line5)
    db.TimeTable.update_one({"_id": timetable_l5}, {"$set": {"timetable": line5IDs}})

    line105TT = db.TimeTable.find_one({"line": 105, "date": DATE})
    timetable_l105 = line105TT["_id"]
    db.BusTrip.insert_many(line105)
    db.TimeTable.update_one({"_id": timetable_l105}, {"$set": {"timetable": line105IDs}})

    line14TT = db.TimeTable.find_one({"line": 14, "date": DATE})
    timetable_l14 = line14TT["_id"]
    db.BusTrip.insert_many(line14)
    db.TimeTable.update_one({"_id": timetable_l14}, {"$set": {"timetable": line14IDs}})

    line114TT = db.TimeTable.find_one({"line": 114, "date": DATE})
    timetable_l114 = line114TT["_id"]
    db.BusTrip.insert_many(line114)
    db.TimeTable.update_one({"_id": timetable_l114}, {"$set": {"timetable": line114IDs}})
    
################### line 1 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 33,
    "line" : 1,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 23),
    "capacity" : 60,
    "trajectory" : [
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
            "busStop" : ObjectId("56321850aef06e102712208d")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 03),
            "busStop" : ObjectId("56321850aef06e102712208e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 04),
            "busStop" : ObjectId("56321850aef06e102712208f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05),
            "busStop" : ObjectId("56321850aef06e1027122090")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 07),
            "busStop" : ObjectId("56321850aef06e1027122092")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8),
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 9),
            "busStop" : ObjectId("5640a09273b239624322ed1e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 10),
            "busStop" : ObjectId("5640a09273b239624322ed1f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 12),
            "busStop" : ObjectId("5640a09273b239624322ed20")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 13),
            "busStop" : ObjectId("5640a09273b239624322ed21")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 14),
            "busStop" : ObjectId("5640a09273b239624322ed22")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 15),
            "busStop" : ObjectId("5640a09273b239624322ed23")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 16),
            "busStop" : ObjectId("5640a09273b239624322ed24")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18),
            "busStop" : ObjectId("5640a09273b239624322ed25")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 20),
            "busStop" : ObjectId("5640a09273b239624322ed26")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 22),
            "busStop" : ObjectId("5640a09273b239624322ed27")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 23),
            "busStop" : ObjectId("5640a09273b239624322ed28")
        }
    ]
}
timeDiffs = [mins(4), mins(9), mins(19), mins(27), mins(35), mins(39), mins(45), mins(47), mins(56),
        hmin(2, 25), hmin(2, 30), hmin(2, 54), hmin(2, 58), hmin(3, 27), hmin(3, 49), hmin(4, 8),
        hmin(4, 43), hmin(5, 25), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 42), hmin(6, 47),
        hmin(6, 48), hmin(6, 52), hmin(7, 27), hmin(8, 04), hmin(9, 14), hmin(9, 18), hmin(9, 25),
        hmin(9, 29), hmin(10, 7), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 00), hmin(13, 20), hmin(13, 25), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 32), hmin(14, 48), hmin(14, 53),
        hmin(15, 03), hmin(15, 18), hmin(15, 34), hmin(15, 36), hmin(15, 42), hmin(16, 0),
        hmin(16, 30), hmin(16, 50), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 18), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 03), hmin(19, 31),
        hmin(19, 48), hmin(19, 49), hmin(19, 55), hmin(19, 59), hmin(20, 00), hmin(20, 07),
        hmin(20, 19), hmin(20, 28), hmin(20, 43), hmin(21, 13), hmin(21, 33), hmin(21, 51),
        hmin(22, 29), hmin(22, 58), hmin(23, 12), hmin(23, 34), hmin(23, 50)]
line1 = [baseEntry]
line1IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line1.append(entry)
    line1IDs.append(tripID)

################### line 101 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 31,
    "line" : 101,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 23),
    "capacity" : 60,
    "trajectory" : [
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
            "busStop" : ObjectId("5640a09273b239624322ed28")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 03),
            "busStop" : ObjectId("5640a09273b239624322ed27")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05),
            "busStop" : ObjectId("5640a09273b239624322ed26")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 07),
            "busStop" : ObjectId("5640a09273b239624322ed25")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 9),
            "busStop" : ObjectId("5640a09273b239624322ed24")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 10),
            "busStop" : ObjectId("5640a09273b239624322ed23")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 11),
            "busStop" : ObjectId("5640a09273b239624322ed22")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 12),
            "busStop" : ObjectId("5640a09273b239624322ed21")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 13),
            "busStop" : ObjectId("5640a09273b239624322ed20")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 14),
            "busStop" : ObjectId("5640a09273b239624322ed1f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 15),
            "busStop" : ObjectId("5640a09273b239624322ed1e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 16),
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 17),
            "busStop" : ObjectId("56321850aef06e1027122092")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18),
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 19),
            "busStop" : ObjectId("56321850aef06e1027122090")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 21),
            "busStop" : ObjectId("56321850aef06e102712208f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 22),
            "busStop" : ObjectId("56321850aef06e102712208e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 23),
            "busStop" : ObjectId("56321850aef06e102712208d")
        }
    ]
}
timeDiffs = [mins(4), mins(12), mins(19), mins(27), mins(35), mins(39), mins(45), mins(47), mins(56),
        hmin(2, 25), hmin(2, 30), hmin(2, 54), hmin(2, 58), hmin(3, 27), hmin(3, 49), hmin(4, 8),
        hmin(4, 43), hmin(5, 25), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 42), hmin(6, 47),
        hmin(6, 48), hmin(6, 52), hmin(7, 27), hmin(8, 04), hmin(9, 14), hmin(9, 18), hmin(9, 25),
        hmin(9, 29), hmin(10, 7), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 00), hmin(13, 20), hmin(13, 25), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 32), hmin(14, 48), hmin(14, 53),
        hmin(15, 03), hmin(15, 18), hmin(15, 34), hmin(15, 36), hmin(15, 42), hmin(16, 0),
        hmin(16, 30), hmin(16, 50), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 18), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 03), hmin(19, 31),
        hmin(19, 48), hmin(19, 49), hmin(19, 55), hmin(19, 59), hmin(20, 00), hmin(20, 07),
        hmin(20, 19), hmin(20, 28), hmin(20, 43), hmin(21, 13), hmin(21, 33), hmin(21, 51),
        hmin(22, 29), hmin(22, 58), hmin(23, 12), hmin(23, 34), hmin(23, 50)]
line101 = [baseEntry]
line101IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line101.append(entry)
    line101IDs.append(tripID)

################### line 2 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 77,
    "capacity" : 60,
    "line" : 2,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 39),
    "trajectory" : [ 
        {
            "busStop" : ObjectId("562a07c473b23914826f046f"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 01)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0470"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 03)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0471"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0472"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0473"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 07)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0474"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 9)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0475"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 10)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0476"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 11)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0477"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 13)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0478"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 14)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0479"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 15)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047a"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 16)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047b"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 17)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047c"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047d"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047e"),
            "capacity" : 60,
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 22)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047f"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 24)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0480"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 26)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0481"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 27)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0482"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 29)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0483"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 30)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0484"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 32)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0485"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 32)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0486"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 33)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0487"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 34)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0488"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 35)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0489"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 37)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f048a"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 38)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f048b"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 39)
        }
    ]
}

timeDiffs = [mins(2), mins(4), mins(11), mins(15), mins(35), mins(35), mins(45), mins(47), mins(56),
        hmin(2, 25), hmin(2, 30), hmin(2, 54), hmin(2, 58), hmin(3, 37), hmin(3, 44), hmin(4, 8),
        hmin(4, 43), hmin(5, 25), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 42), hmin(6, 47),
        hmin(6, 48), hmin(6, 52), hmin(7, 27), hmin(8, 04), hmin(9, 14), hmin(9, 18), hmin(9, 25),
        hmin(9, 29), hmin(10, 27), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 16), hmin(13, 18), hmin(13, 20), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 42), hmin(14, 48), hmin(14, 53),
        hmin(15, 13), hmin(15, 18), hmin(15, 34), hmin(15, 36), hmin(15, 42), hmin(16, 0),
        hmin(16, 54), hmin(16, 56), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 18), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 03), hmin(19, 41),
        hmin(19, 48), hmin(19, 49), hmin(19, 55), hmin(19, 59), hmin(20, 00), hmin(20, 07),
        hmin(20, 19), hmin(20, 28), hmin(20, 33), hmin(21, 13), hmin(21, 13), hmin(21, 41),
        hmin(22, 29), hmin(22, 58), hmin(23, 02), hmin(23, 04), hmin(23, 16)]
line2 = [baseEntry]
line2IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line2.append(entry)
    line2IDs.append(tripID)

################### line 102 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 15,
    "capacity" : 60,
    "line" : 102,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 39),
    "trajectory" : [ 
        {
            "busStop" : ObjectId("562a07c473b23914826f048b"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 01)
        },
        {
            "busStop" : ObjectId("562a07c473b23914826f048a"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 02)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0489"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 03)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0488"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0487"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0486"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 07)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0485"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0484"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0483"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 10)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0482"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 11)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0481"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 13)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0480"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 14)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047f"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 16)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047e"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047d"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 22)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047c"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 23)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047b"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 24)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f047a"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 25)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0479"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 26)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0478"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 27)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0477"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 28)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0476"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 30)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0475"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 31)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0474"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 32)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0473"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 34)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0472"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 35)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0471"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 36)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f0470"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 38)
        }, 
        {
            "busStop" : ObjectId("562a07c473b23914826f046f"),
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 39)
        }, 
    ]
}

timeDiffs = [mins(2), mins(4), mins(15), mins(35), mins(35), mins(45), mins(47), mins(56),
        hmin(1, 25), hmin(2, 10), hmin(2, 34), hmin(2, 58), hmin(3, 27), hmin(3, 44), hmin(4, 8),
        hmin(4, 43), hmin(5, 05), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 42), hmin(6, 47),
        hmin(6, 48), hmin(6, 52), hmin(7, 27), hmin(8, 04), hmin(9, 14), hmin(9, 18), hmin(9, 25),
        hmin(9, 29), hmin(10, 07), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 16), hmin(13, 18), hmin(13, 20), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 42), hmin(14, 48), hmin(14, 53),
        hmin(15, 13), hmin(15, 18), hmin(15, 34), hmin(15, 36), hmin(15, 42), hmin(16, 0),
        hmin(16, 54), hmin(16, 56), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 07), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 13), hmin(19, 41),
        hmin(19, 48), hmin(19, 49), hmin(19, 55), hmin(19, 59), hmin(20, 10), hmin(20, 17),
        hmin(20, 29), hmin(20, 38), hmin(20, 53), hmin(21, 13), hmin(21, 33), hmin(21, 41),
        hmin(22, 29), hmin(22, 58), hmin(23, 02), hmin(23, 14), hmin(23, 36)]
line102 = [baseEntry]
line102IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line102.append(entry)
    line102IDs.append(tripID)

################### line 3 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 45,
    "line" : 3,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 38),
    "capacity" : 60,
    "trajectory" : [
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
            "busStop" : ObjectId("5641aa72aef06e0b819e352d")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 03),
            "busStop" : ObjectId("5641aa72aef06e0b819e352e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05),
            "busStop" : ObjectId("5641aa72aef06e0b819e352f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("5641aa72aef06e0b819e3530")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8),
            "busStop" : ObjectId("5641aa72aef06e0b819e3531")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 10),
            "busStop" : ObjectId("5641aa72aef06e0b819e3532")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 13),
            "busStop" : ObjectId("562a07c473b23914826f047b")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 15),
            "busStop" : ObjectId("562a07c473b23914826f047c")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 17),
            "busStop" : ObjectId("562a07c473b23914826f047d")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18),
            "busStop" : ObjectId("56321850aef06e102712208d")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 19),
            "busStop" : ObjectId("56321850aef06e102712208e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 21),
            "busStop" : ObjectId("56321850aef06e102712208f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 22),
            "busStop" : ObjectId("56321850aef06e1027122090")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 23),
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 24),
            "busStop" : ObjectId("56321850aef06e1027122092")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 25),
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 26),
            "busStop" : ObjectId("56321850aef06e1027122094")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 28),
            "busStop" : ObjectId("56321850aef06e1027122095")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 29),
            "busStop" : ObjectId("5641aa72aef06e0b819e3533")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 30),
            "busStop" : ObjectId("5641aa72aef06e0b819e3534")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 31),
            "busStop" : ObjectId("5641aa72aef06e0b819e3535")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 32),
            "busStop" : ObjectId("5641aa72aef06e0b819e3536")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 34),
            "busStop" : ObjectId("5641aa72aef06e0b819e3537")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 35),
            "busStop" : ObjectId("5641aa72aef06e0b819e3538")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 36),
            "busStop" : ObjectId("5641aa72aef06e0b819e3539")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 37),
            "busStop" : ObjectId("5641aa72aef06e0b819e353a")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 38),
            "busStop" : ObjectId("5641aa72aef06e0b819e353b")
        }
    ]
}
timeDiffs = [mins(2), mins(4), mins(15), mins(35), mins(35), mins(45), mins(47), mins(56),
        hmin(1, 25), hmin(2, 10), hmin(2, 34), hmin(2, 58), hmin(3, 27), hmin(3, 44), hmin(4, 8),
        hmin(4, 43), hmin(5, 05), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 42), hmin(6, 47),
        hmin(6, 48), hmin(6, 52), hmin(7, 27), hmin(8, 04), hmin(9, 14), hmin(9, 18), hmin(9, 25),
        hmin(9, 29), hmin(10, 07), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 16), hmin(13, 18), hmin(13, 20), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 42), hmin(14, 48), hmin(14, 53),
        hmin(15, 13), hmin(15, 18), hmin(15, 34), hmin(15, 46), hmin(15, 52), hmin(16, 10),
        hmin(16, 34), hmin(16, 50), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 07), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 13), hmin(19, 31),
        hmin(19, 38), hmin(19, 49), hmin(19, 55), hmin(19, 59), hmin(20, 10), hmin(20, 17),
        hmin(20, 29), hmin(20, 38), hmin(20, 53), hmin(21, 13), hmin(21, 33), hmin(21, 41),
        hmin(22, 29), hmin(22, 58), hmin(23, 02), hmin(23, 14), hmin(23, 36)]
line3 = [baseEntry]
line3IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line3.append(entry)
    line3IDs.append(tripID)

################### line 103 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 10,
    "line" : 103,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 38),
    "capacity" : 60,
    "trajectory" : [
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
            "busStop" : ObjectId("5641aa72aef06e0b819e353b")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
            "busStop" : ObjectId("5641aa72aef06e0b819e353a")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 03),
            "busStop" : ObjectId("5641aa72aef06e0b819e3539")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05),
            "busStop" : ObjectId("5641aa72aef06e0b819e3538")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("5641aa72aef06e0b819e3537")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 07),
            "busStop" : ObjectId("5641aa72aef06e0b819e3536")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8),
            "busStop" : ObjectId("5641aa72aef06e0b819e3535")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 9),
            "busStop" : ObjectId("5641aa72aef06e0b819e3534")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 11),
            "busStop" : ObjectId("5641aa72aef06e0b819e3533")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 12),
            "busStop" : ObjectId("56321850aef06e1027122095")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 13),
            "busStop" : ObjectId("56321850aef06e1027122094")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 14),
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 15),
            "busStop" : ObjectId("56321850aef06e1027122092")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 16),
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18),
            "busStop" : ObjectId("56321850aef06e1027122090")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 19),
            "busStop" : ObjectId("56321850aef06e102712208f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 20),
            "busStop" : ObjectId("56321850aef06e102712208e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 22),
            "busStop" : ObjectId("56321850aef06e102712208d")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 24),
            "busStop" : ObjectId("562a07c473b23914826f047d")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 27),
            "busStop" : ObjectId("562a07c473b23914826f047c")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 29),
            "busStop" : ObjectId("562a07c473b23914826f047b")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 31),
            "busStop" : ObjectId("5641aa72aef06e0b819e3532")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 32),
            "busStop" : ObjectId("5641aa72aef06e0b819e3531")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 34),
            "busStop" : ObjectId("5641aa72aef06e0b819e3530")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 36),
            "busStop" : ObjectId("5641aa72aef06e0b819e352f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 37),
            "busStop" : ObjectId("5641aa72aef06e0b819e352e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 38),
            "busStop" : ObjectId("5641aa72aef06e0b819e352d")
        }
    ]
}
timeDiffs = [mins(2), mins(11), mins(15), mins(35), mins(35), mins(45), mins(47), mins(56),
        hmin(2, 25), hmin(2, 30), hmin(2, 54), hmin(2, 58), hmin(3, 37), hmin(3, 44), hmin(4, 8),
        hmin(4, 43), hmin(5, 25), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 42), hmin(6, 47),
        hmin(6, 48), hmin(6, 52), hmin(7, 27), hmin(8, 04), hmin(9, 14), hmin(9, 18), hmin(9, 25),
        hmin(9, 29), hmin(10, 27), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 16), hmin(13, 18), hmin(13, 20), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 42), hmin(14, 48), hmin(14, 53),
        hmin(15, 13), hmin(15, 18), hmin(15, 27), hmin(15, 36), hmin(15, 52), hmin(16, 0),
        hmin(16, 24), hmin(16, 50), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 18), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 03), hmin(19, 11),
        hmin(19, 28), hmin(19, 40), hmin(19, 51), hmin(19, 59), hmin(20, 10), hmin(20, 21),
        hmin(20, 29), hmin(20, 35), hmin(20, 48), hmin(21, 13), hmin(21, 22), hmin(21, 41),
        hmin(22, 29), hmin(22, 58), hmin(23, 05), hmin(23, 19), hmin(23, 48)]
line103 = [baseEntry]
line103IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line103.append(entry)
    line103IDs.append(tripID)

################### line 5 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 12,
    "line" : 5,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 10),
    "capacity" : 60,
    "trajectory" : [
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2a")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 03),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2b")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 04),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2c")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2d")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 7),
            "busStop" : ObjectId("568bdb7daef06e0dab282d3a")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8),
            "busStop" : ObjectId("568bdb7daef06e0dab282d3b")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 10),
            "busStop" : ObjectId("562a07c473b23914826f0487")
        }
    ]
}
timeDiffs = [mins(2), mins(20), mins(45), hmin(9, 35), hmin(12, 45), hmin(8, 0), hmin(16, 12), hmin(7, 30),
        hmin(2, 25), hmin(2, 30), hmin(2, 54), hmin(8, 35), hmin(8, 20), hmin(3, 44), hmin(4, 8),
        hmin(4, 43), hmin(5, 25), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 37), hmin(6, 47),
        hmin(6, 59), hmin(7, 15), hmin(7, 40), hmin(8, 45), hmin(9, 14), hmin(9, 18), hmin(9, 40),
        hmin(9, 59), hmin(10, 17), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 16), hmin(13, 18), hmin(13, 20), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 42), hmin(14, 48), hmin(14, 53),
        hmin(15, 13), hmin(15, 18), hmin(15, 27), hmin(15, 36), hmin(15, 52), hmin(16, 0),
        hmin(16, 24), hmin(16, 50), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 18), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 03), hmin(19, 11),
        hmin(19, 28), hmin(19, 40), hmin(19, 51), hmin(19, 59), hmin(20, 10), hmin(20, 21),
        hmin(20, 29), hmin(20, 35), hmin(20, 48), hmin(21, 13), hmin(21, 22), hmin(21, 41),
        hmin(22, 29), hmin(22, 58), hmin(23, 05), hmin(23, 19), hmin(23, 48)]
line5 = [baseEntry]
line5IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line5.append(entry)
    line5IDs.append(tripID)

################### line 105 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 13,
    "line" : 105,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 10),
    "capacity" : 60,
    "trajectory" : [
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 10),
            "busStop" : ObjectId("562a07c473b23914826f0487")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8),
            "busStop" : ObjectId("568bdb7daef06e0dab282d3b")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 7),
            "busStop" : ObjectId("568bdb7daef06e0dab282d3a")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2f")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2e")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2d")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 04),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2c")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 03),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2b")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 01),
            "busStop" : ObjectId("568bdb7daef06e0dab282d2a")
        }
    ]
}
timeDiffs = [mins(2), mins(20), mins(45), hmin(9, 35), hmin(12, 45), hmin(8, 0), hmin(16, 12), hmin(7, 30),
        hmin(2, 25), hmin(2, 30), hmin(2, 54), hmin(8, 35), hmin(8, 20), hmin(3, 44), hmin(4, 8),
        hmin(4, 43), hmin(5, 25), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 37), hmin(6, 47),
        hmin(6, 59), hmin(7, 15), hmin(7, 40), hmin(8, 45), hmin(9, 14), hmin(9, 18), hmin(9, 40),
        hmin(9, 59), hmin(10, 17), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 16), hmin(13, 18), hmin(13, 20), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 42), hmin(14, 48), hmin(14, 53),
        hmin(15, 13), hmin(15, 18), hmin(15, 27), hmin(15, 36), hmin(15, 52), hmin(16, 0),
        hmin(16, 24), hmin(16, 50), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 18), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 03), hmin(19, 11),
        hmin(19, 28), hmin(19, 40), hmin(19, 51), hmin(19, 59), hmin(20, 10), hmin(20, 21),
        hmin(20, 29), hmin(20, 35), hmin(20, 48), hmin(21, 13), hmin(21, 22), hmin(21, 41),
        hmin(22, 29), hmin(22, 58), hmin(23, 05), hmin(23, 19), hmin(23, 48)]
line105 = [baseEntry]
line105IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line105.append(entry)
    line105IDs.append(tripID)

################### line 14 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 44,
    "line" : 14,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 46),
    "capacity" : 60,
    "trajectory" : [ 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
            "busStop" : ObjectId("56321850aef06e102712207f")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 04),
            "busStop" : ObjectId("56321850aef06e1027122080")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05),
            "busStop" : ObjectId("56321850aef06e1027122081")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("56321850aef06e1027122082")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8),
            "busStop" : ObjectId("56321850aef06e1027122083")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 9),
            "busStop" : ObjectId("56321850aef06e1027122084")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 11),
            "busStop" : ObjectId("56321850aef06e1027122085")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 13),
            "busStop" : ObjectId("56321850aef06e1027122086")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 14),
            "busStop" : ObjectId("56321850aef06e1027122087")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 15),
            "busStop" : ObjectId("56321850aef06e1027122088")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 16),
            "busStop" : ObjectId("56321850aef06e1027122089")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 17),
            "busStop" : ObjectId("56321850aef06e102712208a")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18),
            "busStop" : ObjectId("56321850aef06e102712208b")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 19),
            "busStop" : ObjectId("56321850aef06e102712208c")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 21),
            "busStop" : ObjectId("562a07c473b23914826f047e")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 25),
            "busStop" : ObjectId("562a07c473b23914826f047d")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 27),
            "busStop" : ObjectId("56321850aef06e102712208d")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 28),
            "busStop" : ObjectId("56321850aef06e102712208e")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 30),
            "busStop" : ObjectId("56321850aef06e102712208f")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 31),
            "busStop" : ObjectId("56321850aef06e1027122090")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 33),
            "busStop" : ObjectId("56321850aef06e1027122091")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 35),
            "busStop" : ObjectId("56321850aef06e1027122092")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 36),
            "busStop" : ObjectId("56321850aef06e1027122093")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 38),
            "busStop" : ObjectId("56321850aef06e1027122094")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 39),
            "busStop" : ObjectId("56321850aef06e1027122095")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 41),
            "busStop" : ObjectId("56321850aef06e1027122096")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 42),
            "busStop" : ObjectId("56321850aef06e1027122097")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 43),
            "busStop" : ObjectId("56321850aef06e1027122098")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 44),
            "busStop" : ObjectId("56321850aef06e1027122099")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 46),
            "busStop" : ObjectId("56321850aef06e102712209a")
        }
    ]
}
timeDiffs = [mins(2), mins(4), mins(11), mins(15), mins(35), mins(35), mins(45), mins(47), mins(56),
        hmin(2, 25), hmin(2, 30), hmin(2, 54), hmin(2, 58), hmin(3, 37), hmin(3, 44), hmin(4, 8),
        hmin(4, 43), hmin(5, 25), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 42), hmin(6, 47),
        hmin(6, 48), hmin(6, 52), hmin(7, 27), hmin(8, 04), hmin(9, 14), hmin(9, 18), hmin(9, 25),
        hmin(9, 29), hmin(10, 27), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 16), hmin(13, 18), hmin(13, 20), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 42), hmin(14, 48), hmin(14, 53),
        hmin(15, 13), hmin(15, 18), hmin(15, 34), hmin(15, 36), hmin(15, 42), hmin(16, 0),
        hmin(16, 54), hmin(16, 56), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 18), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 03), hmin(19, 41),
        hmin(19, 48), hmin(19, 49), hmin(19, 55), hmin(19, 59), hmin(20, 00), hmin(20, 07),
        hmin(20, 19), hmin(20, 28), hmin(20, 33), hmin(21, 13), hmin(21, 13), hmin(21, 41),
        hmin(22, 29), hmin(22, 58), hmin(23, 02), hmin(23, 04), hmin(23, 16)]
line14 = [baseEntry]
line14IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line14.append(entry)
    line14IDs.append(tripID)

################### line 114 ##################

baseID = ObjectId()
baseEntry = {
    "_id" : baseID,
    "busID" : 44,
    "line" : 114,
    "startTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
    "endTime" : datetime.datetime(YEAR, MONTH, DAY, 00, 46),
    "capacity" : 60,
    "trajectory" : [
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 02),
            "busStop" : ObjectId("56321850aef06e102712209a")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 04),
            "busStop" : ObjectId("56321850aef06e1027122099")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 05),
            "busStop" : ObjectId("56321850aef06e1027122098")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 06),
            "busStop" : ObjectId("56321850aef06e1027122097")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 07),
            "busStop" : ObjectId("56321850aef06e1027122096")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 8),
            "busStop" : ObjectId("56321850aef06e1027122095")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 10),
            "busStop" : ObjectId("56321850aef06e1027122094")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 11),
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 12),
            "busStop" : ObjectId("56321850aef06e1027122092")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 13),
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 15),
            "busStop" : ObjectId("56321850aef06e1027122090")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 16),
            "busStop" : ObjectId("56321850aef06e102712208f")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 18),
            "busStop" : ObjectId("56321850aef06e102712208e")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 19),
            "busStop" : ObjectId("56321850aef06e102712208d")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 21),
            "busStop" : ObjectId("562a07c473b23914826f047d")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 25),
            "busStop" : ObjectId("562a07c473b23914826f047e")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 27),
            "busStop" : ObjectId("56321850aef06e102712208c")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 28),
            "busStop" : ObjectId("56321850aef06e102712208b")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 29),
            "busStop" : ObjectId("56321850aef06e102712208a")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 30),
            "busStop" : ObjectId("56321850aef06e1027122089")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 31),
            "busStop" : ObjectId("56321850aef06e1027122088")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 32),
            "busStop" : ObjectId("56321850aef06e1027122087")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 34),
            "busStop" : ObjectId("56321850aef06e1027122086")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 36),
            "busStop" : ObjectId("56321850aef06e1027122085")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 38),
            "busStop" : ObjectId("56321850aef06e1027122084")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 39),
            "busStop" : ObjectId("56321850aef06e1027122083")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 42),
            "busStop" : ObjectId("56321850aef06e1027122082")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 43),
            "busStop" : ObjectId("56321850aef06e1027122081")
        }, 
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 44),
            "busStop" : ObjectId("56321850aef06e1027122080")
        },
        {
            "time" : datetime.datetime(YEAR, MONTH, DAY, 00, 46),
            "busStop" : ObjectId("56321850aef06e102712207f")
        },
    ]
}
timeDiffs = [mins(2), mins(11), mins(25), mins(35), mins(35), mins(45), mins(47), mins(56),
        hmin(2, 0), hmin(2, 30), hmin(2, 44), hmin(2, 58), hmin(3, 37), hmin(3, 44), hmin(4, 8),
        hmin(4, 43), hmin(5, 25), hmin(5, 31), hmin(5, 48), hmin(6, 22), hmin(6, 42), hmin(6, 47),
        hmin(6, 48), hmin(6, 52), hmin(7, 27), hmin(8, 04), hmin(9, 14), hmin(9, 18), hmin(9, 25),
        hmin(9, 29), hmin(10, 27), hmin(10, 29), hmin(10, 35), hmin(10, 47), hmin(10, 49),
        hmin(11, 23), hmin(11, 38), hmin(11, 55), hmin(11, 56), hmin(11, 56), hmin(12, 02),
        hmin(12, 27), hmin(12, 35), hmin(13, 16), hmin(13, 18), hmin(13, 20), hmin(13, 36),
        hmin(13, 46), hmin(13, 57), hmin(14, 19), hmin(14, 32), hmin(14, 48), hmin(14, 53),
        hmin(15, 13), hmin(15, 18), hmin(15, 34), hmin(15, 36), hmin(15, 42), hmin(16, 0),
        hmin(16, 34), hmin(16, 56), hmin(17, 04), hmin(17, 25), hmin(17, 38), hmin(17, 47),
        hmin(18, 18), hmin(18, 26), hmin(18, 41), hmin(18, 59), hmin(19, 03), hmin(19, 21),
        hmin(19, 38), hmin(19, 49), hmin(19, 55), hmin(19, 59), hmin(20, 10), hmin(20, 17),
        hmin(20, 29), hmin(20, 38), hmin(20, 53), hmin(21, 13), hmin(21, 23), hmin(21, 41),
        hmin(22, 29), hmin(22, 58), hmin(23, 02), hmin(23, 04), hmin(23, 16)]
line114 = [baseEntry]
line114IDs = [baseID]
for diff in timeDiffs:
    tripID = ObjectId()
    entry = {
        "_id" : tripID,
        "line" : baseEntry["line"],
        "startTime" : baseEntry["startTime"] + diff,
        "endTime" : baseEntry["endTime"] + diff,
        "busID" : random.randint(1, 100),
        "trajectory" : []
    }
    for stop in baseEntry["trajectory"]:
        newStop = {
            "time" : stop["time"] + diff,
            "busStop" : stop["busStop"]
        }
        entry["trajectory"].append(newStop)
    line114.append(entry)
    line114IDs.append(tripID)



writeInDB()

