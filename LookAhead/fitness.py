#11 -*- coding: utf-8 -*-
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
from datetime import datetime
import datetime
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
    requestOut = []
    requestIndexOut = []
    totalRequestsBusline = {}
    # yesterday = date.today() - timedelta(13)

    yesterdayDate = datetime.datetime.now() - timedelta(1)
    yesterday = datetime.datetime(yesterdayDate.year, yesterdayDate.month, yesterdayDate.day)


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
        startTime = datetime.datetime.combine(Fitness.yesterday, datetime.datetime.strptime(Fitness.firstMinute, Fitness.formatTime).time())
        endTime = datetime.datetime.combine(Fitness.yesterday, datetime.datetime.strptime(Fitness.lastMinute, Fitness.formatTime).time())
        # Create index for the people going on the bus
        Fitness.request = db.grpReqByBusstopAndTime(startTime, endTime)
        self.createRequestIndex(Fitness.request)
        # Create index for the people going down the bus
        Fitness.requestOut = db.getReqCountByEndBusStop(startTime, endTime)
        self.createRequestIndexOut(Fitness.requestOut)
        '''
        # Functions for new encoding including multiple line
        busLines = set(db.busLine)
        for line in busLines:
            for x in db.timeSliceArray:
                start = datetime.datetime.combine(Fitness.yesterday,datetime.time(x[0], 0, 0))
                end = datetime.datetime.combine(Fitness.yesterday, datetime.time(x[1], 59, 59))
                requestBetweenTimeSlices = db.getTravelRequestBetween(start, end, line)
                for count in enumerate(requestBetweenTimeSlices, start=1):
                    countingNoOfRequest = (count[0])
                finalNoReqBetweenTimeSlice = countingNoOfRequest
                Fitness.totalRequestsBusline[(line, start, end)] = finalNoReqBetweenTimeSlice
        print Fitness.totalRequestsBusline
        '''

    def search(self, initialTime, NextTime, BusStop, Line):
        res = []
        counting = 0
        for match in Fitness.request:
            if initialTime <= match["_id"]["RequestTime"] <= NextTime and match["_id"]["line"]==Line and match["_id"]["BusStop"] == BusStop:
                counting+=1
                res.append(match)
                if match["total"] > 1:
                    counting += match["total"]-1
        return res, counting

    def search(self, initialTime, NextTime, BusStop, Line):
        ''' what does it do?
        '''
        res = []
        for match in Fitness.request:
            if (initialTime <= match["_id"]["RequestTime"] <= NextTime) and (match["_id"]["line"] == Line and 
                match["_id"]["BusStop"] == BusStop):
                    res.append(match)
        return res 

    def timeDiff(self, time1, time2):
        ''' Evaluates the difference between two times.

        Args: time1 and time2 in datetime format, time1 > time2
        Returns: the timedelta between time1 and time2.
        '''
        return datetime.strptime(time1, Fitness.formatTime) - datetime.strptime(time2, Fitness.formatTime)

    def getMinutes(self, td):
        return (td.seconds//Fitness.secondMinute) % Fitness.secondMinute

    def getMinutesFromTimedelta(td):
        return (td.seconds//60) % 60

    def createRequestIndex(self, request):
        ''' Creates a structure that stores the hour, the minute and the position on the request array for this particular time
        
        @param: request (array): Structure that stores the requests grouped by bus stop, hour and minute. It also includes a COUNT column
        '''
        # requestTime = 0
        Fitness.requestIndex.append([request[0]["_id"]["RequestTime"], 0])
        requestTime = request[0]["_id"]["RequestTime"]
        for i in range(1, len(request)):
            if request[i]["_id"]["RequestTime"] != requestTime:
                # Fitness.requestIndex.append([request[i]["_id"]["RequestTime"].day, request[i]["_id"]["RequestTime"].hour, request[i]["_id"]["RequestTime"].minute, i])
                Fitness.requestIndex.append([request[i]["_id"]["RequestTime"], i])
                requestTime = request[i]["_id"]["RequestTime"]

    def searchRequest(self, initialTime, finalTime, busStop, line):
        ''' Search on the request array based on an inital time, a final time and a particular bus stop

        @param: initialTime (datetime): Initial time to perform the request's search
        @param: finalTime (datetime): Final time to perform the request's search
        @param: busStop (string): Bus stop name used on the request's search
        '''
        result = []
        index = self.searchRequestIndex(Fitness.requestIndex, initialTime, finalTime)
        if index != False:
            request = Fitness.request[index[0]:index[1]]
            for i in range(len(request)):
                if request[i]["_id"]["BusStop"] == busStop and request[i]["_id"]["line"] == line:
                    result.append(request[i])
        return result

    def searchRequestIndex(self, index, initialDate, finalDate):
        ''' Search the index to get the position on the request array for a specific time frame
        
        @param: index (array): Structure that stores hour, minute and the request's array position for this time
        @param: initialHour (int): Initial hour to perform the search over the index
        @param: initialMinute (int): Final minute to perform the search over the index
        @param: finalHour (int): Final hour to perform the search over the index
        @param: finalMinute (int): Final minute to perform the search over the index
        '''
        result = []
        position = 0
        test = True
        # Look for the first index on the search
        for i in range(len(index)):
            if index[i][0] >= initialDate and index[i][0] < finalDate:
                result.append(index[i][1])
                indexDate = index[i][0]
                position = i
                break
            if index[i][0] >= finalDate:
                break
        if len(result) == 0:
            test = False
        # Evaluate if the first index was found
        if test:
            # If found, look for the second index, however the index has to go backwards
            for j in reversed(range(position, len(index))):
                if index[j][0] > indexDate and index[j][0] <= finalDate:
                    result.append(index[j][1])
                    break
                if index[j][0] <= indexDate:
                    break
            if len(result) == 1:
                test = False
        # Check if both values were generated, if not return an array with false values
        if test:
            return result

        else:
            return False

    def createRequestIndexOut(self, request):
        ''' Creates a structure that stores the hour, the minute and the position on the request array for this particular time

        @param: request (array): Structure that stores the requests grouped by bus stop, hour and minute. It also includes a COUNT column
        '''
        Fitness.requestIndexOut.append([request[0]["_id"]["endTime"], 0])
        requestTime = request[0]["_id"]["endTime"]
        for i in range(1, len(request)):
            if request[i]["_id"]["endTime"] != requestTime:
                Fitness.requestIndexOut.append([request[i]["_id"]["endTime"], i])
                requestTime = request[i]["_id"]["endTime"]

    def searchRequestOut(self, initialTime, finalTime, busStop, line):
        ''' Search on the request array based on an inital time, a final time and a particular bus stop

        @param: initialTime (datetime): Initial time to perform the request's search
        @param: finalTime (datetime): Final time to perform the request's search
        @param: busStop (string): Bus stop name used on the request's search
        '''
        result = []
        index = self.searchRequestIndex(Fitness.requestIndexOut, initialTime, finalTime)
        if index != False:
            request = Fitness.requestOut[index[0]:index[1]]
            for i in range(len(request)):
                if request[i]["_id"]["busStop"] == busStop and request[i]["_id"]["line"] == line:
                    result.append(request[i])
        return result

    def calculateCost(self, individual, totalWaitingTime, penaltyOverCapacity):
        ''' Calculate cost for an individual in the population. 

        @param  individual: individual in the population; 
                totalWaitingTime: total waiting time for that individual
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
        # return cost
        return waitingCost

    def generateStartTimeBasedOnFreq(self, busLine, capacity, frequency, startTime):
        """ Generate all the trips within a time slice given a single starting time
        
        Args: 
             busLine: an integer representing the bus line ID
             frequency: the headway in minutes between successive buses
             startTime: a datetime object representing the start time within the time slice
        
        Return: 
             an array containing all the starting times for the bus trips within the corresponding time slice.
        """
        # we make sure the starting time is in between the upper and lower bound of our time slices
        startTimeArray = []
        lineTimes = {}
        for x in DB.timeSliceArray:
            start = datetime.datetime.combine(Fitness.yesterday, datetime.time(x[0], 0, 0))
            end = datetime.datetime.combine(Fitness.yesterday, datetime.time(x[1], 59, 59))
            if start <= startTime <= end:
                nextStartTime = startTime + datetime.timedelta(minutes=frequency)
                nextStartTime2 = startTime - datetime.timedelta(minutes=frequency)
                startTimeArray.append([startTime, capacity])
                if nextStartTime <= end:
                    startTimeArray.append([nextStartTime, capacity])
                if nextStartTime2 >= start:
                    startTimeArray.append([nextStartTime2, capacity])
                while nextStartTime <= end:
                    nextStartTime = nextStartTime + datetime.timedelta(minutes=frequency)
                    if nextStartTime <= end:
                        startTimeArray.append([nextStartTime, capacity])
                while nextStartTime2 >= start:
                    nextStartTime2 = nextStartTime2 - datetime.timedelta(minutes=frequency)
                    if nextStartTime2 >= start:
                        startTimeArray.append([nextStartTime2, capacity])
        return sorted(startTimeArray) 

    def genTimetable(self, individual):
        """ Generate a timetable for the whole day, for all the bus lines."""

        timetable = {}
        counter = 0
        busLines = set([x[0] for x in individual])
        for line in busLines:
            ind = [y for y in individual if y[0] == line]
            for i, val in enumerate(ind):
                counter+=1
                generate = self.generateStartTimeBasedOnFreq(line, val[1], val[2], val[3])

                if line not in timetable:
                    timetable[line] = generate
                else:
                    timetable[line] = timetable[line] + generate

        timetable = sorted(timetable.items(), key = lambda e: e[0])
        ttLines = []
        for i, item in enumerate(timetable):
            for trip in item[1]:
                ttLines.append([item[0], trip[1], trip[0]])
                    #print trip
        #print sorted(timetable.items(), key = lambda e: e[0])

        return ttLines

    def getTimeSlice(self, startTime):
        ''' Evaluates the time slice a given starting time in a gene belongs to.
        @ param startTime datetime
        @ return (start, end) datetime.datetime objects
        '''
        startTimeArray = []
        for x in DB.timeSliceArray:
            start = datetime.datetime.combine(Fitness.yesterday, datetime.time(x[0], 0, 0))
            end = datetime.datetime.combine(Fitness.yesterday, datetime.time(x[1], 59, 59))
            if start <= startTime <= end:
                return start
