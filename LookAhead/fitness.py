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
from datetime import datetime
from datetime import timedelta
from datetime import date


class Fitness():

    # Main [class] variables
    diffMinutes = 0
    formatString = '%d-%m-%Y %H:%M'
    formatTime = '%H:%M'
    secondMinute = 60.0
    firstMinute = "00:00"
    lastMinute = "23:59"
    requests = []
    routes = []
    request = []
    requestIndex = []
    yesterday = date.today() - timedelta(8)

# A decorator is a function that can accept another function as
# a parameter to be able to modify or extend it
    def decorator(afunction):
        # A wrapper function is used to wrap functionalites you want around the original function
        def wrapper(*args):
            # Checks whether or not the original function as been executed once
            if not wrapper.has_run:
                wrapper.has_run = True
                return afunction(*args)

        wrapper.has_run = False
        return wrapper

    @decorator
    def runOnce(self):
        db = DB()

        # Setting the start time boundary of request that we want
        startTime = datetime.combine(Fitness.yesterday, datetime.strptime(Fitness.firstMinute, Fitness.formatTime).time())
        # Setting the end time boundary of request that we want
        endTime = datetime.combine(Fitness.yesterday, datetime.strptime(Fitness.lastMinute, Fitness.formatTime).time())
        Fitness.request = db.getTravelRequestSummary2(startTime, endTime)

        self.createRequestIndex(Fitness.request)


    def timeDiff(self, time1, time2):
        ''' Evaluates the difference between two times.

        Args: time1 and time2 in datetime format, time1 > time2
        Returns: the timedelta between time1 and time2.
        '''
        return datetime.strptime(time1, Fitness.formatTime) - datetime.strptime(time2, Fitness.formatTime)

    def getMinutes(self, td):
        return (td.seconds//Fitness.secondMinute) % Fitness.secondMinute

    def createRequestIndex(self, request):
        ''' Creates a structure that stores the hour, the minute and the position on the request array for this particular time
        
        @param: request (array): Structure that stores the requests grouped by bus stop, hour and minute. It also includes a COUNT column
        '''
        minute = 0

        for i in range(len(request)):
            #print(request[1]["_id"]["RequestTime"].hour)
            if request[i]["_id"]["RequestTime"].minute != minute or i == 0:
                Fitness.requestIndex.append([request[i]["_id"]["RequestTime"].hour, request[i]["_id"]["RequestTime"].minute, i])
                minute = request[i]["_id"]["RequestTime"].minute

    def searchRequestIndex(self, index, initialHour, initialMinute, finalHour, finalMinute):
        ''' Search the index to get the position on the request array for a specific time frame
        
        @param: index (array): Structure that stores hour, minute and the request's array position for this time
        @param: initialHour (int): Initial hour to perform the search over the index
        @param: initialMinute (int): Final minute to perform the search over the index
        @param: finalHour (int): Final hour to perform the search over the index
        @param: finalMinute (int): Final minute to perform the search over the index
        '''
        result = []
        for i in range(len(index)):
            if index[i][0] == initialHour and index[i][1] == initialMinute:
                result.append(index[i][2])
                break
        # TODO: Watch out with MIDNIGHT trips !!!!
        if len(result) == 0:
            result.append(len(Fitness.request))
        # if result[0] > len(Fitness.request):
        #    result[0] = len(Fitness.request)
        for i in range(i, len(index)):
            if index[i][0] == finalHour and index[i][1] == finalMinute:
                result.append(index[i][2])
                break
        # TODO: Watch out with MIDNIGHT trips !!!!
        if len(result) == 1:
            result.append(len(Fitness.request))
        return result

    def searchRequest(self, initialTime, finalTime, busStop):
        ''' Search on the request array based on an inital time, a final time and a particular bus stop
        
        @param: initialTime (datetime): Initial time to perform the request's search
        @param: finalTime (datetime): Final time to perform the request's search
        @param: busStop (string): Bus stop name used on the request's search
        '''
        result = []
        index = self.searchRequestIndex(Fitness.requestIndex, initialTime.hour, initialTime.minute, finalTime.hour, finalTime.minute)
        request = Fitness.request[index[0]:index[1]]
        for i in range(len(request)):
            if request[i]["_id"]["BusStop"] == busStop:
                result.append(request[i])
        return result

    def evalIndividualCapacity(self, individual):
        ''' Evaluates an individual based on the capacity/bus type chosen for each trip.

        @param: individual - a possible timetable for a bus line, covering the whole day.
        @return: a fitness score assigned in accordance with how close the requested
        capacity is to the availed capacity on the individual
        '''
        individual.sort(key = itemgetter(2))

        db = DB()
        requests = db.getRequestsFromDB()
        requests[:] = [request.time() for request in requests if request is not None]
        fitnessVal = 0 # assumed initial fitness value TODO: put as class variable

        for trip, item in enumerate(individual):
            nrReqs = []
            if trip == 0:
                start = datetime.strptime('00:00', '%H:%M').time()
                end   = datetime.strptime(individual[0][2], '%H:%M').time()
                nrReqs = [i for i in requests if i > start and i <= end]

                # Assign fitness values
                if len(nrReqs) == individual[trip][1]:
                    fitnessVal += 0
                elif len(nrReqs) < individual[trip][1]:
                    fitnessVal += 1
                else:
                    fitnessVal += 1000000
            else:
                start = datetime.strptime(individual[trip-1][2], '%H:%M').time()
                end   = datetime.strptime(individual[trip][2], '%H:%M').time()
                nrReqs = [i for i in requests if i > start and i <= end]

                # Assign fitness values
                if len(nrReqs) == individual[trip][1]:
                    fitnessVal += 0
                elif len(nrReqs) < individual[trip][1]:
                    fitnessVal += 1
                else:
                    fitnessVal += 1000000

        return fitnessVal

    def evalIndividual(self, individual):
        ''' Evaluate an individual in the population. Based on how close the
        average bus request time is to the actual bus trip time.

        @param an individual in the population
        @return a summation of the difference between past past requests'
        average trip starting time and actual start time
        according to the evolving timetable.
        Lower values are better.
        '''
        self.runOnce()

        # Multi thread the MAP functions
        # First, the randomly-generated starting times are sorted in order to check sequentially the number of requests for that particular trip
        individual = sorted(individual, key=itemgetter(2))

        # Second, we loop trough the number of genes in order to retrieve the number of requests for that particular trip
        # For the 1st trip, the starting time has to be selected
        db = DB()
        dif = []
        cnt = []
        intialTripTime = "00:00"

        for i in range(len(individual)):
            tripTimeTable = db.generateFitnessTripTimeTable(individual[i][0], individual[i][2])


            for j in range(len(tripTimeTable)):

                # Search on Fitness.request array for the particular requests
                request = self.searchRequest(datetime.combine(Fitness.yesterday, datetime.strptime(intialTripTime, Fitness.formatTime).time()),
                                             datetime.combine(Fitness.yesterday, datetime.strptime(tripTimeTable[j][1], Fitness.formatTime).time()),
                                             tripTimeTable[j][0])

                intialTripTime = tripTimeTable[j][1]
                if len(request) > 0:
                    diff = 0
                    count = 0
                    for k in range(len(request)):
                        diff = diff + self.getMinutes(self.timeDiff(tripTimeTable[j][1], str(int(request[k]["_id"]["RequestTime"].hour)) + ":" + str(int(request[k]["_id"]["RequestTime"].minute))))*int(request[k]["total"])
                        count = count + int(request[k]["total"])
                    dif.append(diff)
                    cnt.append(count)
        return sum(dif)/sum(cnt),

