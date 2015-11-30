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
import sys
sys.path.append('../OpenStreetMap')

from deap import base
from deap import creator
from deap import tools
from scoop import futures
from dbConnection import DB
from fitness import Fitness
from operator import itemgetter
import datetime
from datetime import timedelta
from routeGenerator import coordinates_to_nearest_stops, get_route

# Constant
DB.noOfslices = 0

# The individual size corresponds to the number of trips
# TODO: Change how the INDIVIDUAL_SIZE is calculated
INDIVIDUAL_SIZE =  42

# Initialize variables
startTimeArray = []
theTimes = []

# Initialize the classes
databaseClass = DB()
fitnessClass = Fitness()


def evaluateNewIndividualFormat(individual):
    """ Evaluate an individual's fitness as a candidate timetable for the bus network.

    An individual's fitness is evaluated based on the waiting time for passengers requesting buses for the lines
    represented in the individual. Shorter waiting times on average mean better solutions. The algorithm works by by
    first sorting the individual by starting times, grouped by the bus  lines.

    Args:
        individual: an individual represented as [[lineID, Capacity, frequency, startTime]...]

    Return:
        a fitness score calculated as a cost to the bus company.
    """
    totalWaitingMinutes = []
    totalNumberRequests = []
    leftOver = []
    db = DB()
    # Order individual by starting slice time
    individual = sorted(individual, key=itemgetter(3))
    # Order individual by bus line
    individual = sorted(individual, key=itemgetter(0))
    # ------------------------------------------------------------
    # Evaluate average time based on requests & bus capacity
    # ------------------------------------------------------------
    # Get the starting time for the 1st slice
    firstSliceHr = datetime.datetime.combine(Fitness.yesterday, datetime.time(db.timeSliceArray[0][0], 0, 0))
    # Initialize initial trip time
    initialTripTime = firstSliceHr
    for i in range(len(individual)):
        # phenotype = db.generatePhenotype(individual[i][0], individual[i][3])
        phenotype = db.generatePhenotype2(individual[i])
        initialCrew = 0
        leftOvers = 0
        # ------------------------------------------------------
        # Evaluate average time and capacity for each gene now
        # ------------------------------------------------------
        for j in range(len(phenotype)):
            for k in range(len(phenotype[j])):
                # Define parameters for the first search
                initialTrip = initialTripTime
                lastTrip = phenotype[j][k][1]
                # This is a restriction, so the search is not incoherent
                if initialTrip > lastTrip:
                    initialTrip = lastTrip - timedelta(minutes=individual[i][2])
                # Search on requests from people going in and out of the bus
                request = fitnessClass.searchRequest(initialTrip, lastTrip, phenotype[j][k][0], individual[i][0])
                requestOut = fitnessClass.searchRequestOut(initialTrip, lastTrip, phenotype[j][k][0], individual[i][0])
                # TODO: Replace the length by the sum of the number of requests
                # Calculate the number of people that is left on the bus
                initialCrew = initialCrew + (len(request) - len(requestOut))
                # Compare the crew against the capacity, if it is higher then the waiting time based on capacity is calculated
                if(initialCrew > individual[i][1]):
                    # People that did not make it !!
                    leftOvers = initialCrew - individual[i][1]
                    # Total waiting time is number of people left times waiting time in minutes
                    if i < len(phenotype[j])-1:
                        # Send next gene and bus stop
                        leftOversWaitTime = leftOvers * individual[i][2]
                    else:
                        # Heuristic, computation of this would result really expensive
                        leftOversWaitTime = leftOvers * db.minutesHour
                    leftOver.append([leftOvers,leftOversWaitTime])
                # Assign the last trip value to the initial trip
                initialTripTime = phenotype[j][k][1]
                if len(request) > 0:
                    waitingMinutes = 0
                    numberRequests = 0
                    for l in range(len(request)):
                        waitingTime = phenotype[j][k][1] - request[l]["_id"]["RequestTime"]
                        waitingMinutes = waitingMinutes + round(((waitingTime.total_seconds() % 3600) / databaseClass.minutesHour), 2)
                        numberRequests = numberRequests + int(request[l]["total"])
                    totalWaitingMinutes.append(waitingMinutes)
                    totalNumberRequests.append(numberRequests)
    # Summarize the results 
    # Initialize total variable
    totalLeftOverTime = 0
    # noOfLeftOvers = 0
    # Loop trough leftovers array
    for z in range(len(leftOver)):
        # Summarize the waiting time for all the leftovers in every bus stop
        totalLeftOverTime += leftOver[z][0]
    # Summarize the waiting times based on requests and based on capacity
    totalWaitingTime = sum(totalWaitingMinutes) + totalLeftOverTime
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
toolbox.register("attribute", databaseClass.generateGenotype)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, INDIVIDUAL_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluateNewIndividualFormat)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mutate", mutation.mutUniformTime)
toolbox.register("map", futures.map)
