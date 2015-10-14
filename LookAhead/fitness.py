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
from datetime import datetime, timedelta


class Fitness():

    # Main variables
    formatString = '%H:%M'
    secondMinute = 60.0
    avgBusRequestTime = [
            '03:52', '04:22', '04:52', '05:07', '05:22', '05:37', '05:52',
            '06:07', '06:22', '06:36', '06:47', '06:57', '07:07', '07:17',
            '07:27', '07:37', '07:47', '07:57', '08:07', '08:17', '08:27',
            '08:37', '08:48', '09:00', '09:10', '09:20', '09:30', '09:40',
            '09:50', '10:00', '10:10', '10:20', '10:30', '10:40', '10:50',
            '11:00', '11:10', '11:20', '11:30', '11:40', '11:49', '11:59',
            '12:09', '12:19', '12:29', '12:39', '12:49', '12:59', '13:09',
            '13:19', '13:29', '13:39', '13:49', '13:59', '14:09', '14:19',
            '14:29', '14:39', '14:49', '14:58', '15:08', '15:18', '15:28',
            '15:38', '15:48', '15:58', '16:08', '16:18', '16:28', '16:38',
            '16:48', '16:58', '17:08', '17:18', '17:28', '17:38', '17:49',
            '18:00', '18:10', '18:20', '18:30', '18:40', '18:50', '19:00',
            '19:10', '19:30', '19:51', '20:11', '20:31', '20:51']

    def timeDiff(self, time1, time2):
        ''' Evaluates the difference between two times.

        Args: time1 and time2 in datetime format, time1 > time2
        Returns: the timedelta between time1 and time2.
        '''
        return datetime.strptime(time1, Fitness.formatString) - datetime.strptime(time2, Fitness.formatString)

    def evalIndividual(self, individual):
        ''' Evaluate an individual in the population. Based on how close the
        average bus request time is to the actual bus trip time.

        @param an individual in the population
        @return a summation of the difference between past past requests'
        average trip starting time and actual start time
        according to the evolving timetable.
        Lower values are better.
        '''
        # The least and most possible time timedelta values
        # timeDelta = timeDiff(individual[0][2], individual[0][2])
        minDiff = timedelta.max
        diffMinutes = 0
        for reqTime in Fitness.avgBusRequestTime:
            for i in range(len(individual)):
                timeTableDiff = self.timeDiff(individual[i][2], reqTime)
                if timeTableDiff >= timedelta(minutes=0) and timeTableDiff < minDiff:
                    # waitMin = individual[i][2]
                    # index = i
                    minDiff = timeTableDiff
            '''
            print "Average req time (based on past requests)"
            print reqTime
            print "Best departure time"
            print waitMin
            print "Individual gene"
            print individual[index]
            '''
            diffMinutes += minDiff.total_seconds() / Fitness.secondMinute
            # print diffMinutes
            minDiff = timedelta.max  # Reset minDiff for the next request time
        return diffMinutes,
