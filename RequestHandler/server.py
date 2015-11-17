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
import logging
import pymongo
import smtplib
import json
import serverConfig
import requests

from pymongo import errors
from datetime import datetime
from random import randint
from bson.objectid import ObjectId
from planner import TravelPlanner, Mode
from routeGenerator import string_to_coordinates, coordinates_to_nearest_stop


def escape(text):
	"""Replace dangerous characters with blanks"""
	return "".join(serverConfig.escape_table.get(c,c) for c in text)
	
	
def send_email(from_addr, to_addr_list, subject, message): 
	"""Send an email"""
	header  = "From: {0}\n".format(from_addr)
	header += "To: %s\n" % ",".join(to_addr_list)    
	header += "Subject: {0}\n\n".format(subject)
	message = header + message
 
	server = smtplib.SMTP(serverConfig.EMAIL_HOST, serverConfig.EMAIL_PORT)
	server.starttls()
	server.login(serverConfig.EMAIL_ADDRESS, serverConfig.EMAIL_PASSWORD)
	server.sendmail(from_addr, to_addr_list, message)
	server.quit()
	
	
def generate_notification(user_id, booked_trip_id):    
	url = serverConfig.NOTIFICATIONS_SERVER
	headers = {'Content-type': 'application/x-www-form-urlencoded'}
	data = {"userID" : str(user_id), "bookedTripID" : str(booked_trip_id)}	
	requests.post(url, data = data, headers = headers) 
	  			

