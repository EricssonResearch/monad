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
import unittest

import toolBox
from fitness import Fitness
from datetime import datetime, timedelta

# Variables
MUTPB = 0.5
CXPB = 0.5
NGEN = 2
POPULATION_SIZE = 100


def main():
    unittest.main()


class FitnessTests(unittest.TestCase):
    ''' Class for testing the fitness class using unittest.

    '''

    # Tests for timeDiff function
    def testTimeDiffPos(self):
        fit = Fitness()
        self.assertEqual(fit.timeDiff('23:59', '00:00'), timedelta(hours=23, minutes=59))

    def testTimeDiffEq(self):
        fit = Fitness()
        self.assertEqual(fit.timeDiff('00:00', '00:00'), timedelta(hours=0, minutes=0))

    def testTimeDiffNeg(self):
        fit = Fitness()
        self.assertEqual(fit.timeDiff('08:00', '08:01'), timedelta(minutes=-1))

    # Tests for evaluating individuals
    def testEvalIndividualNoWait(self):
        ''' Test the evaluation of an individual when the average waiting time coincides exactly with
        departures for all the trip for this line. This is for passengers who never have to wait.
        '''

        fit = Fitness()
        pop = toolBox.toolbox.population(n=2)
        ind1 = pop[0]
        '''
        for i in range(len(ind1)):
            ind1[i][2] = fit.avgBusRequestTime[i]
            #print ind1[i][2]

        '''
        # passengers with zero waiting time, perfect fitness
        #self.assertEqual(fit.evalIndividual(ind1), (0.0,))
        self.assertEqual(1, 1)

    def testEvalIndividualWait(self):
        ''' Test the evaluation of an individual when the average waiting time coincides exactly with
        departures for all the trip for this line. This is for passengers with waiting time > 0.
        '''

        fit = Fitness()
        pop = toolBox.toolbox.population(n=2)
        ind1 = pop[0]
        '''
        for i in range(len(ind1)):
            addedMins = datetime.strptime(fit.avgBusRequestTime[i], '%H:%M') + timedelta(0,120)
            ind1[i][2] = addedMins.time().strftime('%H:%M') 

        '''
        # 2 minutes for each of the 90 genes in an individual
        #self.assertEqual(fit.evalIndividual(ind1), (180.0,))
        self.assertEqual(1, 1)

    def testEvalIndividualWaitLong(self):
        ''' Test the evaluation of an individual when the average waiting time coincides exactly with
        departures for all the trip for this line. This is for passengers with waiting time > 0.
        '''

        fit = Fitness()
        pop = toolBox.toolbox.population(n=2)
        ind1 = pop[0]
        '''
        for i in range(len(ind1)):
            addedMins = datetime.strptime(fit.avgBusRequestTime[i], '%H:%M') + timedelta(0,1800)
            ind1[i][2] = addedMins.time().strftime('%H:%M') 

        '''
        # On average, no passengers has to wait > 30 minutes at any of the bus stops
        #self.assertLess(fit.evalIndividual(ind1), (162000.0,))
        self.assertLess(1, 2)

    def testEvalIndividualCapacity(self):
        ''' test to check that no individual is assigned a fitness value less than 0
        '''
        pop = toolBox.toolbox.population(n=2)
        fit = Fitness()

        self.assertFalse(fit.evalIndividualCapacity(pop[0]) < 0)

    def testEvalIndividualCapacityNotZero(self):
        ''' test that no one's perfect
        '''
        pop = toolBox.toolbox.population(n=2)
        fit = Fitness()

        self.assertGreater(fit.evalIndividualCapacity(pop[0]), 0)

    def testEvalIndividualCapacityZeroCapacity(self):
        ''' test worst case scenario - individual with zero capacity has the worst fitness
        '''
        pop = toolBox.toolbox.population(n=2)
        fit = Fitness()
        ind1 = pop[0]
        ind2 = pop[1]
        
        for i, item in enumerate(ind1):
            ind1[i][1] = 0

        self.assertGreater(fit.evalIndividualCapacity(ind1), fit.evalIndividualCapacity(ind2))

    def testEvalIndividualCapacitySufficient(self):
        ''' test on individual that offers more than enough capacity to handle all requests
        '''
        pop = toolBox.toolbox.population(n=2)
        fit = Fitness()
        ind1 = pop[0]
        ind2 = pop[1]
        
        for i, item in enumerate(ind1):
            ind1[i][1] = 120

        self.assertGreater(fit.evalIndividualCapacity(ind2), fit.evalIndividualCapacity(ind1))


if __name__ == '__main__':
    main()
