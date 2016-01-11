import pymongo
import bson
import random
import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient


client = MongoClient()

db = client.monad

YEAR = 2015
MONTH = 10
DAY = 27

print ("Creating timetables...")
new_record1 = {
                  
                  "date": datetime.datetime(YEAR, MONTH, DAY),
                  "line": 10,
                  "timetable": [
                                 {
                                        "routeId":ObjectId(),
                                        "busId": [1],
                                        "busStops": [
                                                    {
                                                        "capacity":20,
                                                        "busstop": "Polacksbacken", 
                                                        "time": datetime.datetime(2015, 10, 28, 14, 45, 0),
                                                        "latitude": 59.840427,
                                                        "longitude": 17.647628
                                                    },
                                                    {
                                                        "capacity":20,
                                                        "busstop": "Gamla Uppsala", 
                                                        "time": datetime.datetime(2015, 10, 28, 14, 55, 0),
                                                        "latitude":59.897172,
                                                        "longitude": 17.636958
                                                    }
                                        ]
                                },
                                {
                                        "routeId":ObjectId(),
                                        "busId": [2],
                                        "busStops": [
                                                    {
                                                        "capacity":20,
                                                        "busstop": "Polacksbacken", 
                                                        "time": datetime.datetime(2015, 10, 28, 15, 45, 0),
                                                        "latitude": 59.840427,
                                                        "longitude": 17.647628
                                                    },
                                                    {
                                                        "capacity":20,
                                                        "busstop": "Gamla Uppsala", 
                                                        "time": datetime.datetime(2015, 10, 28, 15, 55, 0),
                                                        "latitude":59.897172,
                                                        "longitude": 17.636958 
                                                    }
                                        ]
                                },
                                {
                                        "routeId":ObjectId(),
                                        "busId": [555],
                                        "busStops": [
                                                    {
                                                        "capacity":20,
                                                        "busstop": "Polacksbacken", 
                                                        "time": datetime.datetime(2015, 10, 28, 17, 10, 0),
                                                        "latitude": 59.840427,
                                                        "longitude": 17.647628
                                                    },
                                                    {
                                                        "capacity":20,
                                                        "busstop": "Flogsta", 
                                                        "time": datetime.datetime(2015, 10, 28, 17, 45, 0),
                                                        "latitude": 59.851252,
                                                        "longitude": 17.593290
                                                    }
                                        ]
                                },
                                {
                                        "routeId":ObjectId(),
                                        "busId": [888],
                                        "busStops": [
                                                    {
                                                        "capacity":20,
                                                        "busstop": "Flogsta", 
                                                        "time": datetime.datetime(2015, 10, 28, 8, 40, 0),
                                                        "latitude": 59.851252,
                                                        "longitude": 17.593290
                                                    },
                                                    {
                                                        "capacity":20,
                                                        "busstop": "Polacksbacken", 
                                                        "time": datetime.datetime(2015, 10, 28, 9, 05, 0),
                                                        "latitude": 59.840427,
                                                        "longitude": 17.647628
                                                    }
                                        ]
                                }

                            ]
}
new_record2 = {
                 
                  "date": datetime.datetime(YEAR, MONTH, 26),
                  "line": 20,
                  "timetable": [
                                {
                                        "routeId":ObjectId(),
                                        "busId": [2],
                                        "busStops": [
                                                    {   
                                                        "capacity":40,
                                                        "busstop": "flogsta", 
                                                        "time": datetime.datetime(2015, 10, 26, 23, 15, 0),
                                                        "latitude": 27,
                                                        "longitude": 59
                                                    },
                                                    {
                                                        "capacity":40,
                                                        "busstop": "central", 
                                                        "time": datetime.datetime(2015, 10, 26, 23, 45, 0),
                                                        "latitude": 65,
                                                        "longitude": 12
                                                    }
                                        ]
                                },
                                {
                                        "routeId":ObjectId(),
                                        "busId": [23],
                                        "busStops": [
                                                    {
                                                        "capacity":40,
                                                        "busstop": "flogsta", 
                                                        "time": datetime.datetime(2015, 10, 26, 1, 15, 0),
                                                        "latitude": 27,
                                                        "longitude": 59
                                                    },
                                                    {
                                                        "capacity":40,
                                                        "busstop": "central", 
                                                        "time": datetime.datetime(2015, 10, 26, 1, 45, 0),
                                                        "latitude": 65,
                                                        "longitude": 12
                                                    }
                                        ]
                                }

                            ]
}
new_record3 = {
                  
                  "date": datetime.datetime(YEAR, MONTH, 25),
                  "line": 300000,
                  "timetable": [
                                {
                                        "routeId":ObjectId(),
                                        "busId": [3],
                                        "busStops": [
                                                    {
                                                        "capacity":77,
                                                        "busstop": "science park", 
                                                        "time": datetime.datetime(2015, 10, 25, 10, 25, 0),
                                                        "latitude": 10,
                                                        "longitude": 34
                                                    },
                                                    {
                                                        "capacity":77,
                                                        "busstop": "hospital", 
                                                        "time": datetime.datetime(2015, 10, 25, 10, 30, 0),
                                                        "latitude": 15,
                                                        "longitude": 39
                                                    }
                                        ]
                                },
                                {
                                        "routeId":ObjectId(),
                                        "busId": [30],
                                        "busStops": [
                                                    {
                                                        "capacity":77,
                                                        "busstop": "science park", 
                                                        "time": datetime.datetime(2015, 10, 25, 11, 25, 0),
                                                        "latitude": 10,
                                                        "longitude": 34
                                                    },
                                                    {
                                                        "capacity":77,
                                                        "busstop": "hospital", 
                                                        "time": datetime.datetime(2015, 10, 25, 11, 30, 0),
                                                        "latitude": 15,
                                                        "longitude": 39
                                                    }
                                        ]
                                }

                            ]
}
new_record4 = {
                  
                  "date": datetime.datetime(YEAR, MONTH, 24),
                  "line": 40,
                  "timetable": [
                                {
                                      "routeId":ObjectId(),
                                      "busId": [40],
                                      "busStops": [
                                                  {
                                                      "capacity":60,
                                                      "busstop": "carolina", 
                                                      "time": datetime.datetime(2015, 10, 24, 10, 10, 0),
                                                      "latitude": 48,
                                                      "longitude": 59
                                                  },
                                                  {
                                                      "capacity":60,
                                                      "busstop": "stora torget", 
                                                      "time": datetime.datetime(2015, 10, 24, 10, 25, 0),
                                                      "latitude": 13,
                                                      "longitude": 99
                                                  }
                                      ]
                                },
                                {
                                      "routeId":ObjectId(),
                                      "busId": [401],
                                      "busStops": [
                                                  {
                                                      "capacity":60,
                                                      "busstop": "carolina", 
                                                      "time": datetime.datetime(2015, 10, 24, 11, 10, 0),
                                                      "latitude": 48,
                                                      "longitude": 59
                                                  },
                                                  {
                                                      "capacity":60,
                                                      "busstop": "stora torget", 
                                                      "time": datetime.datetime(2015, 10, 24, 11, 25, 0),
                                                      "latitude": 13,
                                                      "longitude": 99
                                                  }
                                      ]
                                }

                            ]
}
db.TimeTableNew.insert_many([new_record1,new_record2,new_record3,new_record4])
'''db.TimeTableNew.insert(new_record1)   
db.TimeTableNew.insert(new_record2)
db.TimeTableNew.insert(new_record3)
db.TimeTableNew.insert(new_record4)'''

      
print ("Done.")