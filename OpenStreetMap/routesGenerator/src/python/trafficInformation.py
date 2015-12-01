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
import urllib2, urllib
import string
import xml.etree.ElementTree
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree

class getTrafficInformation():
	'''
	Provide traffic information such as, 1: Accident

	2: Congestion

	3: DisabledVehicle

	4: MassTransit... 
	'''
	def __init__(self):
		SouthLatitude = 59.1995
    	WestLongitude = -18.3894
    	NorthLatitude = 59.1957
    	EastLongitude = -18.0353
    	l = 120
    	SouthLatitude = 45.219

	def postRequest(self):
		a = str(59.818882)
		b = str(17.472703)
		c = str(59.949800)
		d = str(17.818773)
		securekey = 'AvlEK4dxNCW1GZRjhXQq1S57gprUKWV2-DXms3TrExBfxO1vSxLDoYxSDDLBFcMp'
		#b = urllib.quote(self.EastLongitude)
		#c = urllib.quote(self.SouthLatitude)
		#d = urllib.quote(self.NorthLatitude)
		#f = urllib.quote(self.WestLongitude)

		#URL = "http://dev.virtualearth.net/REST/V1/Traffic/Incidents/59.818882,17.472703,59.949800,17.818773/true?t=9,2&s=2,3&o=xml&key=" + securekey
		URL = "http://dev.virtualearth.net/REST/V1/Traffic/Incidents/" + a + "," + b + "," + c + "," + d + "/true?t=9&s=2,3&o=xml&key=" + securekey

		response = urllib.urlopen(URL).read()
		root = ET.fromstring(response)
		trafficDic = {}
		index = 0
		

		for TrafficIncident in root.iter('{http://schemas.microsoft.com/search/local/ws/rest/v1}TrafficIncident'):
			trafficDic[index] = {}
			for i in range(13): 
				if i == 0:
					trafficDic[index]["StartPoint Latitude: "] = TrafficIncident[i][0].text
					trafficDic[index]["StartPoint Longitude: "] = TrafficIncident[i][1].text
				if i == 3:
					trafficDic[index]["LastModifiedUTC: "] = TrafficIncident[i].text
				if i == 4:
					trafficDic[index]["StartTimeUTC: "] = TrafficIncident[i].text
				if i == 5:
					trafficDic[index]["EndTimeUTC: "] = TrafficIncident[i].text
				if i == 6:
					trafficDic[index]["Incident Type: "] = TrafficIncident[i].text
				if i == 7:
					trafficDic[index]["Incident Severity: "] = TrafficIncident[i].text
				if i == 9:
					trafficDic[index]["Road Closed: "] = TrafficIncident[i].text
				if i == 10:
					trafficDic[index]["Description: "] = TrafficIncident[i].text
				if i == 11:
					trafficDic[index]["StopPoint Latitude: "] = TrafficIncident[i][0].text
					trafficDic[index]["StopPoint Longitude: "] = TrafficIncident[i][1].text
			index = index + 1

		print trafficDic

getTrafficInformation().postRequest()




