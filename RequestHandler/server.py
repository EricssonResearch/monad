import cgi
import logging
import pymongo
import smtplib

from pymongo import MongoClient
from pymongo import errors
from datetime import datetime
from random import randint

IP_ADDRESS_OF_MONGODB = "localhost"
PORT_OF_MONGODB = 27017

escape_table = {
	"&": "",
	'"': "",
	"'": "",
	">": "",
	"<": "",
	"$": "",
	";": "",
	"{": "",
	"}": "",
	"\\": "",
	",": ""	
}


def escape(text):
	"""Replace dangerous characters with blanks"""
	return "".join(escape_table.get(c,c) for c in text)
	
def send_email(from_addr, to_addr_list, subject, message): 
	header  = "From: {0}\n".format(from_addr)
	header += "To: %s\n" % ",".join(to_addr_list)    
	header += "Subject: {0}\n\n".format(subject)
	message = header + message
 
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login("", "")
	problems = server.sendmail(from_addr, to_addr_list, message)
	server.quit()
	

def insert_one_document(collection, document):
	"""Insert a single document in a collection"""
  	collection.insert_one(document)
  			

def application(env, start_response):
	"""Get data from the client and insert them into the database"""
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
		
			try:
				requestTime = datetime.strptime(requestTime, "%Y %a %d %b %H:%M")
				if startTime == "null":
					endTime = datetime.strptime(endTime, "%Y %a %d %b %H:%M")
				else:
					startTime = datetime.strptime(startTime, "%Y %a %d %b %H:%M")
			except ValueError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])
				logging.error("Something went wrong with the date format: {0}".format(e))
				return ["Something went wrong, please try again. We are sorry for the inconvenience."]			
			
			try:
				connection = MongoClient(IP_ADDRESS_OF_MONGODB, PORT_OF_MONGODB, connectTimeoutMS = 5000, 
										serverSelectionTimeoutMS = 5000)		
				database = connection.monad
				collection = database.TravelRequest		
				document = {"userId": userId, "startTime": startTime, "endTime": endTime,
							"requestTime": requestTime, "stPosition": stPosition, "edPosition": edPosition}			
				insert_one_document(collection, document)
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return ["Something went wrong, please try again. We are sorry for the inconvenience."]		
			else:
				start_response("200 OK", [("Content-Type", "text/plain")])				
				return ["Data successfully written in the database! Go Mo.N.A.D team!"]
			finally:					
				connection.close()										
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Request: Something went wrong with the data sent by the user's request.")
			return ["Something went wrong, please try again. We are sorry for the inconvenience."]
			
	elif data_env["PATH_INFO"] == "/resetPassword":
		if "email" in data:
			email = escape(data.getvalue("email"))			
			email_list = [email]			
			code = randint(1000, 9999)
			message = "This is your confirmation code: {0}. Please type it into the appropriate field.".format(code)
			send_email("project.monad2015@gmail.com", email_list, "Confirmation Code", message)
			
			start_response("200 OK", [("Content-Type", "text/plain")])				
			return ["{0}".format(code)]
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Reset Password: Something went wrong with the data sent by the user's request.")
			return ["Something went wrong, please try again. We are sorry for the inconvenience."]
			
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
		
			try:
				requestTime = datetime.strptime(requestTime, "%Y %a %d %b %H:%M")
				if startTime == "null":
					endTime = datetime.strptime(endTime, "%Y %a %d %b %H:%M")
				else:
					startTime = datetime.strptime(startTime, "%Y %a %d %b %H:%M")
			except ValueError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])
				logging.error("Something went wrong with the date format: {0}".format(e))
				return ["Something went wrong, please try again. We are sorry for the inconvenience."]			
			
			try:
				connection = MongoClient(IP_ADDRESS_OF_MONGODB, PORT_OF_MONGODB, connectTimeoutMS = 5000, 
										serverSelectionTimeoutMS = 5000)		
				database = connection.monad
				collection = database.TravelRequest		
				document = {"userId": userId, "startTime": startTime, "endTime": endTime,
							"requestTime": requestTime, "startPositionLatitude": startPositionLatitude,
							"startPositionLongitude": startPositionLongitude, "edPosition": edPosition}			
				insert_one_document(collection, document)
			except pymongo.errors.PyMongoError as e:
				start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
				logging.error("Something went wrong: {0}".format(e))
				return ["Something went wrong, please try again. We are sorry for the inconvenience."]		
			else:
				start_response("200 OK", [("Content-Type", "text/plain")])				
				return ["Data successfully written in the database! Go Mo.N.A.D team!"]
			finally:					
				connection.close()										
		else:
			start_response("500 INTERNAL ERROR", [("Content-Type", "text/plain")])	
			logging.error("Quick request: Something went wrong with the data sent by the user's request.")
			return ["Something went wrong, please try again. We are sorry for the inconvenience."]
			
	else:
		start_response("403 FORBIDDEN", [("Content-Type", "text/plain")])
		logging.warning("Someone is trying to access the server outside the app.")		
		return ["Something went wrong, please try again. We are sorry for the inconvenience."]

