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
from deap import base, creator, tools
from dbConnection import DB
from fitness import Fitness
import mutation
# Variables
MUTPB = 0.5
BUSLINE = 2
NUMTRIP = 5
POPSIZE = 10

# Initialize the DB and Fitness classes
db = DB()
fitness = Fitness()
# Create individuals structure
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
# Initialize DEAP toolbox
toolbox = base.Toolbox()
# Create initial population
toolbox.register("attribute", db.generateTripTimeTable, BUSLINE)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attribute, NUMTRIP)
toolbox.register("population", tools.initRepeat, list, toolbox.individual, POPSIZE)
# Register genetic operators
toolbox.register("evaluate", fitness.evalIndividual)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mutation.mutUniformTime)
toolbox.register("select", tools.selTournament, tournsize=3)
# Generate the population
pop = toolbox.population()
# Evaluate the fitness values for entire population
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
# Apply crossover
print pop
offspring = toolbox.select(pop, len(pop))
offspring = list(map(toolbox.clone, offspring))

'''
# Testing mutation
for mutant in pop:
    if random.random() < MUTPB:
        toolbox.mutate(mutant)
        del mutant.fitness.values
'''
invalids = [ind for ind in pop if not ind.fitness.valid]
fitnesses = toolbox.map(toolbox.evaluate, invalids)
for ind, fit in zip(invalids, fitnesses):
    ind.fitness.values = fit

'''
print " Mutation done"
for child1, child2 in zip(pop[::2], pop[1::2]):
    print "Child 1"
    print len(child1)
    print "Child 2"
    print len(child2)
    #print(toolbox.mate(child1, child2))
    '''
