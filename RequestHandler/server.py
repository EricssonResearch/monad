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

from pymongo import errors
from datetime import datetime
from random import randint
from bson.objectid import ObjectId
#from planner import TravelPlanner, Mode


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
  			

def application(env, start_response):
	"""Get data from the client and handle them according to the type of the request"""
	data_env = env.copy()
	# Remove the query string from the request, we only accept data through POST
	data_env["QUERY_STRING"] = ""	
	data = cgi.FieldStorage(fp = env["wsgi.input"], environ = data_env)		
	
	if data_env["PATH_INFO"] == "/request":
		if ("userId" and "startTime" and "endTime" and "requestTime" and "stPosition" and "edPosition" 
			and "priority" in data):
			userId = int(escape(data.getvalue("userId")))
			startTime = escape(data.getvalue("startTime"))
			endTime = escape(data.getvalue("endTime"))
			requestTime = escape(data.getvalue("requestTime"))
			stPosition = escape(data.getvalue("stPosition"))
			edPosition = escape(data.getvalue("edPosition"))
			priority = escape(data.getvalue("priority"))	
			
			# dummy coordinates, have to update to real ones when Ilyass implements the required module
			startPositionLatitude = 59.840728
			startPositionLongitude = 17.6466147
			endPositionLatitude = 59.8758
			endPositionLongitude = 17.6627
			
			# dummy bus stops, have to update to real ones when Jens implements the required module
			startBusStop = "Polacksbacken"
			endBusStop = "Almqvistgatan"
			
			try:
				requestTime = datetime.strptime(requestTime, serverConfig.DATE_FORMAT)
				if startTime == "null":
					endTime = datetime.strptime(endTime, serverConfig.DATE_FORMAT)
				else:
					startTime = datetime.strptime(startTime, serverConfig.DATE_FORMAT)
			except ValueError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])
				logging.error("Something went wrong with the date format: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]			
			
			try:
				connection = serverConfig.MONGO_CLIENT		
				database = connection.monad
				collection = database.TravelRequest		
				document = {"userId": userId, "startTime": startTime, "endTime": endTime,
							"requestTime": requestTime, "startPositionLatitude": startPositionLatitude,
							"startPositionLongitude": startPositionLongitude, "startBusStop": startBusStop,
							"endPositionLatitude": endPositionLatitude, "endBusStop": endBusStop,
							"endPositionLongitude": endPositionLongitude}			
				result = collection.insert_one(document)
				requestId = result.inserted_id
				
				"""travelPlanner = TravelPlanner(connection)
				if priority == "distance":
					userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.tripTime)
				else:
					userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.waitTime)"""				
				
				# dummy data, have to update when Travel Planner is ready
				userTripJson = {"1": {"id": 123, "dest": "hoho"},
								"2": {"id": 456, "dest": "hihi"},
								"3": {"id": 789, "dest": "huhu"}}				
			
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]
			else:
				start_response("200 OK", [("Content-Type", "application/json")])							
				return [json.dumps(userTripJson)]
			finally:					
				connection.close()
												
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
			
	elif data_env["PATH_INFO"] == "/resetPassword":
		if "email" in data:
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
			
	elif data_env["PATH_INFO"] == "/quickRequest":
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
			
			# dummy coordinates, have to update to real ones when Ilyass implements the required module
			endPositionLatitude = 59.8758
			endPositionLongitude = 17.6627
			
			# dummy bus stops, have to update to real ones when Jens implements the required module
			startBusStop = "Polacksbacken"
			endBusStop = "Almqvistgatan"	
		
			try:
				requestTime = datetime.strptime(requestTime, serverConfig.DATE_FORMAT)
				if startTime == "null":
					endTime = datetime.strptime(endTime, serverConfig.DATE_FORMAT)
				else:
					startTime = datetime.strptime(startTime, serverConfig.DATE_FORMAT)
			except ValueError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])
				logging.error("Something went wrong with the date format: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]			
			
			try:
				connection = serverConfig.MONGO_CLIENT		
				database = connection.monad
				collection = database.TravelRequest		
				document = {"userId": userId, "startTime": startTime, "endTime": endTime,
							"requestTime": requestTime, "startPositionLatitude": startPositionLatitude,
							"startPositionLongitude": startPositionLongitude, "startBusStop": startBusStop,
							"endPositionLatitude": endPositionLatitude, "endBusStop": endBusStop,
							"endPositionLongitude": endPositionLongitude}			
				result = collection.insert_one(document)
				requestId = result.inserted_id
				
				"""travelPlanner = TravelPlanner(connection)
				if priority == "distance":
					userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.tripTime)
				else:
					userTripJson = travelPlanner.getBestRoutes(requestID = requestId, mode = Mode.waitTime)"""				
				
				# dummy data, have to update when Travel Planner is ready
				userTripJson = {"1": {"id": 123, "dest": "hoho"},
								"2": {"id": 456, "dest": "hihi"},
								"3": {"id": 789, "dest": "huhu"}}				
				
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]		
			else:
				start_response("200 OK", [("Content-Type", "application/json")])							
				return [json.dumps(userTripJson)]
			finally:					
				connection.close()										
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Quick request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
			
	elif data_env["PATH_INFO"] == "/bookingRequest":
		if "userTripId" in data:
			userTripId = escape(data.getvalue("userTripId"))			
				
			try:
				connection = serverConfig.MONGO_CLIENT		
				database = connection.monad				
				collection = database.UserTrip
				objectID = ObjectId(userTripId)				
				
				document = collection.find_one({"_id": objectID})
				requestId = document["requestId"]
				collection.update({"_id": objectID}, {"$set": {"booked": True}}, upsert = False)
				
				# We have to set the "booked" value to True for every part of the user's trip 
				# (if the trip is split into many parts)								
				document = collection.find_one({"$and": [{"_id": objectID}, {"next": {'$exists': True}}]})				
				while (document != None):
					objectID = document["next"]
					collection.update({"_id": objectID}, {"$set": {"booked": True}}, upsert = False)
					document = collection.find_one({"$and": [{"_id": objectID}, {"next": {'$exists': True}}]})	
					
				collection = database.TravelRequest
				collection.update({"_id": requestId}, {"$set": {"reservedTrip": ObjectId(userTripId)}}, upsert = False)		
				
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]		
			else:
				start_response("200 OK", [("Content-Type", "text/plain")])				
				return ["Confirmation successful, enjoy your trip!"]
			finally:					
				connection.close()
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Booking request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
			
	elif data_env["PATH_INFO"] == "/bookingCancelRequest":
		if "userTripId" in data:
			userTripId = escape(data.getvalue("userTripId"))
			
			try:
				connection = serverConfig.MONGO_CLIENT		
				database = connection.monad				
				collection = database.UserTrip
				objectID = ObjectId(userTripId)				
				
				document = collection.find_one({"_id": objectID})
				requestId = document["requestId"]
				collection.update({"_id": objectID}, {"$set": {"booked": False}}, upsert = False)
				
				# We have to set the "booked" value to False for every part of the user's cancelled trip 
				# (if the trip is split into many parts)								
				document = collection.find_one({"$and": [{"_id": objectID}, {"next": {'$exists': True}}]})				
				while (document != None):
					objectID = document["next"]
					collection.update({"_id": objectID}, {"$set": {"booked": False}}, upsert = False)
					document = collection.find_one({"$and": [{"_id": objectID}, {"next": {'$exists': True}}]})
					
				collection = database.TravelRequest
				collection.update({"_id": requestId}, {"$unset": {"reservedTrip": 1}})				
				
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return [serverConfig.ERROR_MESSAGE]		
			else:
				start_response("200 OK", [("Content-Type", "text/plain")])				
				return ["The trip has been successfully cancelled."]
			finally:					
				connection.close()
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Booking cancel request: Something went wrong with the data sent by the user's request.")
			return [serverConfig.ERROR_MESSAGE]
		
	else:
		start_response("403 FORBIDDEN", [("Content-Type", "text/plain")])
		logging.warning("Someone is trying to access the server outside the app.")		
		return [serverConfig.ERROR_MESSAGE]

