# -*- coding: utf-8 -*-
"""Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the 
License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
CONDITIONS OF ANY KIND, either express or implied. See the License for the 
specific language governing permissions and limitations under the License.
"""
import numpy
import toolBox
from deap import tools
from deap import algorithms
from dbConnection import DB
from operator import itemgetter
from fitness import Fitness
from dbConnection import DB

# Variables
MUTATION_PROB = 0.5
CROSS_OVER_PROB = 1
NO_OF_GENERATION = 2
POPULATION_SIZE = 10
fitnessClass = Fitness()
databaseClass = DB()
def main():
    # Generate the population
    pop = toolBox.toolbox.population(n=POPULATION_SIZE)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    pop, log = algorithms.eaSimple(pop, toolBox.toolbox, cxpb=CROSS_OVER_PROB,
                                   mutpb=MUTATION_PROB, ngen=NO_OF_GENERATION, stats=stats,
                                   halloffame=hof, verbose=True)

    # The Best Individual found
    best_ind = tools.selBest(pop, 1)[0]
    individual = sorted(best_ind, key=itemgetter(3))
    individual = sorted(individual, key=itemgetter(0))
    #print("Best individual is %s, %s" % (individual, best_ind.fitness.values))
    timetable = fitnessClass.genTimetable(individual)
    #databaseClass.insertBusTrip(timetable)


if __name__ == '__main__':
    main()
