"""
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the 
specific language governing permissions and limitations under the License.
"""
import mutation
import inits
from deap import base
from deap import creator
from deap import tools
from scoop import futures
from dbConnection import DB
from fitness import Fitness
from operator import itemgetter
import datetime
from datetime import timedelta



# Constant
BUS_LINE = 2
DB.noOfslices = 0
# The individual size corresponds to the number of trips
INDIVIDUAL_SIZE =  14
INDIVIDUAL_SIZE_BOUNDS = [30, 90]


# Initialize the classes
databaseClass = DB()
fitnessClass = Fitness()
def generateStartTimeBasedOnFreq(busLine,frequency, startTime):
    # we make sure the starting time is in between the upper and lower bound of our time slices
    startTimeArray = []
    lineTimes = {}
    for x in DB.timeSliceArray:
        start = datetime.datetime.combine(Fitness.yesterday, datetime.time(x[0], 0, 0))
        end = datetime.datetime.combine(Fitness.yesterday, datetime.time(x[1], 59, 59))

        # if the startTime is in a specific time slice
        if start <= startTime <= end:
            NextstartTime = startTime + datetime.timedelta(minutes=frequency)
            NextstartTime2 = startTime - datetime.timedelta(minutes=frequency)
            startTimeArray.append(startTime.time())
            if NextstartTime <= end:
                startTimeArray.append(NextstartTime.time())
            if NextstartTime2 >= start:
                startTimeArray.append(NextstartTime2.time())

            while NextstartTime <= end:

                NextstartTime = NextstartTime + datetime.timedelta(minutes=frequency)
                if NextstartTime <= end:
                    startTimeArray.append(NextstartTime.time())

            while NextstartTime2 >= start:

                NextstartTime2 = NextstartTime2 - datetime.timedelta(minutes=frequency)

                if NextstartTime2 >= start:
                    startTimeArray.append(NextstartTime2.time())

    return startTimeArray


def evaluateNewIndividualFormat(individual):
    individual = sorted(individual, key=itemgetter(3))

    #print("THIS IS AN INDIVIDUAL")
    #print(individual)
    #print("\n")
    #this will be called for each gene in the individual

    busLines = [x[0] for x in individual]
    busLines[:] = set(busLines)
    times = {}
    for line in busLines:
        ind = [x for x in individual if x[0] == line]
        for i, val in enumerate(ind):
            generate = generateStartTimeBasedOnFreq(line,val[2], val[3])
            if line not in times:
                times[line] = generate
            else:
                times[line] = times[line] + generate
                #print "Result starting times....."

    #print sorted(times[2])
    #print sorted(times[102])

    for i, trip in enumerate(times):
        count = 0
        for tr in sorted(times[trip]):
            if datetime.time(0,0,0) <= tr <= datetime.time(6, 0, 0):
                count+=1
                print count
            elif datetime.time(6,0,0) <= tr <= datetime.time(9, 0, 0):
                count+=1
                print count
            elif datetime.time(9,0,0) <= tr <= datetime.time(12, 0, 0):
                count+=1
                print count
            elif datetime.time(12,0,0) <= tr <= datetime.time(15, 0, 0):
                count+=1
                print count
            elif datetime.time(15,0,0) <= tr <= datetime.time(18, 0, 0):
                count+=1
                print count
            elif datetime.time(18,0,0) <= tr <= datetime.time(21, 0, 0):
                count+=1
                print count
            elif datetime.time(21,0,0) <= tr <= datetime.time(23, 59, 59):
                count+=1
                print count
        print "No of trips " + str(len(times[trip]))
        print""

        print "Departure times, line " + str(trip)
        print sorted(times[trip])

# TODO: count the number of trips




    return 1,

""""
    for i in range(len(individual)):
        tripTimeTable = databaseClass.generateFitnessTripTimeTable(individual[i][0], individual[i][2])
        for j in range(len(tripTimeTable)):
            # TODO: Fix trips that finish at the next day
            initialTrip = initialTripTime
            lastTrip = tripTimeTable[j][1]
            if initialTrip > lastTrip:
                initialTrip = lastTrip - timedelta(minutes=db.getFrequency(individual[i][0]))
            # Search on Fitness.request array for the particular requests

            request = fitnessClass.searchRequest(initialTrip, lastTrip, tripTimeTable[j][0])
            initialTripTime = tripTimeTable[j][1]
"""



