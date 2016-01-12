# -*- coding: utf-8 -*-
"""Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

"""
from dbConnection import DB
import datetime
from bson.objectid import ObjectId

# Initialize the classes
databaseClass = DB()

timetable = {
        "BusLine": 2,
        "BusID": 501,
        "StartTime": "04:57",
        "EndTime": "05:51",
        "StartBusStop":"Kungshögarna",
        "EndBusStop": "Säves väg",
        "WayPoints": [
            {
                "BusStop":"Värnlundsgatan",
                "DptTime": "05:01",
                "PsgGetOn": 11,
                "PsgGetOff": 2,
            },
            {
                "BusStop":"Heidenstamstorg",
                "DptTime": "05:04",
                "PsgGetOn": 11,
                "PsgGetOff": 2,
            },
            {
                "BusStop":"Höganäsgatan",
                "DptTime": "05:10",
                "PsgGetOn": 11,
                "PsgGetOff": 2,
            },
            {
                "BusStop":"Stadshuset",
                "DptTime": "05:17",
                "PsgGetOn": 11,
                "PsgGetOff": 2,
            },
            {
                "BusStop":"Studentstaden",
                "DptTime": "05:23",
                "PsgGetOn": 11,
                "PsgGetOff": 2,
            }

        ],
        "DriverID": 3,
        "VehicleID": "UJK123"
    }


def inserttimetable(timetable):
    databaseClass.db.timeTable.insert_one(timetable)



def getTimeTable():
    dataFile = open("timetableResult.txt", "w")
    # find (where , select clause)

    cursor = databaseClass.db.timeTable.find({"_id": ObjectId("561fc48baa47f81faa244d6e")},
                                             {"line": 1, "timetable": 1
                                              })

    for document in cursor:

        dataFile.write(str("This Is The TimeTable for Bus Line " +
                           str(document["line"])+'\n'+'\n'))

        for i in range(len(document["timetable"])):
            dataFile.write("\n")
            for j in range(len(document["timetable"][i]["trip"])):
                dataFile.write(str(document["timetable"][i]["trip"][j]["DptTime"]) + " " +document["timetable"][i]["trip"][j]["BusStop"].encode('utf-8').strip()+"\n")



    dataFile.close()

getTimeTable()



