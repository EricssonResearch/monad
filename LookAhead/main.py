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
import struct
import time
import random
from dbConnection import DB
from deap import base
from deap import creator
from deap import tools
from datetime import datetime, timedelta
from itertools import repeat
from collections import Sequence
import mutation
import toolBox
from deap import base, creator, tools
from itertools import repeat
from collections import Sequence
from dbConnection import DB
from fitness import Fitness

MUTPB = 0.5
# Initialize the look ahead class
lookAhead = DB()
fitness = Fitness()

# Generate the population
pop = toolBox.toolbox.population()
# print pop
# Evaluate the entire population
fitnesses = list(map(toolBox.toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
#print("  Evaluated %i individuals" % len(pop))

print(len(pop))
offspring = toolBox.toolbox.select(pop, len(pop))
print(offspring)
offspring = list(map(toolBox.toolbox.clone, offspring))
print(offspring)
'''

# Testing mutation
for mutant in pop:
    if random.random() < MUTPB:
        toolbox.mutate(mutant)
        del mutant.fitness.values
'''
invalids = [ind for ind in pop if not ind.fitness.valid]
fitnesses = toolBox.toolbox.map(toolBox.toolbox.evaluate, invalids)
for ind, fit in zip(invalids, fitnesses):
    ind.fitness.values = fit

'''
print " Mutation done"

# for child1, child2 in zip(pop[::2], pop[1::2]):
    # print "Child 1"
    # print len(child1)
    # print "Child 2"
    # print len(child2)

for child1, child2 in zip(pop[::2], pop[1::2]):
    print "Child 1"
    print len(child1)
    print "Child 2"
    print len(child2)
    #print(toolbox.mate(child1, child2))
    '''