def evalIndividual(individual):
    ''' Evaluate an individual in the population. Based on how close the
    average bus request time is to the actual bus trip time.

    @param an individual in the population
    @return a summation of the difference between past past requests'
    average trip starting time and actual start time
    according to the evolving timetable.
    Lower values are better.
    '''
    # First, the randomly-generated starting times are sorted in order to check sequentially the number of requests for that particular trip
    individual[:] = [x for x in individual if x[0] == 2]  # choosing only line 2 for now
    individual = sorted(individual, key=itemgetter(3))

    # Second, we loop trough the number of genes in order to retrieve the number of requests for that particular trip
    # For the 1st trip, the starting time has to be selected
    request = []
    dif = []
    cnt = []
    initialTripTime = datetime.datetime.combine(fitnessClass.yesterday, 
                                       datetime.datetime.strptime("00:00", 
                                       fitnessClass.formatTime).time())
    db = DB()
    tripWaitingTime = timedelta(minutes=0) # waiting time due to insufficient capacity
    noOfLeftOvers = 0
    for i, trip in enumerate(individual):
        tripStartTime = trip[3]
        '''
        if len(str(tripStartTime.hour)) == 1:
            temp = "0" + str(tripStartTime.hour) + ":" + str(tripStartTime.minute)
        else:
            temp = str(tripStartTime.hour) + ":" + str(tripStartTime.minute)

        if i == 0:
            start, end = '2015-10-21 00:00:00', '2015-10-21 ' + temp + ':00' 
        else:
            start, end = end, '2015-10-21 ' + temp + ':00'
            '''
        # TODO: Evaluate individual fitness based on how many requests can be handled, increase waiting time for
        # leftover passengers
        tslice = [(x[0], x[1]) for x in timeSlices if x[0].time() <= tripStartTime.time() <= x[1].time()]
        earliestDeparture = tslice[0][0] + timedelta(minutes=trip[2])
        while (earliestDeparture.time() <= tslice[0][1].time()):
            departures.append(earliestDeparture.time())
            earliestDeparture += timedelta(minutes=trip[2])
        #print "earliest possible departure " + str(earliestDeparture.time())
        #print "next departure: " + str(nextDeparture.time())

        #tripCapacity = trip[1]
        #earliestDeparture = '2015-10-21 ' + str(earliestDeparture.time())
        #end = '2015-10-21 ' + departures[len(departures)-1].strftime('%H:%M:%S')
        #print "End..." + str(end)
        '''
        stopsAndRequests = db.MaxReqNumTrip(earliestDeparture, end, 2)
        for j, stop in enumerate(stopsAndRequests):
            requestsAtStop = stop[1]
            if requestsAtStop > tripCapacity and i < len(individual)-1:
                #print "Trip time " + str(tripStartTime)
                nextTripTime = individual[i+1][3]
                nextTripWait = nextTripTime - tripStartTime
                #print "next trip in " + str(nextTripWait.total_seconds()/60.0) + " minutes"
                #print "next trip time: " + str(nextTripTime)
                noOfLeftOvers = noOfLeftOvers + (requestsAtStop - tripCapacity) #must wait for the next bus trip
                tripWaitingTime += nextTripWait*(stop[1] - trip[1])
            else:
                pass

        print "Number left over: " + str(noOfLeftOvers)
        print "total waiting time: " + str(tripWaitingTime.total_seconds()/60.0)
        '''

    '''
    # Evaluate average time
    for i in range(len(individual)):
        tripTimeTable = db.generateFitnessTripTimeTable(individual[i][0], individual[i][2])
        for j in range(len(tripTimeTable)):
            # TODO: Fix trips that finish at the next day
            initialTrip = initialTripTime
            lastTrip = tripTimeTable[j][1]
            if initialTrip > lastTrip:
                initialTrip = lastTrip - timedelta(minutes=db.getFrequency(individual[i][0]))
            # Search on Fitness.request array for the particular requests
            request = fitnessClass.searchRequest(initialTrip, lastTrip, tripTimeTable[j][0])
            initialTripTime = tripTimeTable[j][1]
            if len(request) > 0:
                diff = 0
                count = 0
                for k in range(len(request)):
                    z = tripTimeTable[j][1] - request[k]["_id"]["RequestTime"]
                    diff = diff + (z.days * databaseClass.minutesDay) + (z.seconds / databaseClass.minutesHour)
                    count = count + int(request[k]["total"])
                dif.append(diff)
                cnt.append(count)

    totalWaitingTime = sum(dif) + tripWaitingTime.total_seconds()/60.0
    averageWaitingTime = totalWaitingTime / (sum(cnt) + noOfLeftOvers)
    return fitnessClass.calculateCost(individual, totalWaitingTime, 0),
    '''
    return 1,


# Creating a minimizing fitness class to minimize a single objective that
# inherits from the base class "Fitness".
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Creating an individual class that inherits a list property and has a fitness
# attribute of type FitnessMin
creator.create("Individual", list, fitness=creator.FitnessMin)

# Initialize the toolbox from the base class
toolbox = base.Toolbox()

# Register the operations to be used in the toolbox
toolbox.register("attribute", databaseClass.generateRandomStartingTimeForTrip)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attribute, INDIVIDUAL_SIZE)
#toolbox.register("individual", inits.initRepeatBound, creator.Individual,
#                  toolbox.attribute, INDIVIDUAL_SIZE_BOUNDS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluateNewIndividualFormat)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mutate", mutation.mutUniformTime)
toolbox.register("map", futures.map)
