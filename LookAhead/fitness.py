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
    yesterday = date.today() - timedelta(13)


# A decorator is a function that can accept another function as
# a parameter to be able to modify or extend it
    def __init__(self):
        self.runOnce()

    def decorator(afunction):
        # A wrapper function is used to wrap functionalites you want around the original function
        def wrapper(*args):
            # Checks whether or not the original function as been executed once
            if not wrapper.has_run:
                wrapper.has_run = True
                return afunction(*args)
            else:
                pass
        wrapper.has_run = False
        return wrapper

    @decorator
    def runOnce(self):
        db = DB()
        # Setting the start time boundary of request that we want
        startTime = datetime.combine(Fitness.yesterday, datetime.strptime(Fitness.firstMinute, Fitness.formatTime).time())
        # Setting the end time boundary of request that we want
        endTime = datetime.combine(Fitness.yesterday, datetime.strptime(Fitness.lastMinute, Fitness.formatTime).time())
        Fitness.request = db.grpReqByBusstopAndTime(startTime, endTime)
        self.createRequestIndex(Fitness.request)

    def timeDiff(self, time1, time2):
        ''' Evaluates the difference between two times.

        Args: time1 and time2 in datetime format, time1 > time2
        Returns: the timedelta between time1 and time2.
        '''
        return datetime.strptime(time1, Fitness.formatTime) - datetime.strptime(time2, Fitness.formatTime)

    def getMinutes(self, td):
        return (td.seconds//Fitness.secondMinute) % Fitness.secondMinute

    def getNumberOfRequests(self, tripStartTime, lineNumber=2):
        ''' finds the max # of transit requests that can be served by the trip with startBusStop along the
        bus line

        @param: tripStartTime - departure time for this trip
        @return maximum number of requests between two stops in the trip
        '''
        self.expectedTimes = {}
        self.stopsCount = {}
        self.reqGroup = []
        print ("routes.....................")
        print (self.routes)
        for i, item in enumerate(self.routes):
            if item[2] == 2:
                self.busStops = [[i[0], i[1]] for i in self.routes[i][1]]
                self.expTime = tripStartTime;
                for i, stop in enumerate(self.busStops):
                    self.expectedTimes[stop[0]] = self.expTime.time()
                    self.expTime = self.expTime + timedelta(minutes=stop[1])
                    self.stopsCount[stop[0]] = 0

        for req in self.requests:
            if req[1] in self.expectedTimes:
                if req[0].time() < self.expectedTimes[req[1]]:
                    self.reqGroup.append(req)
                    self.stopsCount[req[1]] += 1
                    self.stopsCount[req[2]] -= 1

        #print "Max request count", self.stopsCount[max(self.stopsCount, key = self.stopsCount.get)]
        return self.stopsCount[max(self.stopsCount, key = self.stopsCount.get)]

    def createRequestIndex(self, request):
        ''' Creates a structure that stores the hour, the minute and the position on the request array for this particular time
        
        @param: request (array): Structure that stores the requests grouped by bus stop, hour and minute. It also includes a COUNT column
        '''
        minute = 0
        for i in range(len(request)):
            if request[i]["_id"]["RequestTime"].minute != minute or i == 0:
                Fitness.requestIndex.append([request[i]["_id"]["RequestTime"].hour, request[i]["_id"]["RequestTime"].minute, i])
                minute = request[i]["_id"]["RequestTime"].minute
               # minute = request[i]["minute"]
        print(Fitness.requestIndex)
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
            if index[i][0] >= initialHour and index[i][1] >= initialMinute:
                result.append(index[i][2])
                break
        # TODO: Watch out with MIDNIGHT trips !!!!
        if len(result) == 0:
            result.append(len(Fitness.request))
        for i in range(i, len(index)):
            if index[i][0] >= finalHour and index[i][1] >= finalMinute:
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

    def calculateCost(self, individual, totalWaitingTime, penaltyOverCapacity):
        ''' Calculate cost for an individual in the population. 

        @param  individual: individual in the population; 
                averageWaitingTime: average waiting time for that individual
                penaltyOverCapacity: a positive integer to represent a large cost to individual if capacity cannot handle all request of that trip
        @return cost: positive integer for this individual, if input param is out of range, cost will be -1

        Less cost, better individual
        Assume one minute's waiting per person equals to 1kr
        '''
        cost = 0
        costOfBus = [[20, 1000], [60, 1200], [120, 1400]]
        waitingCostPerMin = 1
        busCost = 0
        if penaltyOverCapacity < 0 or individual is None or totalWaitingTime < 0:
            cost = -1
        else:
            for i in range(len(individual)):
                busCapacity = individual[i][1]
                for j in range(len(costOfBus)):
                    if busCapacity == costOfBus[j][0]:
                        busCost = busCost + costOfBus[j][1]
                        break
            waitingCost = totalWaitingTime * waitingCostPerMin
            cost = busCost + waitingCost + penaltyOverCapacity
        return cost
