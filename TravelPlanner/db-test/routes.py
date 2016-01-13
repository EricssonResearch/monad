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
DATE  = datetime.datetime(YEAR, MONTH, DAY)

client = MongoClient()
db = client.monad

def writeToDB():
    print('Do you really want to change the Routes collection on ' + str(client) + '? ')
    sys.stdin.read(1)
    db.Route.insert_many(line1_101)
    db.Route.insert_many(line2_102)
    db.Route.insert_many(line3_103)
    db.Route.insert_many(line5_105)
    db.Route.insert_many(line14_114)
    return


line1_101 = [{
    "_id" : ObjectId(),
    "duration" : 21,
    "line" : 1,
    "frequency" : 15,
    "date" : DATE,
    "trajectory" : [
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208d")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712208e")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122090")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122092")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed1e")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed1f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed20")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed21")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5640a09273b239624322ed22")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed23")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed24")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5640a09273b239624322ed25")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed26")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed27")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed28")
        }
    ]
},
{
    "_id" : ObjectId(),
    "duration" : 21,
    "line" : 101,
    "frequency" : 15,
    "date" : DATE,
    "trajectory" : [
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed28")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed27")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed26")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed25")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5640a09273b239624322ed24")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed23")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed22")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5640a09273b239624322ed21")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed20")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5640a09273b239624322ed1f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5640a09273b239624322ed1e")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122092")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122090")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208e")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208d")
        }
    ]
}]

line2_102 = [
{
    "_id" : ObjectId(),
    "duration" : 37,
    "date" : DATE,
    "line" : 102,
    "trajectory" : [ 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f048b")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f048a")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0489")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0488")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0487")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0486")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0485")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("562a07c473b23914826f0484")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0483")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0482")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0481")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0480")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047f")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047e")
        }, 
        {
            "interval" : 4,
            "busStop" : ObjectId("562a07c473b23914826f047d")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("562a07c473b23914826f047c")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f047b")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f047a")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0479")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0478")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0477")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0476")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0475")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0474")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0473")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0472")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0471")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0470")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f046f")
        }
    ]
},
{
    "_id" : ObjectId(),
    "duration" : 38,
    "date" : DATE,
    "line" : 2,
    "trajectory" : [ 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f046f")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0470")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0471")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0472")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0473")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0474")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0475")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0476")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0477")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0478")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0479")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f047a")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f047b")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("562a07c473b23914826f047c")
        }, 
        {
            "interval" : 4,
            "busStop" : ObjectId("562a07c473b23914826f047d")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047e")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047f")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0480")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0481")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0482")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0483")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("562a07c473b23914826f0484")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0485")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0486")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0487")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f0488")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0489")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f048a")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("562a07c473b23914826f048b")
        }
    ]
}]

line3_103 = [{
    "_id" : ObjectId(),
    "duration" : 37,
    "line" : 3,
    "date" : DATE,
    "trajectory" : [
        {
            "interval" : 0,
            "busStop" : ObjectId("5641aa72aef06e0b819e352d")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e352e")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e352f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3530")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e3531")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e3532")
        },
        {
            "interval" : 3,
            "busStop" : ObjectId("562a07c473b23914826f047b")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047c")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047d")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208d")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208e")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712208f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122090")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122092")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122094")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122095")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3533")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3534")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3535")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3536")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e3537")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3538")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3539")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e353a")
        },
        {
            "interval" : 0,
            "busStop" : ObjectId("5641aa72aef06e0b819e353b")
        }
    ]
},
{
    "_id" : ObjectId(),
    "duration" : 37,
    "line" : 103,
    "frequency" : 15,
    "date" : DATE,
    "trajectory" : [
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e353b")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e353a")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3539")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e3538")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3537")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3536")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3535")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3534")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e3533")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122095")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122094")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122093")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122092")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122091")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122090")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208e")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712208d")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047d")
        },
        {
            "interval" : 3,
            "busStop" : ObjectId("562a07c473b23914826f047c")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047b")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e3532")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e3531")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e3530")
        },
        {
            "interval" : 2,
            "busStop" : ObjectId("5641aa72aef06e0b819e352f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("5641aa72aef06e0b819e352e")
        },
        {
            "interval" : 0,
            "busStop" : ObjectId("5641aa72aef06e0b819e352d")
        }
    ]
}]

line5_105 = [
{
    "_id" : ObjectId(),
    "duration" : 9,
    "date" : DATE,
    "line" : 5,
    "trajectory" : [ 
        {
            "interval" : 2,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2a")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2b")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2c")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2d")
        },
        {
            "interval" : 0,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2e")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d3a")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d3b")
        },
        {
            "interval" : 0,
            "busStop" : ObjectId("562a07c473b23914826f0487")
        }
    ]
},
{
    "_id" : ObjectId(),
    "duration" : 9,
    "date" : DATE,
    "line" : 105,
    "trajectory" : [
        {
            "interval" : 1,
            "busStop" : ObjectId("562a07c473b23914826f0487")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d3b")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d3a")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2f")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2e")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2d")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2c")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2b")
        },
        {
            "interval" : 0,
            "busStop" : ObjectId("568bdb7daef06e0dab282d2a")
        }
    ]
}]

line14_114 = [{
    "_id" : ObjectId(),
    "duration" : 44,
    "line" : 14,
    "frequency" : 15,
    "date" : DATE,
    "trajectory" : [ 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712207f")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122080")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122081")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122082")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122083")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122084")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122085")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122086")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122087")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122088")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122089")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208a")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208b")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("56321850aef06e102712208c")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047e")
        }, 
        {
            "interval" : 4,
            "busStop" : ObjectId("562a07c473b23914826f047d")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712208d")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208e")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712208f")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122090")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122091")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("56321850aef06e1027122092")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122093")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122094")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122095")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122096")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122097")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122098")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122099")
        },
        {
            "interval" : 0,
            "busStop" : ObjectId("56321850aef06e102712209a")
        }
    ]
},
{
    "_id" : ObjectId(),
    "duration" : 44,
    "line" : 114,
    "frequency" : 15,
    "date" : DATE,
    "trajectory" : [
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712209a")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122099")
        },
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122098")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122097")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122096")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122095")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122094")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122093")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("56321850aef06e1027122092")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122091")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122090")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712208f")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208e")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712208d")
        }, 
        {
            "interval" : 4,
            "busStop" : ObjectId("562a07c473b23914826f047d")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("562a07c473b23914826f047e")
        }, 
        {
            "interval" : 0,
            "busStop" : ObjectId("56321850aef06e102712208c")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208b")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e102712208a")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122089")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122088")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122087")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122086")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122085")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122084")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122083")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122082")
        }, 
        {
            "interval" : 1,
            "busStop" : ObjectId("56321850aef06e1027122081")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e1027122080")
        }, 
        {
            "interval" : 2,
            "busStop" : ObjectId("56321850aef06e102712207f")
        }
    ]
}]

writeToDB()

