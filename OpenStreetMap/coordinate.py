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


class Coordinate(object):
    """
    A geographic coordinate on a map represented by Latitude and Longitude.

    Longitude and Latitude are floating point values in degrees.
    """

    def __init__(self, latitude=0.0, longitude=0.0):
        self.latitude = float(latitude)
        self.longitude = float(longitude)

    @property
    def coordinates(self):
        return (self.longitude, self.latitude)
