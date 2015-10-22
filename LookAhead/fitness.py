# -*- coding: utf-8 -*-
"""
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

"""
import unittest
from dbConnection import DB
from operator import itemgetter
from datetime import datetime, timedelta
from operator import itemgetter
import bson
from bson import json_util
import json


class Fitness():

    # Main [class] variables
    diffMinutes = 0
    formatString = '%d-%m-%Y %H:%M'
    secondMinute = 60.0

    def timeDiff(self, time1, time2):
        ''' Evaluates the difference between two times.

        Args: time1 and time2 in datetime format, time1 > time2
        Returns: the timedelta between time1 and time2.
        '''
        return datetime.strptime(time1, Fitness.formatString) - datetime.strptime(time2, Fitness.formatString)

    def getMinutes(self, td):
        return (td.seconds//Fitness.secondMinute) % Fitness.secondMinute

    def evalIndividual(self, individual):
        #print(sorted(individual, key = itemgetter(2)))

        """
        dataFile = open("data.bson", "w")

        databaseClass = DB()
        cursor = databaseClass.db.TravelRequest.find({}, {'_id': False})

        for document in cursor:

            json.dump(document, dataFile, default=json_util.default)

            dataFile.write(",\n")

        dataFile.close()
        """

        ''' Evaluate an individual in the population. Based on how close the
        average bus request time is to the actual bus trip time.

        @param an individual in the population
        @return a summation of the difference between past past requests'
        average trip starting time and actual start time
        according to the evolving timetable.
        Lower values are better.
        '''
        # Store the date on mongo as datetime 
        # Store the requests of the previous day into a JSON file order them by date
        # Group by request query from the file to reduce the number of elements being processed
        # Use map function instead of LOOP
        # Multi thread the MAP functions

        # First, the randomly-generated starting times are sorted in order to check sequentially the number of requests for that particular trip
       # individual = sorted(individual, key=itemgetter(2))
        # Second, we loop trough the number of genes in order to retrieve the number of requests for that particular trip
        # DB calls can ve avoided by querying the whole Request Collection for a particular day
        # For the 1st trip, the starting time has to be selected
        #db = DB()
        # Replace the dates here from yesterday's date
        request = []
        # The result here should be added into a file: the order is by hour, minute and initialBusStop
       # request = db.getTravelRequestSummary(datetime.datetime(2015, 10, 23, 0, 0, 0), datetime.datetime(2015, 10, 23, 23, 59, 59))

        # for i in range(len(individual)-1):
        #     request = []
        #     request = db.getTravelRequestBetween("20-10-2015 "+individual[i][2] ,"20-10-2015 "+individual[i+1][2])
        #     req.append(request.count())
        #     diff = []
        #     for j in range(request.count()):
        #         diff.append(self.getMinutes(self.timeDiff(tripTime,request[j]["StartTime"])))
        #         tripTime = "20-10-2015 "+individual[i+1][2]
        #     dif.append([diff])
        # print req
        # print dif
        # Apply a map function to sum all elements of req and diff
        # Then, perform diff / req
        # The result is the value of the fitness function in waiting minutes

        # The least and most possible time timedelta values
        # timeDelta = timeDiff(individual[0][2], individual[0][2])
        '''
        minDiff = timedelta.max
        #diffMinutes = 0
        for reqTime in Fitness.avgBusRequestTime:
            for i in range(len(individual)):
                timeTableDiff = self.timeDiff(individual[i][2], reqTime)
                if timeTableDiff >= timedelta(minutes=0) and timeTableDiff < minDiff:
                    # waitMin = individual[i][2]
                    # index = i
                    minDiff = timeTableDiff
            
            print "Average req time (based on past requests)"
            print reqTime
            print "Best departure time"
            print waitMin
            print "Individual gene"
            print individual[index]
            
            self.diffMinutes += minDiff.total_seconds() / Fitness.secondMinute
            # print diffMinutes
            minDiff = timedelta.max  # Reset minDiff for the next request time
        return self.diffMinutes,
        '''
        return 1 #TODO



# incorporating capacity/no of requests into the fitness function

def evalIndividualCapacity(individual):
    # TODO: pass individual to be evaluated as a paramete
    ''' Evaluates an individual based on the capacity/bus type chosen for each trip.

    @param: individual - a possible timetable for a bus line, covering the whole day.
    @return: a fitness score assigned in accordance with how close the requested
    capacity is to the availed capacity on the individual
    '''
    db = DB()
    requests = sorted(db.getRequestsFromDB())
    print (requests[0])
    #requests = ['10:28', '10:35', '10:45', '10:51', '10:55', '11:05']
    fitnessVal = 0 # assumed initial fitness value TODO: put as class variable
    for trip in range(len(individual)):
        nrReqs = []
        if trip == 0:
            start = datetime.strptime('00:00', '%H:%M')
            end   = datetime.strptime(individual[0][2], '%H:%M')
            nrReqs = [i for i in requests if (datetime.strptime(i, '%H:%M')) >= start and
                    datetime.strptime(i, '%H:%M') < end]

            # Assign fitness value
            if len(nrReqs) == individual[0][1]:
                fitnessVal += 0
            elif len(nrReqs) < individual[0][1]:
                fitnessVal += 1
            else:
                fitnessVal += 1000
        else:
            start = datetime.strptime(individual[trip-1][2], '%H:%M')
            end   = datetime.strptime(individual[trip][2], '%H:%M')
            nrReqs = [i for i in requests if (datetime.strptime(i, '%H:%M')) >= start and
                    datetime.strptime(i, '%H:%M') < end]

            # Assign fitness value
            if len(nrReqs) == individual[0][1]:
                fitnessVal += 0
            elif len(nrReqs) < individual[0][1]:
                fitnessVal += 1
            else:
                fitnessVal += 1000

    return fitnessVal



