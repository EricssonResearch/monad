# -*- coding: utf-8 -*-
"""
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
import re


class Address(object):
    """
    An address object is used to store street address. A address has a street
    name and possibly numbers, usually marking a house or entrance.

    A building can be associated to several numbers, e.g 10A, 10B, and 10C. If
    the different coordinates are known, all numbers can be added to a single
    address object, marking the building.

    """

    def __init__(self, name):
        self.name = name
        self.coordinates = []
        self.numbers = {}

    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def addNumber(self, number, coordinate):

        for num in address_range(number):
            self.numbers[num] = coordinate

        #self.numbers[number] = coordinate

    def __str__(self):
        return "%s : %s" % (self.numbers, self.coordinates)

    def __repr__(self):
        return "%s : %s" % (self.numbers, self.coordinates)


def make_address(name):
    address = Address(name)
    return address


def address_range(number):
    """
    Turn street number format into a range. E.g. '1A-1C' to '1A','1B','1C'.

    :param number: string
    :return: generator
    """
    numbe = re.compile(
            '''
            ((?P<fromN>(\d+))
             (?P<fromL> ([a-zA-Z]*))
             \s*-\s*
             (?P<toN>(\d+))
             (?P<toL>([a-zA-Z]*)))
            ''',
            re.VERBOSE
        )
    match = numbe.search(number)

    if match:
        fromNumber = match.groupdict()['fromN']
        fromLetter = match.groupdict()['fromL']
        toNumber = match.groupdict()['toN']
        toLetter = match.groupdict()['toL']
        if fromLetter and toLetter:
            for c in xrange(ord(fromLetter), ord(toLetter)+1):
                yield ''+fromNumber+chr(c)
        elif fromNumber and toNumber:
            for d in xrange(int(fromNumber), int(toNumber)+1):
                yield d
        else:
            yield ''+fromNumber+fromLetter
    else:
        numbers = number.split(',')
        if len(numbers) > 1:
            for num in numbers:
                yield num.strip()
        else:
            yield number