def application(env, start_response):
	"""Get data from the client and handle them according to the type of the request"""
	data_env = env.copy()
	# Remove the query string from the request, we only accept data through POST
	data_env["QUERY_STRING"] = ""	
	data = cgi.FieldStorage(fp = env["wsgi.input"], environ = data_env)		
	
	if (data_env["PATH_INFO"] == "/request"):
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
			
			if (stPosition != "Current Position"):
				coordinates = string_to_coordinates(stPosition)
				if ((coordinates["latitude"] == None) or (coordinates["longitude"] == None)):
					start_response("200 OK", [("Content-Type", "application/json")])							
					return [json.dumps({})]
				else:
					startPositionLatitude = coordinates["latitude"]
					startPositionLongitude = coordinates["longitude"]														
			stop = coordinates_to_nearest_stop(startPositionLongitude, startPositionLatitude)
			startStop = stop["name"]
			
			coordinates = string_to_coordinates(edPosition)
			if (coordinates["latitude"] == None or coordinates["longitude"] == None):
				start_response("200 OK", [("Content-Type", "application/json")])							
				return [json.dumps({})]
			else:
				endPositionLatitude = coordinates["latitude"]
				endPositionLongitude = coordinates["longitude"]
			stop = coordinates_to_nearest_stop(endPositionLongitude, endPositionLatitude)
			endStop = stop["name"]			
			
			try:
				requestTime = datetime.strptime(requestTime, serverConfig.DATE_FORMAT)
				if (startTime == "null"):
					endTime = datetime.strptime(endTime, serverConfig.DATE_FORMAT)
				elif (endTime == "null"):
					startTime = datetime.strptime(startTime, serverConfig.DATE_FORMAT)
			except ValueError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])
				logging.error("Something went wrong with the date format: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]			
			
			try:						
				database = serverConfig.MONGO_DATABASE
				collection = database.BusStop
				
				stop1 = collection.find_one({"name": startStop})
				stop2 = collection.find_one({"name": endStop})
				if (stop1 != None and stop2 != None):
					startBusStop = stop1["_id"]
					endBusStop = stop2["_id"]
				else:
					start_response("200 OK", [("Content-Type", "application/json")])							
					return [json.dumps({})]
				
				collection = database.TravelRequest		
				document = {"userID": userId, "startTime": startTime, "endTime": endTime,
							"requestTime": requestTime, "startPositionLatitude": startPositionLatitude,
							"startPositionLongitude": startPositionLongitude, "startBusStop": startBusStop,
							"endPositionLatitude": endPositionLatitude, "endBusStop": endBusStop,
							"endPositionLongitude": endPositionLongitude}			
				result = collection.insert_one(document)
				requestId = result.inserted_id
				
				travelPlanner = TravelPlanner(database)
				if (priority == "distance"):
					userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.tripTime)
				else:
					userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.waitTime)
				
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]
			else:
				start_response("200 OK", [("Content-Type", "application/json")])							
				return [json.dumps(userTripJson)]
			finally:					
				serverConfig.MONGO_CLIENT.close()
												
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
			
	elif (data_env["PATH_INFO"] == "/resetPassword"):
		if ("email" in data):
			email = data.getvalue("email")			
			email_list = [email]			
			code = randint(1000, 9999)
			message = serverConfig.EMAIL_MESSAGE.format(code)
			send_email(serverConfig.EMAIL_ADDRESS, email_list, serverConfig.EMAIL_SUBJECT, message)
			
			start_response("200 OK", [("Content-Type", "text/plain")])				
			return ["{0}".format(code)]
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Reset Password: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
			
	elif (data_env["PATH_INFO"] == "/quickRequest"):
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
																	
			stop = coordinates_to_nearest_stop(startPositionLongitude, startPositionLatitude)			
			startStop = stop["name"]
			
			coordinates = string_to_coordinates(edPosition)
			if (coordinates["latitude"] == None or coordinates["longitude"] == None):
				start_response("200 OK", [("Content-Type", "application/json")])							
				return [json.dumps({})]
			else:
				endPositionLatitude = coordinates["latitude"]
				endPositionLongitude = coordinates["longitude"]
			stop = coordinates_to_nearest_stop(endPositionLongitude, endPositionLatitude)
			endStop = stop["name"]
		
			try:
				requestTime = datetime.strptime(requestTime, serverConfig.DATE_FORMAT)
				if (startTime == "null"):
					endTime = datetime.strptime(endTime, serverConfig.DATE_FORMAT)
				elif (endTime == "null"):
					startTime = datetime.strptime(startTime, serverConfig.DATE_FORMAT)
			except ValueError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])
				logging.error("Something went wrong with the date format: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]			
			
			try:						
				database = serverConfig.MONGO_DATABASE
				collection = database.BusStop
				
				stop1 = collection.find_one({"name": startStop})
				stop2 = collection.find_one({"name": endStop})
				if (stop1 != None and stop2 != None):
					startBusStop = stop1["_id"]
					endBusStop = stop2["_id"]
				else:
					start_response("200 OK", [("Content-Type", "application/json")])							
					return [json.dumps({})]
				
				collection = database.TravelRequest		
				document = {"userID": userId, "startTime": startTime, "endTime": endTime,
							"requestTime": requestTime, "startPositionLatitude": startPositionLatitude,
							"startPositionLongitude": startPositionLongitude, "startBusStop": startBusStop,
							"endPositionLatitude": endPositionLatitude, "endBusStop": endBusStop,
							"endPositionLongitude": endPositionLongitude}			
				result = collection.insert_one(document)
				requestId = result.inserted_id
				
				travelPlanner = TravelPlanner(database)
				if (priority == "distance"):
					userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.tripTime)
				else:
					userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.waitTime)											
				
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]		
			else:
				start_response("200 OK", [("Content-Type", "application/json")])							
				return [json.dumps(userTripJson)]
			finally:					
				serverConfig.MONGO_CLIENT.close()										
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Quick request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
			
	elif (data_env["PATH_INFO"] == "/bookingRequest"):
		if ("userTripId" in data):
			userTripId = escape(data.getvalue("userTripId"))			
				
			try:						
				database = serverConfig.MONGO_DATABASE				
				collection = database.UserTrip
				objectID = ObjectId(userTripId)				
				
				document = collection.find_one({"_id": objectID})
				#requestId = document["requestID"]
				userId = document["userID"]
				collection.update({"_id": objectID}, {"$set": {"booked": True}}, upsert = False)
				partialTrips = []
				partialTrips.append(objectID)
				
				# We have to set the "booked" value to True for every part of the user's trip 
				# (if the trip is split into many parts)								
				document = collection.find_one({"$and": [{"_id": objectID}, {"next": {'$exists': True}}]})				
				while (document != None):
					objectID = document["next"]
					partialTrips.append(objectID)
					collection.update({"_id": objectID}, {"$set": {"booked": True}}, upsert = False)
					document = collection.find_one({"$and": [{"_id": objectID}, {"next": {'$exists': True}}]})	
					
				collection = database.BookedTrip
				document = {"userID": userId, "partialTrips": partialTrips}
				booked_trip_id = collection.insert_one(document).inserted_id
					
				"""collection = database.TravelRequest
				collection.update({"_id": requestId}, {"$set": {"reservedTrip": ObjectId(userTripId)}}, upsert = False)"""
				
				generate_notification(userId, booked_trip_id)				
				
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]
			except Exception as e:
				logging.error("Something went wrong with the notification: {0}".format(e))		
			else:
				start_response("200 OK", [("Content-Type", "text/plain")])				
				return [serverConfig.BOOKING_SUCCESSFUL_MESSAGE]
			finally:					
				serverConfig.MONGO_CLIENT.close()
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Booking request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
			
	elif (data_env["PATH_INFO"] == "/bookingCancelRequest"):
		if ("userTripId" in data):
			userTripId = escape(data.getvalue("userTripId"))
			
			try:						
				database = serverConfig.MONGO_DATABASE				
				collection = database.UserTrip
				objectID = ObjectId(userTripId)
				
				document = collection.find_one({"_id": objectID})
				#requestId = document["requestID"]
				userId = document["userID"]
				collection.update({"_id": objectID}, {"$set": {"booked": False}}, upsert = False)
				
				collection = database.BookedTrip
				bookedTrips = collection.find({"userID": userId})
				for bookedTrip in bookedTrips:
					partialTrips = bookedTrip["partialTrips"]
					if (partialTrips[0] == objectID):
						collection.delete_one({"_id": bookedTrip["_id"]})
						break
						
				collection = database.UserTrip				
				# We have to set the "booked" value to False for every part of the user's cancelled trip 
				# (if the trip is split into many parts)								
				document = collection.find_one({"$and": [{"_id": objectID}, {"next": {'$exists': True}}]})				
				while (document != None):
					objectID = document["next"]
					collection.update({"_id": objectID}, {"$set": {"booked": False}}, upsert = False)
					document = collection.find_one({"$and": [{"_id": objectID}, {"next": {'$exists': True}}]})
					
				"""collection = database.TravelRequest				
				collection.update({"_id": requestId}, {"$unset": {"reservedTrip": 1}})"""				
				
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]		
			else:
				start_response("200 OK", [("Content-Type", "text/plain")])				
				return [serverConfig.BOOKING_CANCEL_SUCCESSFUL_MESSAGE]
			finally:					
				serverConfig.MONGO_CLIENT.close()
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Booking cancel request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
	
	elif (data_env["PATH_INFO"] == "/getUserBookingsRequest"):
		if ("userId" in data):
			userId = int(escape(data.getvalue("userId")))
		
			try:						
				database = serverConfig.MONGO_DATABASE				
				collection = database.BookedTrip
				
				userTripJson = {}
				i = 0
				bookedTrips = collection.find({"userID": userId})
				collection = database.UserTrip
				for bookedTrip in bookedTrips:
					partialTripIDs = bookedTrip["partialTrips"]
					partialTrips = []
					
					# Delete bookings more than the specified days old
					cursor = collection.find_one({"_id": partialTripIDs[0]})
					if ((datetime.now() - cursor["startTime"]).days 
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
							requestTime = str(datetime.now())													
							requestID = "null"																									
						partialTrip = {
							"_id": str(partialTripCursor["_id"]),
							"userID" : partialTripCursor["userID"],
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
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]		
			else:
				start_response("200 OK", [("Content-Type", "application/json")])							
				return [json.dumps(userTripJson)]
			finally:					
				serverConfig.MONGO_CLIENT.close()
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Get user bookings request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
			
	else:
		start_response("403 FORBIDDEN", [("Content-Type", "text/plain")])
		logging.warning("Someone is trying to access the server outside the app.")		
		return [serverConfig.ERROR_MESSAGE]

