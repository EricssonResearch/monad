import cgi
import logging
import pymongo

from pymongo import MongoClient
from pymongo import errors

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
   

def insert_one_document(collection, document):
	"""Insert a single document in a collection"""
  	collection.insert_one(document)
  			

def application(env, start_response):
	"""Get data from the client and insert them into the database"""
	data_env = env.copy()
	# Remove the query string from the request, we only accept data through POST
	data_env["QUERY_STRING"] = ""
	data = cgi.FieldStorage(fp = env["wsgi.input"], environ = data_env)		
	
	if "userId" and "startTime" and "endTime" and "requestTime" and "stPosition" and "edPosition" in data:
		userId = int(escape(data.getvalue("userId")))
		startTime = escape(data.getvalue("startTime"))
		endTime = escape(data.getvalue("endTime"))
		requestTime = escape(data.getvalue("requestTime"))
		stPosition = escape(data.getvalue("stPosition"))
		edPosition = escape(data.getvalue("edPosition"))		
			
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
		start_response("403 FORBIDDEN", [("Content-Type", "text/plain")])
		logging.warning("Someone is trying to access the server outside the app.")		
		return ["Something went wrong, please try again. We are sorry for the inconvenience."]

