# -*- coding: utf-8 -*-
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


MUTPB = 0.5

# Initialize the look ahead class
lookAhead = DB()
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)
# Register genes on the toolbox
toolbox = base.Toolbox()
# toolbox.register("line", lookAhead.getRoute, "line")
# The parameter here is the number of the line


def timeDiff(time1, time2):
    ''' Evaluates the difference between two times. 
    
    Args: time1 and time2 in datetime format, time1 > time2 
    Returns: the timedelta between time1 and time2.
    '''
    # FMT = '%H:%M:%S'
    FMT = '%H:%M'
    return datetime.strptime(time1, FMT) - datetime.strptime(time2, FMT)


def evalIndividual(individual):
    ''' Evaluate an individual in the population. Based on how close the average bus request time is to the actual bus trip time.

    @param an individual in the population
    @return a summation of the difference between past past requests' average trip starting time and actual start time
    according to the evolving timetable.
    Lower values are better.
    '''
    avgBusRequestTime = [
        '03:52', '04:22', '04:52', '05:07', '05:22', '05:37', '05:52', '06:07',
        '06:22', '06:36', '06:47', '06:57', '07:07', '07:17', '07:27', '07:37', '07:47',
        '07:57', '08:07', '08:17', '08:27', '08:37', '08:48', '09:00', '09:10', '09:20',
        '09:30', '09:40', '09:50', '10:00', '10:10', '10:20', '10:30', '10:40', '10:50',
        '11:00', '11:10', '11:20', '11:30', '11:40', '11:49', '11:59', '12:09', '12:19',
        '12:29', '12:39', '12:49', '12:59', '13:09', '13:19', '13:29', '13:39', '13:49',
        '13:59', '14:09', '14:19', '14:29', '14:39', '14:49', '14:58', '15:08', '15:18',
        '15:28', '15:38', '15:48', '15:58', '16:08', '16:18', '16:28', '16:38', '16:48',
        '16:58', '17:08', '17:18', '17:28', '17:38', '17:49', '18:00', '18:10', '18:20',
        '18:30', '18:40', '18:50', '19:00', '19:10', '19:30', '19:51', '20:11', '20:31',
        '20:51']
    # The least and most possible time timedelta values
    timeDelta = timeDiff(individual[0][2], individual[0][2])
    minDiff = timedelta.max
    diffMinutes = 0
    for reqTime in avgBusRequestTime:
        for i in range(len(individual)):
            timeTableDiff = timeDiff(individual[i][2], reqTime)
            if timeTableDiff >= timedelta(minutes=0) and timeTableDiff < minDiff:
                waitMin = individual[i][2]
                index = i
                minDiff = timeTableDiff
        '''
        print "Average req time (based on past requests)"
        print reqTime
        print "Best departure time"
        print waitMin
        print "Individual gene"
        print individual[index]
        '''
        diffMinutes += minDiff.total_seconds() / 60.0
        # print diffMinutes
        minDiff = timedelta.max  # Reset minDiff for the next request time

    # TODO: mutation may produce individuals with overlapping times, penalize such individuals
    return diffMinutes,
# Define the genes on every chromosome
toolbox.register("attribute", lookAhead.generateTripTimeTable, 2)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attribute, 24)
toolbox.register("population", tools.initRepeat, list, toolbox.individual, 100)
# Operator registering
toolbox.register("evaluate", evalIndividual)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", mutation.mutUniformTime)
toolbox.register("select", tools.selTournament, tournsize=3)
# ind = toolbox.individual()
# print ind
# Generate the population
pop = toolbox.population()
# print pop
# Evaluate the entire population
fitnesses = list(map(toolbox.evaluate, pop))
for ind, fit in zip(pop, fitnesses):
    ind.fitness.values = fit
print("  Evaluated %i individuals" % len(pop))
'''
print len(pop)
offspring = toolbox.select(pop, len(pop))
print offspring
offspring = list(map(toolbox.clone, offspring))
print offspring
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

# for child1, child2 in zip(pop[::2], pop[1::2]):
    # print "Child 1"
    # print len(child1)
    # print "Child 2"
    # print len(child2)
    #print(toolbox.mate(child1, child2))
