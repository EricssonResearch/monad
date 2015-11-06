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


class Address(object):
    """

    """

    def __init__(self, name):
        self.name = name
        self.coordinates = []
        self.numbers = {}

    def addCoordinate(self, coordinate):
        self.coordinates.append(coordinate)

    def addNumber(self, number, coordinate):
        # TODO Add logic in adding a house number

        #if "-" in number:
        #    if re.search("[A-Z]", number) != None:
        #        print number
        #    #print number
        #    #print re.split("-", number)
        #    #print re.search("[1-9]+[A-Z]", number)
        #    #re.
        self.numbers[number] = coordinate

    def __str__(self):
        return "%s : %s" % (self.numbers, self.coordinates)

    def __repr__(self):
        return "%s : %s" % (self.numbers, self.coordinates)


def make_address(name):
    address = Address(name)
    return address
