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
from deap import tools, algorithms
import numpy
from dbConnection import DB
import toolBox

from fitness import Fitness

# Variables
MUTATION_PROB = 0.5
CROSS_OVER_PROB = 0.5
NO_OF_GENERATION = 2
POPULATION_SIZE = 1


def main():
    fitnessClass =Fitness()
    # Generate the population
    pop = toolBox.toolbox.population(n=POPULATION_SIZE)

    fitnessClass.evalIndividualCapacity(pop[0])
    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    pop, log = algorithms.eaSimple(pop, toolBox.toolbox, cxpb=CROSS_OVER_PROB,
                                   mutpb=MUTATION_PROB, ngen=NO_OF_GENERATION, stats=stats,
                                   halloffame=hof, verbose=True)



    ## Evaluate the entire population
    #fitnesses = list(map(toolBox.toolbox.evaluate, pop))
    #for ind, fit in zip(pop, fitnesses):

    #    ind.fitness.values = fit

    # Iterate trough a number of generations
    # for g in range(NGEN):
    #    print("-- Generation %i --" % g)
    #    # Select individuals based on their fitness
    #    offspring = toolBox.toolbox.select(pop, len(pop))
    #    # Cloning those individuals into a new population
    #    offspring = list(map(toolBox.toolbox.clone, offspring))

    #    # Calling the crossover function
    #    crossover(offspring)
    #    mutation(offspring)

    #    invalidfitness(offspring)

    # The Best Individual found
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    generateTimeTable(best_ind)


# def crossover(offspring):
#    # Apply Crossover
#    for child1, child2 in zip(offspring[::2], offspring[1::2]):
#        if random.random() < CXPB:
#            toolBox.toolbox.mate(child1, child2)
#            del child1.fitness.values
#            del child2.fitness.values
#
#
# def mutation(offspring):
#    # Testing mutation
#    for mutant in offspring:
#         if random.random() < MUTPB:
#             toolBox.toolbox.mutate(mutant)
#             del mutant.fitness.values
#
#
# def invalidfitness(offspring):
#    # Evaluate the individuals with an invalid fitness
#    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
#    fitnesses = map(toolBox.toolbox.evaluate, invalid_ind)
#    for ind, fit in zip(invalid_ind, fitnesses):
#        ind.fitness.values = fit
#    print("  Evaluated %i individuals" % len(invalid_ind))
#    # The population is entirely replaced by the offspring
#    pop[:] = offspring
#    # Gather all the fitnesses in one list and print the stats
#    fits = [ind.fitness.values[0] for ind in pop]
#    length = len(pop)
#    mean = sum(fits) / length
#    sum2 = sum(x*x for x in fits)
#    std = abs(sum2 / length - mean**2)**0.5
#    print("  Min %s" % min(fits))
#    print("  Max %s" % max(fits))
#    print("  Avg %s" % mean)
#    print("  Std %s" % std)


def generateTimeTable(individual):
    databaseClass = DB()
    timetable = databaseClass.generateTripTimeTable(individual)
    databaseClass.insertTimeTable(timetable)


if __name__ == '__main__':
    main()
