import random
import time
from datetime import datetime
from datetime import timedelta
from fitness import Fitness
from dbConnection import DB

formatString = '%H:%M'

# Initialize the classes

databaseClass = DB()
fitnessClass = Fitness()

def strTimeProp(start, end, format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formated in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))


def randomDate(start, end, prop):
    return strTimeProp(start, end, formatString, prop)


def mutUniformTime(individual):
    """Mutate an individual by replacing attributes, with probability *indpb*,
    by a integer uniformly drawn between *low* and *up* inclusively.

    :param individual: :term:`Sequence <sequence>` individual to be mutated.
    :param low: The lower bound or a :term:`python:sequence` of
                of lower bounds of the range from wich to draw the new
                integer.
    :param up: The upper bound or a :term:`python:sequence` of
               of upper bounds of the range from wich to draw the new
               integer.
    :param indpb: Independent probability for each attribute to be mutated.
    :returns: A tuple of one individual.
    """
    mutLocation = random.randint(0, len(individual)-1)
    '''
    if not isinstance(low, Sequence):
        low = repeat(low, size)
    elif len(low) < size:
        raise IndexError("low must be at least the size of individual: %d < %d" % (len(low), size))
    if not isinstance(up, Sequence):
        up = repeat(up, size)
    elif len(up) < size:
        raise IndexError("up must be at least the size of individual: %d < %d" % (len(up), size))
    '''
    # Repairing the mutant
    hour = databaseClass.generateTime(databaseClass.generateMinute(databaseClass.mergeRandomTime(databaseClass.getRandomHour(), databaseClass.getRandomMinute())))
    # timeDiff = datetime.strptime(randomDate("00:00", "23:59", random.random()), formatString)
    # individual[mutLocation][2] = timeDiff.time().strftime(formatString)
    individual[mutLocation][2] = datetime.combine(fitnessClass.yesterday, datetime.strptime(hour, formatString).time())
    # Update the gene's bus stops after mutation, assumes time between 2 bus stops is 120 seconds
    # TODO: use variable time from database
    # THIS LOOP IS NEVER EXECUTED
    for trip in range(3, len(individual[mutLocation])):
        individual[mutLocation][trip] = (timeDiff + timedelta(0, 120*(trip-2))).time().strftime(formatString)
    '''
    for i, xl, xu in zip(range(size), low, up):
        if random.random() < indpb:
            individual[i] = strTimeProp(xl, xu, '%H:%M', random.random())
            #print(individual[i])
    '''
    return individual,
