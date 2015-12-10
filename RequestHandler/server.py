# Copyright 2015 Ericsson AB
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not 
# use this file except in compliance with the License. You may obtain a copy 
# of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software 
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT 
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the 
# License for the specific language governing permissions and limitations 
# under the License.


import cgi
import json
import logging
import pymongo
import smtplib
import requests
import serverConfig

from random import randint
from pymongo import errors
from datetime import datetime
from builtins import str, range
from bson.objectid import ObjectId
from planner import TravelPlanner, Mode
from routeGenerator import string_to_coordinates, coordinates_to_nearest_stop


def escape(text):
    """Replace dangerous characters with blanks"""
    return "".join(serverConfig.escape_table.get(c,c) for c in text)
    
    
def send_email(from_addr, to_addr_list, subject, message): 
    """Send an email"""
    header  = "From: {0}\n".format(from_addr)
    header += "To: {0}\n".format(",".join(to_addr_list))
    header += "Subject: {0}\n\n".format(subject)
    message = header + message
 
    server = smtplib.SMTP(serverConfig.EMAIL_HOST, serverConfig.EMAIL_PORT)
    server.starttls()
    server.login(serverConfig.EMAIL_ADDRESS, serverConfig.EMAIL_PASSWORD)
    server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    

def get_search_results(database, priority, requestId):
    """Get the search results from the travel planner"""
    travelPlanner = TravelPlanner(database)
    userTripJson = {}
    if (priority == "distance"):
        userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.tripTime)
    else:
        userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.waitTime)             
    return userTripJson


def get_nearest_bus_stop_and_coordinates(address):
    """Get the nearest bus stop to the address and its coordinates"""
    coordinates = string_to_coordinates(address)
    if (coordinates["latitude"] == None or coordinates["longitude"] == None): 
        logging.error("Problematic address: {0}".format(address))       
        raise ValueError("Could not find the coordinates for the address given.")
    else:
        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]
        stop = coordinates_to_nearest_stop(longitude, latitude)
        result = {"latitude": latitude, "longitude": longitude, "busStop": stop["name"]}
        return result


def _update_number_of_passengers(busTripIDs, database, startBusStops, endBusStops, amount):
    """Update the number of passengers boarding/departing"""
    for index in range(len(busTripIDs)):
        collection = database.BusStop
        document = collection.find_one({"name": startBusStops[index]})
        startBusStop = document["_id"]
        document = collection.find_one({"name": endBusStops[index]})
        endBusStop = document["_id"]
                    
        collection = database.BusTrip
        collection.update_one({"$and": [{"_id": busTripIDs[index]},
                                {"trajectory": {"$elemMatch": {"busStop": startBusStop}}}]}, 
                                {"$inc": {"trajectory.$.boardingPassengers": amount}})
        collection.update_one({"$and": [{"_id": busTripIDs[index]}, 
                                {"trajectory": {"$elemMatch": {"busStop": endBusStop}}}]}, 
                                {"$inc": {"trajectory.$.departingPassengers": amount}})


