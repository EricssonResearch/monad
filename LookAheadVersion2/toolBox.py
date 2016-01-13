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
from deap import base
from deap import creator
from deap import tools
from scoop import futures
from dbConnection import DB
from fitness import Fitness
from operator import itemgetter
import datetime
from datetime import timedelta
import math


# Constant
BUS_LINE = 2
DB.noOfslices = 0

# The individual size corresponds to the number of bus lines x number of time slices
INDIVIDUAL_SIZE = 42
INDIVIDUAL_SIZE_BOUNDS = [30, 90]
startTimeArray = []
startTimeForABusStop = []
theTimes = []
completeStartTimeArray =[]

# Initialize the classes
databaseClass = DB()
fitnessClass = Fitness()


def evaluateNewIndividualFormat(individual):
    ''' Fitness function that evaluates and each individual in the
    population and assigns a fitness value to it which is the
    average waiting time for the
    individual (i.e a timetable)

        @param: individual - encoded individual which represents
        an timetable for mulitple lines.

    '''

    individual = sorted(individual, key=itemgetter(3))
    individual = sorted(individual, key=itemgetter(0))
    # Second, we loop trough the number of genes in order to retrieve the
    # number of requests for that particular trip
    # For the 1st trip, the starting time has to be selected
    request = []
    totalWaitingMinutes = []
    cnt = []
    db = DB()
    # ----------------------------------------------------
    # Evaluate average time based on requests (& capacity)
    # ----------------------------------------------------
    leftOver = []
    l = len(db.timeSliceArray) - 1
    startT = datetime.datetime.combine(Fitness.yesterday, datetime.time(db.timeSliceArray[l][0], 0, 0))
    endT = datetime.datetime.combine(Fitness.yesterday, datetime.time(db.timeSliceArray[l][1], 59, 59))
    firstSliceHr = datetime.datetime.combine(Fitness.yesterday, datetime.time(db.timeSliceArray[0][0], 0, 0))

    for i in range(len(individual)):
        phenotype = db.generatePhenotype(individual[i][0], individual[i][3])
        initialCrew = 0
        leftOvers = 0
        leftOversWaitTime = 0
        firstHrOfTimeSlice, LastHrOfTimeSlice = fitnessClass.getTimeSlice(individual[i][3])
        diffToFirstHrSlice = individual[i][3] - firstHrOfTimeSlice
        diffToFirstHrSlice = diffToFirstHrSlice.days * databaseClass.minutesDay + diffToFirstHrSlice.seconds / databaseClass.minutesHour
        diffToLastHrSlice = LastHrOfTimeSlice - individual[i][3]
        diffToLastHrSlice = diffToLastHrSlice.days * databaseClass.minutesDay + diffToLastHrSlice.seconds / databaseClass.minutesHour
        backTrips = round(float(diffToFirstHrSlice)/float(individual[i][2]))
        forwardTrips = round(float(diffToLastHrSlice)/float(individual[i][2]))
        noOfTrips = backTrips + forwardTrips + 1

        for key in fitnessClass.totalRequestsBusline:
            if individual[i][0] == key[0] and (key[1] <= individual[i][3] <= key[2]):
                totalCapacityInSlice = noOfTrips * individual[i][1]
                initialCrew = fitnessClass.totalRequestsBusline[key]
                try:
                    if (initialCrew >totalCapacityInSlice ):
                        leftOvers = initialCrew - totalCapacityInSlice

                        if (individual[i][3] + timedelta(minutes=individual[i][2]) > endT):
                            timed = (endT - individual[i][3]) + timedelta(hours=db.timeSliceArray[0][0])
                            timed = (timed.days * databaseClass.minutesDay) + (timed.seconds / databaseClass.minutesHour)
                            timed = timed * leftOvers

                            leftOver.append([timed, leftOvers])

                        else:

                            timed = (individual[i][2]) * leftOvers

                            leftOver.append([timed, leftOvers])

                except IndexError:
                    print("Error")
        for j in range(len(phenotype)):
            # TODO: Fix trips that finish at the next day
            deprtTimeBusStop = phenotype[j][1]
            # Search on Fitness.request array for the all request made in a slice for a particular busStop and Line
            request = fitnessClass.searchRequest(firstHrOfTimeSlice, LastHrOfTimeSlice, phenotype[j][0], individual[i][0])
            if len(request) > 0:
                waitingMinutes = 0
                count = 0
                for k in range(len(request)):
                    requestTime = request[k]["_id"]["RequestTime"]

                    # Senario 1 - When the request time made is after the starting time provided in the GENE
                    # i.e people who can NOT make it.
                    if requestTime > deprtTimeBusStop:
                        difference = requestTime-deprtTimeBusStop
                        difference = difference.days * databaseClass.minutesDay + difference.seconds / databaseClass.minutesHour
                        noOfTimesToGoForwardOnClock = math.ceil(float(difference)/float(individual[i][2]))
                        if noOfTimesToGoForwardOnClock == 1:
                            newTripToTake = deprtTimeBusStop + timedelta(minutes=individual[i][2])
                            waitingTime = (newTripToTake - requestTime)
                            waitingMinutes = waitingTime.days * databaseClass.minutesDay + waitingTime.seconds / databaseClass.minutesHour
                        else:
                            totalMinToGoForwardOnClock = noOfTimesToGoForwardOnClock * individual[i][2]
                            newTripToTake = deprtTimeBusStop + timedelta(minutes=totalMinToGoForwardOnClock)
                            waitingTime = (newTripToTake - requestTime)
                            waitingMinutes = waitingTime.days * databaseClass.minutesDay + waitingTime.seconds / databaseClass.minutesHour

                    # Senario 2 - When the request time made is before the starting time provided in the GENE
                    # i.e people who can make it.
                    else:
                        difference = deprtTimeBusStop-requestTime
                        difference = difference.days * databaseClass.minutesDay + difference.seconds / databaseClass.minutesHour
                        noOfTimesToGoBackOnClock = math.floor(float(difference)/float(individual[i][2]))
                        if noOfTimesToGoBackOnClock == 0:
                            waitingTime = (deprtTimeBusStop - requestTime)
                            waitingMinutes = waitingTime.days * databaseClass.minutesDay + waitingTime.seconds / databaseClass.minutesHour
                        else:
                            totalMinToGoBackOnClock = noOfTimesToGoBackOnClock * individual[i][2]
                            newTripToTake = deprtTimeBusStop - timedelta(minutes=totalMinToGoBackOnClock)
                            waitingTime = (newTripToTake - requestTime)
                            waitingMinutes = waitingTime.days * databaseClass.minutesDay + waitingTime.seconds / databaseClass.minutesHour
                    count = count + int(request[k]["total"])
                    waitingMinutes = waitingMinutes * request[k]["total"]
                    totalWaitingMinutes.append(waitingMinutes)

                # The cnt array consists of the number of requests made for a particular request time
                # eg. 3 people made a request to leave at 4:30
                cnt.append(count)

    totalLeftOverTime = 0
    noOfLeftOvers = 0
    for k in range(len(leftOver)):
        totalLeftOverTime += leftOver[k][0]
        noOfLeftOvers += leftOver[k][1]
    totalWaitingTime = sum(totalWaitingMinutes) + totalLeftOverTime
    averageWaitingTime = totalWaitingTime / (sum(cnt) + noOfLeftOvers)

    return averageWaitingTime,

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
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, INDIVIDUAL_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluateNewIndividualFormat)
toolbox.register("mutate", mutation.mutUniformTime)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("map", futures.map)
