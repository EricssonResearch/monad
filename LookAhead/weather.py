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
from datetime import date
from datetime import timedelta
from dbConnection import DB
import forecastio

db = DB()

class Weather(object):
    """Implements a class to modify timetables based on weather"""
    # ------------------------------------------------------------
    # Class variables
    # ------------------------------------------------------------
    # Forecastio API Credentials
    apiKey = "664dfbd4b12d75c56aab4503f2ddda01"
    # This values can be replaced by Open Maps coordenates values
    latitude = 59.8552777778
    longitude = 17.6319444444

    def __init__(self):
        super(Weather, self).__init__()
        # self.arg = arg
        self.getWeatherData()

    def setQueryDay(self, days):
        """Depending on how workflow is gonna be, pass days to query as a
        parameter"""
        return date.today() + timedelta(days)

    def callWeatherAPI(self):
        """Calls API to get weather information"""
        return forecastio.load_forecast(Weather.apiKey, Weather.latitude, Weather.longitude)

    def getWeatherHourly(self, forecast):
        """Returns the weather info on a specific frequency
        A switch statement can be implemented to pass info
        on a specific frequency (hourly, daily, etc).
        """
        return forecast.hourly()

    '''
    def getWeatherData(self):
        """Calls API to get weather information"""
        forecast = self.getWeatherHourly(self.callWeatherAPI())
        for data in forecast.data:
            if data.time.date() == self.setQueryDay(2):
                print "========================"
                print data.icon
                print data.time
                print data.temperature
    '''


#if __name__ == '__main__':
#    Weather().__init__()    