def application(env, start_response):
    """Get data from the client and handle them according to the type of the request"""
    data_env = env.copy()
    # Remove the query string from the request, we only accept data through POST
    data_env["QUERY_STRING"] = ""   
    data = cgi.FieldStorage(fp = env["wsgi.input"], environ = data_env)
    responseCode = "200 OK" 
    reponseType = "text/plain"    
    
    if (data_env["PATH_INFO"] == "/request"):
        searchResults = {}
        if ("userId" and "startTime" and "endTime" and "requestTime" and "stPosition" and "edPosition" 
            and "priority" and "startPositionLatitude" and "startPositionLongitude" in data):
            userId = int(escape(data.getvalue("userId")))
            startTime = escape(data.getvalue("startTime"))
            endTime = escape(data.getvalue("endTime"))
            requestTime = escape(data.getvalue("requestTime"))
            stPosition = escape(data.getvalue("stPosition"))
            edPosition = escape(data.getvalue("edPosition"))
            priority = escape(data.getvalue("priority"))
            startPositionLatitude = float(escape(data.getvalue("startPositionLatitude")))
            startPositionLongitude = float(escape(data.getvalue("startPositionLongitude"))) 
            
            try:
                if (stPosition != "Current Position"):
                    stPositionInfo = get_nearest_bus_stop_and_coordinates(stPosition)
                    startPositionLatitude = stPositionInfo["latitude"]
                    startPositionLongitude = stPositionInfo["longitude"]
                    startStop = stPositionInfo["busStop"]
                else:                                                                       
                    stop = coordinates_to_nearest_stop(startPositionLongitude, startPositionLatitude)
                    startStop = stop["name"]                        
            
                edPositionInfo = get_nearest_bus_stop_and_coordinates(edPosition)           
                endPositionLatitude = edPositionInfo["latitude"]
                endPositionLongitude = edPositionInfo["longitude"]
                endStop = edPositionInfo["busStop"]
            
                requestTime = datetime.strptime(requestTime, serverConfig.DATE_FORMAT)
                if (startTime == "null"):
                    endTime = datetime.strptime(endTime, serverConfig.DATE_FORMAT)
                elif (endTime == "null"):
                    startTime = datetime.strptime(startTime, serverConfig.DATE_FORMAT)
                  
                database = serverConfig.MONGO_DATABASE
                collection = database.BusStop               
                startBusStop = collection.find_one({"name": startStop})
                endBusStop = collection.find_one({"name": endStop})
                
                if (startBusStop == None or endBusStop == None):
                    start_response("200 OK", [("Content-Type", "application/json")])                            
                    return [json.dumps(searchResults)]                 
                
                collection = database.TravelRequest     
                document = {"userID": userId, "startTime": startTime, "endTime": endTime,
                            "requestTime": requestTime, "startPositionLatitude": startPositionLatitude,
                            "startPositionLongitude": startPositionLongitude, "startBusStop": startBusStop["_id"],
                            "endPositionLatitude": endPositionLatitude, "endBusStop": endBusStop["_id"],
                            "endPositionLongitude": endPositionLongitude}           
                result = collection.insert_one(document)
                requestId = result.inserted_id              
                searchResults = get_search_results(database, priority, requestId)
            
            except ValueError as e:
                responseCode = "500 INTERNAL ERROR"                
                logging.error("Something went wrong: {0}".format(e))                
            except pymongo.errors.PyMongoError as e:
                responseCode = "500 INTERNAL ERROR"  
                logging.error("Something went wrong: {0}".format(e))
            finally:                                    
                serverConfig.MONGO_CLIENT.close()                

        else:
            responseCode = "500 INTERNAL ERROR"  
            logging.error("Request: Something went wrong with the data sent by the user's request.")
        
        reponseType = "application/json"
        response = json.dumps(searchResults)
            
    elif (data_env["PATH_INFO"] == "/resetPassword"):        
        if ("email" in data):
            email = data.getvalue("email") 
            email_list = [email]
            code = randint(1000, 9999)
            message = serverConfig.EMAIL_MESSAGE.format(code)
            send_email(serverConfig.EMAIL_ADDRESS, email_list, serverConfig.EMAIL_SUBJECT, message)
            response = "{0}".format(code)
        else:
            responseCode = "500 INTERNAL ERROR"  
            logging.error("Reset Password: Something went wrong with the data sent by the user's request.")
            response = serverConfig.ERROR_MESSAGE
            
    elif (data_env["PATH_INFO"] == "/quickRequest"):
        searchResults = {}
        if ("userId" and "startTime" and "endTime" and "requestTime" and "startPositionLatitude"
            and "startPositionLongitude" and "edPosition" and "priority" in data):
            userId = int(escape(data.getvalue("userId")))
            startTime = escape(data.getvalue("startTime"))
            endTime = escape(data.getvalue("endTime"))
            requestTime = escape(data.getvalue("requestTime"))
            startPositionLatitude = float(escape(data.getvalue("startPositionLatitude")))
            startPositionLongitude = float(escape(data.getvalue("startPositionLongitude")))
            edPosition = escape(data.getvalue("edPosition"))
            priority = escape(data.getvalue("priority"))            
            
            try:
                stop = coordinates_to_nearest_stop(startPositionLongitude, startPositionLatitude)           
                startStop = stop["name"]
                
                edPositionInfo = get_nearest_bus_stop_and_coordinates(edPosition)           
                endPositionLatitude = edPositionInfo["latitude"]
                endPositionLongitude = edPositionInfo["longitude"]
                endStop = edPositionInfo["busStop"]
                
                requestTime = datetime.strptime(requestTime, serverConfig.DATE_FORMAT)
                if (startTime == "null"):
                    endTime = datetime.strptime(endTime, serverConfig.DATE_FORMAT)
                elif (endTime == "null"):
                    startTime = datetime.strptime(startTime, serverConfig.DATE_FORMAT)
                  
                database = serverConfig.MONGO_DATABASE
                collection = database.BusStop               
                startBusStop = collection.find_one({"name": startStop})
                endBusStop = collection.find_one({"name": endStop})
                
                if (startBusStop == None or endBusStop == None):
                    start_response("200 OK", [("Content-Type", "application/json")])                            
                    return [json.dumps({})]             
                
                collection = database.TravelRequest     
                document = {"userID": userId, "startTime": startTime, "endTime": endTime,
                            "requestTime": requestTime, "startPositionLatitude": startPositionLatitude,
                            "startPositionLongitude": startPositionLongitude, "startBusStop": startBusStop["_id"],
                            "endPositionLatitude": endPositionLatitude, "endBusStop": endBusStop["_id"],
                            "endPositionLongitude": endPositionLongitude}           
                result = collection.insert_one(document)
                requestId = result.inserted_id              
                searchResults = get_search_results(database, priority, requestId)                                            
                
            except ValueError as e:
                responseCode = "500 INTERNAL ERROR"
                logging.error("Something went wrong: {0}".format(e))                 
            except pymongo.errors.PyMongoError as e:
                responseCode = "500 INTERNAL ERROR"  
                logging.error("Something went wrong: {0}".format(e)) 
            finally:                    
                serverConfig.MONGO_CLIENT.close()                                       
        else:
            responseCode = "500 INTERNAL ERROR"  
            logging.error("Quick request: Something went wrong with the data sent by the user's request.")
        
        reponseType = "application/json"
        response = json.dumps(searchResults)
            
    elif (data_env["PATH_INFO"] == "/bookingRequest"):
        if ("userTripId" in data):
            userTripId = escape(data.getvalue("userTripId"))            
                
            try:                        
                database = serverConfig.MONGO_DATABASE              
                collection = database.UserTrip
                objectID = ObjectId(userTripId)
                busTripIDs = []
                startBusStops = []
                endBusStops = []                                                
                
                document = collection.find_one({"_id": objectID})
                startTime = document["startTime"]
                startBusStop = document["startBusStop"]
                endTime = document["endTime"]               
                endBusStop = document["endBusStop"]
                startBusID = document["busID"]
                lastBusID = document["busID"]
                userId = document["userID"] 
                busTripIDs.append(document["busTripID"])
                startBusStops.append(startBusStop)
                endBusStops.append(endBusStop)          
                
                while ("next" in document):
                    document = collection.find_one({"_id": document["next"]})
                    endTime = document["endTime"]
                    endBusStop = document["endBusStop"]
                    lastBusID = document["busID"]
                    busTripIDs.append(document["busTripID"])
                    startBusStops.append(document["startBusStop"])
                    endBusStops.append(endBusStop)                  
                    
                collection = database.BookedTrip
                bookedTrips = collection.find({"userID": userId})
                collection = database.UserTrip
                
                # Check if the user has already booked this trip. Unfortunately we can't just compare the trip IDs
                # because they change every time the user makes a new search.
                if (bookedTrips != None):
                    for bookedTrip in bookedTrips:
                        partialTrips = bookedTrip["partialTrips"]
                        partialTripFirst = partialTrips[0]
                        partialTripLast = partialTrips[len(partialTrips) - 1]                   
                        first = collection.find_one({"_id": partialTripFirst})
                        last = collection.find_one({"_id": partialTripLast})
                        
                        if (startTime == first["startTime"] and endTime == last["endTime"]
                            and startBusStop == first["startBusStop"] and endBusStop == last["endBusStop"]
                            and startBusID == first["busID"] and lastBusID == last["busID"]):
                              
                            start_response("200 OK", [("Content-Type", "text/plain")])              
                            return [serverConfig.BOOKING_DOUBLE_MESSAGE]
                
                document = collection.find_one_and_update({"_id": objectID}, {"$set": {"booked": True}})
                partialTrips = []
                partialTrips.append(objectID)
                
                # Book all partial trips that are part of this trip
                while ("next" in document):
                    objectID = document["next"]
                    partialTrips.append(objectID)
                    document = collection.find_one_and_update({"_id": objectID}, {"$set": {"booked": True}})
                    
                collection = database.BookedTrip
                document = {"userID": userId, "partialTrips": partialTrips, "notified": False}
                bookedTripID = collection.insert_one(document).inserted_id
                
                _update_number_of_passengers(busTripIDs, database, startBusStops, endBusStops, 1)
                
            except pymongo.errors.PyMongoError as e:
                responseCode = "500 INTERNAL ERROR"  
                logging.error("Something went wrong: {0}".format(e))
                response = serverConfig.ERROR_MESSAGE             
            else:                              
                response = serverConfig.BOOKING_SUCCESSFUL_MESSAGE
            finally:                    
                serverConfig.MONGO_CLIENT.close()
        else:
            responseCode = "500 INTERNAL ERROR"  
            logging.error("Booking request: Something went wrong with the data sent by the user's request.")
            response = serverConfig.ERROR_MESSAGE        
            
    elif (data_env["PATH_INFO"] == "/bookingCancelRequest"):
        if ("userTripId" in data):
            userTripId = escape(data.getvalue("userTripId"))
            
            try:                        
                database = serverConfig.MONGO_DATABASE              
                collection = database.UserTrip
                objectID = ObjectId(userTripId)
                busTripIDs = []
                startBusStops = []
                endBusStops = []                
                
                document = collection.find_one_and_update({"_id": objectID}, {"$set": {"booked": False}})               
                userId = document["userID"]
                busTripIDs.append(document["busTripID"])
                startBusStops.append(document["startBusStop"])
                endBusStops.append(document["endBusStop"])          
                
                # Unbook all partial trips that are part of this trip
                while ("next" in document):
                    document = collection.find_one_and_update({"_id": document["next"]}, {"$set": {"booked": False}})
                    busTripIDs.append(document["busTripID"])
                    startBusStops.append(document["startBusStop"])
                    endBusStops.append(document["endBusStop"])              
                
                collection = database.BookedTrip
                bookedTrips = collection.find({"userID": userId})
                for bookedTrip in bookedTrips:
                    partialTrips = bookedTrip["partialTrips"]
                    if (partialTrips[0] == objectID):
                        collection.delete_one({"_id": bookedTrip["_id"]})
                        break
                    
                _update_number_of_passengers(busTripIDs, database, startBusStops, endBusStops, -1)                      
                
            except pymongo.errors.PyMongoError as e:
                responseCode = "500 INTERNAL ERROR"  
                logging.error("Something went wrong: {0}".format(e))
                response = serverConfig.ERROR_MESSAGE     
            else:                              
                response = serverConfig.BOOKING_CANCEL_SUCCESSFUL_MESSAGE
            finally:                    
                serverConfig.MONGO_CLIENT.close()
        else:
            responseCode = "500 INTERNAL ERROR"  
            logging.error("Booking cancel request: Something went wrong with the data sent by the user's request.")
            response = serverConfig.ERROR_MESSAGE        
    
    elif (data_env["PATH_INFO"] == "/getUserBookingsRequest"):
        userTripJson = {}
        if ("userId" in data):
            userId = int(escape(data.getvalue("userId")))
        
            try:                        
                database = serverConfig.MONGO_DATABASE              
                collection = database.BookedTrip                
                
                i = 0
                bookedTrips = collection.find({"userID": userId})
                collection = database.UserTrip
                for bookedTrip in bookedTrips:
                    partialTripIDs = bookedTrip["partialTrips"]
                    partialTrips = []
                    
                    # Delete bookings more than the specified days old
                    document = collection.find_one({"_id": partialTripIDs[0]})
                    if ((datetime.now() - document["startTime"]).days 
                            >= serverConfig.NUMBER_OF_DAYS_TO_KEEP_USER_BOOKINGS):                      
                        collection = database.BookedTrip    
                        collection.delete_one({"_id": bookedTrip["_id"]})
                        collection = database.UserTrip
                        continue
                    
                    for partialTripID in partialTripIDs:
                        partialTripCursor = collection.find_one({"_id": partialTripID})
                         
                        if ("requestTime" in partialTripCursor and "requestID" in partialTripCursor):
                            requestTime = str(partialTripCursor["requestTime"]) 
                            requestID = str(partialTripCursor["requestID"])
                        else:
                            # Applies to user trips generated by the recommendation module
                            requestTime = str(datetime.now())                                                   
                            requestID = "null" 
                                                                                                                             
                        partialTrip = {
                            "_id": str(partialTripCursor["_id"]),
                            "userID": partialTripCursor["userID"],
                            "line": partialTripCursor["line"],
                            "busID": partialTripCursor["busID"],
                            "startBusStop": partialTripCursor["startBusStop"],
                            "endBusStop": partialTripCursor["endBusStop"],
                            "startTime": str(partialTripCursor["startTime"]),
                            "endTime": str(partialTripCursor["endTime"]),
                            "requestTime": requestTime,
                            "trajectory": partialTripCursor["trajectory"],
                            "feedback": partialTripCursor["feedback"],
                            "requestID": requestID,
                            "booked": partialTripCursor["booked"]
                        }
                        if ("next" in partialTripCursor):
                            partialTrip["next"] = str(partialTripCursor["next"])
                        partialTrips.append(partialTrip)
                    
                    i += 1
                    userTripJson[i] = partialTrips
                
            except pymongo.errors.PyMongoError as e:
                responseCode = "500 INTERNAL ERROR"
                userTripJson = {}  
                logging.error("Something went wrong: {0}".format(e)) 
            finally:                    
                serverConfig.MONGO_CLIENT.close()
        else:
            responseCode = "500 INTERNAL ERROR"              
            logging.error("Get user bookings request: Something went wrong with the data sent by the user's request.")            
        
        reponseType = "application/json"
        response = json.dumps(userTripJson)
    
    elif (data_env["PATH_INFO"] == "/updateFeedbackRequest"):       
        if ("changedFeedback" in data):
            try:            
                changedFeedback = json.loads(data.getvalue("changedFeedback"))
                database = serverConfig.MONGO_DATABASE              
                collection = database.UserTrip
                
                for userTripID in changedFeedback:
                    userTripID = escape(userTripID)                                 
                    objectID = ObjectId(userTripID)                    
                    feedback = int(escape(str(changedFeedback[userTripID])))                  
                    document = collection.find_one_and_update({"_id": objectID}, {"$set": {"feedback": feedback}})
                        
                    while ("next" in document):
                        objectID = document["next"]
                        document = collection.find_one_and_update({"_id": objectID}, {"$set": {"feedback": feedback}})
                
            except pymongo.errors.PyMongoError as e:
                responseCode = "500 INTERNAL ERROR"  
                logging.error("Something went wrong: {0}".format(e))
                response = serverConfig.ERROR_MESSAGE
            except ValueError as e:
                responseCode = "500 INTERNAL ERROR"
                logging.error("Something went wrong: {0}".format(e)) 
                response = serverConfig.ERROR_MESSAGE       
            else:                              
                response = serverConfig.FEEDBACK_UPDATE_SUCCESSFUL_MESSAGE
            finally:                    
                serverConfig.MONGO_CLIENT.close()
        else:
            responseCode = "500 INTERNAL ERROR"  
            logging.error("Update feedback request: Something went wrong with the data sent by the user's request.")
            response = serverConfig.ERROR_MESSAGE            
    
    elif (data_env["PATH_INFO"] == "/storeGeofenceInfo"):       
        if ("userID" and "geofenceInfo" in data):
            try:
                userID = int(escape(data.getvalue("userID")))            
                geofenceInfo = json.loads(data.getvalue("geofenceInfo"))
                database = serverConfig.MONGO_DATABASE
                collection = database.Geofence
                
                for busStop in geofenceInfo:
                    time = datetime.strptime(geofenceInfo[busStop]["time"], serverConfig.DATE_FORMAT)                    
                    document = {
                        "userID": userID,                        
                        "latitude": geofenceInfo[busStop]["latitude"],
                        "longitude": geofenceInfo[busStop]["longitude"],
                        "time": time
                    }
                    collection.insert_one(document)
                
            except pymongo.errors.PyMongoError as e:
                responseCode = "500 INTERNAL ERROR"  
                logging.error("Something went wrong: {0}".format(e))
                response = serverConfig.ERROR_MESSAGE
            except ValueError as e:
                responseCode = "500 INTERNAL ERROR"
                logging.error("Something went wrong: {0}".format(e)) 
                response = serverConfig.ERROR_MESSAGE       
            else:                              
                response = serverConfig.GEOFENCE_UPDATE_SUCCESSFUL_MESSAGE
            finally:                    
                serverConfig.MONGO_CLIENT.close()
                
        else:
            responseCode = "500 INTERNAL ERROR"  
            logging.error("Store geofence request: Something went wrong with the data sent by the user's request.")
            response = serverConfig.ERROR_MESSAGE
                          
    else:
        responseCode = "403 FORBIDDEN"        
        logging.warning("Someone is trying to access the server outside the app.")      
        response = serverConfig.ERROR_MESSAGE
        
    start_response(responseCode, [("Content-Type", reponseType)])
    return [response]

