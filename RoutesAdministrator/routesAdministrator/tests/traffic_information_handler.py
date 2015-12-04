'''
Copyright 2015 Ericsson AB

Licensed under the Apache License, Version 2.0 (the 'License'); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
'''
import json
import urllib2, urllib
import string
import xml.etree.ElementTree
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import ElementTree

def start():
    global secure_key
    secure_key = 'AvlEK4dxNCW1GZRjhXQq1S57gprUKWV2-DXms3TrExBfxO1vSxLDoYxSDDLBFcMp'

def get_traffic_information():
    south_latitude = '59.818882'
    west_longitude = '17.472703'
    north_latitude = '59.949800'
    east_longitude = '17.818773'
    URL = 'http://dev.virtualearth.net/REST/V1/Traffic/Incidents/' + \
          south_latitude + ',' + \
          west_longitude + ',' + \
          north_latitude + ',' + \
          east_longitude + \
          '/true?t=9&s=2,3&o=xml&key=' + \
          secure_key

    response = urllib.urlopen(URL).read()
    root = ET.fromstring(response)
    return parse_root(root)

def get_traffic_information_with_params(south_latitude, west_longitude, north_latitude, east_longitude):
    URL = 'http://dev.virtualearth.net/REST/V1/Traffic/Incidents/' + \
          south_latitude + ',' + \
          west_longitude + ',' + \
          north_latitude + ',' + \
          east_longitude + \
          '/true?t=9&s=2,3&o=xml&key=' + \
          secure_key

    response = urllib.urlopen(URL).read()
    root = ET.fromstring(response)
    return parse_root(root)


def parse_root(root):
    traffic_dic = {}
    index = 0

    for traffic_incident in root.iter('{http://schemas.microsoft.com/search/local/ws/rest/v1}TrafficIncident'):
        traffic_dic[index] = {}
        traffic_dic[index]['StartPointLatitude'] = traffic_incident[0][0].text
        traffic_dic[index]['StartPointLongitude'] = traffic_incident[0][1].text
        traffic_dic[index]['LastModifiedUTC'] = traffic_incident[3].text
        traffic_dic[index]['StartTimeUTC'] = traffic_incident[4].text
        traffic_dic[index]['EndTimeUTC'] = traffic_incident[5].text
        traffic_dic[index]['IncidentType'] = traffic_incident[6].text
        traffic_dic[index]['IncidentSeverity'] = traffic_incident[7].text
        traffic_dic[index]['Road Closed'] = traffic_incident[9].text
        traffic_dic[index]['Description'] = traffic_incident[10].text
        traffic_dic[index]['StopPointLatitude'] = traffic_incident[11][0].text
        traffic_dic[index]['StopPointLongitude'] = traffic_incident[11][1].text
        index = index + 1

    return json.dumps(traffic_dic)

if __name__ == "__main__":
    start()
    print get_traffic_information()
    print '\n'
    print get_traffic_information_with_params('59.818882', '17.472703', '59.949800', '17.818773')
