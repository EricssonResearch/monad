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

import pymongo

from pymongo import MongoClient

IP_ADDRESS_OF_MONGODB = "127.0.0.1"
PORT_OF_MONGODB = 27017
# Username for mongoDB
MONGO_USER = ""
# Password for mongoDB
MONGO_PASSWORD = ""
MONGO_CLIENT = MongoClient("mongodb://" + MONGO_USER + ":" + MONGO_PASSWORD + "@" + IP_ADDRESS_OF_MONGODB, 
							PORT_OF_MONGODB, connectTimeoutMS = 5000, serverSelectionTimeoutMS = 5000)
# Name of the database
MONGO_DATABASE = MONGO_CLIENT.monad1

# Email settings, configure them according to your needs
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_ADDRESS = "test@gmail.com"
EMAIL_PASSWORD = ""
# If you change the email message, you must include "{0}" somewhere in order for the code to be sent correctly
EMAIL_MESSAGE = "This is your confirmation code: {0}. Please type it into the appropriate field."
EMAIL_SUBJECT = "Confirmation Code"

# Never change the date format without changing the appropriate java functions of the client app as well
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
ERROR_MESSAGE = "Something went wrong, please try again in a few minutes."
FEEDBACK_UPDATE_SUCCESSFUL_MESSAGE = "Thank you for your feedback!"
GEOFENCE_UPDATE_SUCCESSFUL_MESSAGE = "Thank you for the info!"

BOOKING_SUCCESSFUL_MESSAGE = "Confirmation successful, enjoy your trip!"
BOOKING_CANCEL_SUCCESSFUL_MESSAGE = "The trip has been successfully cancelled."
BOOKING_DOUBLE_MESSAGE = "You have already booked this trip."
NUMBER_OF_DAYS_TO_KEEP_USER_BOOKINGS = 2

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

