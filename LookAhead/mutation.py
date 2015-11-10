# -*- coding: utf-8 -*-
"""
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.

"""
import random
from datetime import datetime
from fitness import Fitness
from dbConnection import DB

# Initialize the classes

databaseClass = DB()
fitnessClass = Fitness()
formatString = '%H:%M'


def mutUniformTime(individual):
    ''' Mutate an individual by replacing attributes, with probability *indpb*,
    by a integer uniformly drawn between *low* and *up* inclusively.

    :param individual: :term:`Sequence <sequence>` individual to be mutated.
    
    :returns: A tuple of one individual.
    '''
    # Choose a random gene from the individual, the mutation will be applied on its random time and capacity
    mutLocation = random.randint(0, len(individual)-1)
    # Generate a random time
    # TODO: Consider Olle's suggestion to change the time between a delta value
    hour = databaseClass.mergeRandomTime(databaseClass.getRandomHour(), databaseClass.getRandomMinute())
    # Generate a random capacity
    # TODO: Some code could be added so creating a similar capacity is avoided
    capacity = databaseClass.generateRandomCapacity()
    # Assign new values to the gene
    individual[mutLocation][1] = capacity
    individual[mutLocation][2] = datetime.combine(fitnessClass.yesterday, datetime.strptime(hour, formatString).time())
    return individual,
