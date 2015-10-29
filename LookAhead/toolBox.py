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
from deap import base
from deap import creator
from deap import tools
from scoop import futures
from dbConnection import DB
from fitness import Fitness
from operator import itemgetter
from datetime import datetime
from datetime import timedelta
import mutation
import inits

# Constant
BUS_LINE = 2
# The individual size corresponds to the number of trips
INDIVIDUAL_SIZE = 90
INDIVIDUAL_SIZE_BOUNDS = [90,90]


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
    initialTripTime = "00:00"
    db = DB()
    tripWaitingTime = timedelta(minutes=0) # waiting time due to insufficient capacity
    for i, trip in enumerate(individual):
        tripTimeTable = db.generateFitnessTripTimeTable(individual[i][0], individual[i][2])
        tripStartTime = trip[2]
        start = '00:00' if i == 0 else individual[i-1][2]
        end = individual[i][2]
        stopsAndRequests = db.MaxReqNumTrip(start, end)
        count = 0
        for i, stop in enumerate(stopsAndRequests):
            if stop[1] > trip[1] and i < len(individual)-1:
                nextTripTime = individual[i+1][2]
                nextTripWait = fitnessClass.timeDiff(nextTripTime, individual[i][2])
                tripWaitingTime += nextTripWait
                count += (stop[1] - trip[1])   # must wait for the next bus trip
                #print "Next trip is in..." + str(nextTripWait) + " minutes"
                #print nextTripTime
            else:
                pass
                #print "Requested capacity " + str(stopsAndRequests[i][1])
                #print "Bus capacity " + str(trip[1])
    for i in range(len(individual)):
        tripTimeTable = db.generateFitnessTripTimeTable(individual[i][0], individual[i][2])
        for j in range(len(tripTimeTable)):
            # TODO: Fix trips that finish at the next day
            # TODO: it might be that some dates have no INDEX since there are no requests. A function has to be added to prevent them to get the LAST POSITION
            initialTrip = datetime.combine(fitnessClass.yesterday, datetime.strptime(initialTripTime, fitnessClass.formatTime).time())
            lastTrip = datetime.combine(fitnessClass.yesterday, datetime.strptime(tripTimeTable[j][1], fitnessClass.formatTime).time())
            if initialTrip > lastTrip:
                initialTrip = lastTrip - timedelta(minutes=db.getFrequency(individual[i][0]))
            # Search on Fitness.request array for the particular requests
            request = fitnessClass.searchRequest(initialTrip, lastTrip, tripTimeTable[j][0])
            initialTripTime = tripTimeTable[j][1]
            if len(request) > 0:
                diff = 0
                count = 0
                for k in range(len(request)):
                    # diff = diff + self.getMinutes(self.timeDiff(tripTimeTable[j][1], str(int(request[k]["_id"]["RequestTime"].hour)) + ":" + str(int(request[k]["_id"]["RequestTime"].minute))))*int(request[k]["total"])
                    diff = diff + fitnessClass.getMinutes(fitnessClass.timeDiff(tripTimeTable[j][1], str(int(request[k]["hour"])) + ":" + str(int(request[k]["minute"]))))*int(request[k]["count"])
                    # count = count + int(request[k]["total"])
                    count = count + int(request[k]["count"])
                dif.append(diff)
                cnt.append(count)
    return (sum(dif) + tripWaitingTime.total_seconds()/60.0)/(sum(cnt) + count),



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