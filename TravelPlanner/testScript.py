# -*- coding: utf-8 -*-
# Testing Instructions
# Required files: testScript.py (this), testsuite.py, test_planner.py, planner.py
# Also required is a database setup according to the description in the report.
# A test setup can be achieved by running the scripts from the "db-test" folder.
# Do this in the following order: busstops, routes, timetable, busTrips
# If a database setup is established, the test can be executed by simply running this file.
# Specific information about the timing is presented if "profiling" is set to True 

from testsuite import tester
from planner import Mode
import datetime

# Note: Change the date to one the database contains
def timeGen10(h, m):
    return datetime.datetime(2015, 11, 10, h, m)
def timeGen11(h, m):
    return datetime.datetime(2015, 11, 11, h, m)

test = tester()

start1 = "Centralstationen"
start2 = "Topeliusgatan"
start3 = "Studentstaden"
start4 = "Stenhagenskolan"
start5 = "Arrheniusplan"
end1 = "Akademiska sjukhuset"
end2 = "Garnisonen"
end3 = "Rosendals skola"
end4 = "Flogsta centrum"
end5 = "Djursjukhuset"
end6 = "Polacksbacken"
end7 = "Stenhagenskolan"
time1 = timeGen10(10, 13)
time2 = timeGen11(16, 15)
timeArr = Mode.arrivalTime
timeSta = Mode.startTime
trip = Mode.tripTime
profiling = False


json3 = test.test(start1, end1, time1, timeArr, trip, profiling)
test.printJson(json3)

json3 = test.test(start1, end2, time1, timeSta, trip, profiling)
test.printJson(json3)

json4 = test.test(start2, end3, time2, timeArr, trip, profiling)
test.printJson(json4)

json5 = test.test(start1, end4, time1, timeSta, trip, profiling)
test.printJson(json5)

json1 = test.test(start3, end5, time2, timeArr, trip, profiling)
test.printJson(json1)

json5 = test.test(start2, end6, time2, timeSta, trip, profiling)
test.printJson(json5)

json3 = test.test(start4, end6, time1, timeArr, trip, profiling)
test.printJson(json3)

json3 = test.test(start5, end7, time2, timeSta, trip, profiling)
test.printJson(json3)

