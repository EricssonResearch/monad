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
from datetime import datetime
from datetime import timedelta



# Constant
BUS_LINE = 2
# The individual size corresponds to the number of trips
# INDIVIDUAL_SIZE =  10
INDIVIDUAL_SIZE_BOUNDS = [30, 90]


# Initialize the classes
databaseClass = DB()
fitnessClass = Fitness()


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
    individual = sorted(individual, key=itemgetter(2))

    # Second, we loop trough the number of genes in order to retrieve the number of requests for that particular trip
    # For the 1st trip, the starting time has to be selected
    request = []
    dif = []
    cnt = []
    initialTripTime = datetime.combine(fitnessClass.yesterday, 
                                       datetime.strptime("00:00", 
                                       fitnessClass.formatTime).time())
    db = DB()
    tripWaitingTime = timedelta(minutes=0) # waiting time due to insufficient capacity
    noOfLeftOvers = 0
    for i, trip in enumerate(individual):
        tripStartTime = trip[2]
        if len(str(tripStartTime.hour)) == 1:
            temp = "0" + str(tripStartTime.hour) + ":" + str(tripStartTime.minute)
        else:
            temp = str(tripStartTime.hour) + ":" + str(tripStartTime.minute)

        if i == 0:
            start, end = '2015-10-21 00:00:00', '2015-10-21 ' + temp + ':00' 
        else:
            start, end = end, '2015-10-21 ' + temp + ':00'

        stopsAndRequests = db.MaxReqNumTrip(start, end)
        for i, stop in enumerate(stopsAndRequests):
            if stop[1] > trip[1] and i < len(individual)-1:
                nextTripTime = individual[i+1][2]
                nextTripWait = nextTripTime - individual[i][2]
                noOfLeftOvers = noOfLeftOvers + (stop[1] - trip[1])   # must wait for the next bus trip
                tripWaitingTime += nextTripWait*(stop[1] - trip[1])

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


# Creating a minimizing fitness class to minimize a single objective that
# inherits from the base class "Fitness".
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Creating an individual class that inherits a list property and has a fitness
# attribute of type FitnessMin
creator.create("Individual", list, fitness=creator.FitnessMin)

# Initialize the toolbox from the base class
toolbox = base.Toolbox()

# Register the operations to be used in the toolbox
toolbox.register("attribute", databaseClass.generateStartingTripTime, BUS_LINE)
#toolbox.register("individual", tools.initRepeat, creator.Individual,
#                 toolbox.attribute, INDIVIDUAL_SIZE)
toolbox.register("individual", inits.initRepeatBound, creator.Individual,
                  toolbox.attribute, INDIVIDUAL_SIZE_BOUNDS)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evalIndividual)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mutate", mutation.mutUniformTime)
toolbox.register("map", futures.map)
