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
from deap import base
from deap import creator
from deap import tools
import toolBox
import random
# Variables
MUTPB = 0.5


def main():
    # Generate the population
    pop = toolBox.toolbox.population()
    # Evaluate the entire population
    fitnesses = list(map(toolBox.toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Cloning the population to select them based on their fitness
    offspring = toolBox.toolbox.select(pop, len(pop))
    offspring = list(map(toolBox.toolbox.clone, offspring))

    # Calling the crossover function
    crossover(offspring)


    '''
    invalids = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolBox.toolbox.map(toolBox.toolbox.evaluate, invalids)
    for ind, fit in zip(invalids, fitnesses):
        ind.fitness.values = fit
    '''


def crossover(offspring):
    # Apply Crossover
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        print "Child 1"
        print len(child1)
        print "Child 2"
        print len(child2)
        print(toolBox.toolbox.mate(child1, child2))


def mutation(offspring):
     # Testing mutation
     for mutant in offspring:
        if random.random() < MUTPB:
            toolBox.toolbox.mutate(mutant)
            del mutant.fitness.values



if __name__ == '__main__':
    main()