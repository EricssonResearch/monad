import json
import bson
import pymongo
import datetime
import time
import threading
import requests

from bson.objectid import ObjectId
from datetime import datetime
from time import gmtime, strftime, strptime
from pymongo import MongoClient
from datetime import datetime, timedelta


IP_ADDRESS_OF_MONGODB = "130.238.15.114"
PORT_OF_MONGODB = 27017

AUTHENTICATION_MODULE_HOST = 'http://130.238.15.114:'
AUTHENTICATION_MODULE_PORT = '9999'

client = MongoClient("130.238.15.114",27017)

db = client.monad
coll = db.UserTrip


def send_notification_to_authentication(user_id, message_title, message_body):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    url = AUTHENTICATION_MODULE_HOST + AUTHENTICATION_MODULE_PORT + '/send_notification'
    data = {'user_id': user_id, 'message_title': message_title, 'message_body': message_body}
    requests.post(url, headers = headers, data = data)


#step1: Pending Request(Get query continuesly every 60 min)
def RetrieveDB():
    threading.Timer(180.0, RetrieveDB).start()
    cursor = db.UserTrip.find({"feedback":-1},{"endTime" : 1 , "_id" : 0})
    for document in cursor:
    #Step2: Ask for feedback (call function from Notification Module)
        scurrent = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        currentTime = datetime.strptime(scurrent,"%Y-%m-%d %H:%M:%S")
        print currentTime
        print document
        documentStr = str(document)
        dateYear = documentStr[31:-18]
        dateMonth = documentStr[37:-14]
        dateDay = documentStr[41:-10]
        print dateYear
        print dateMonth
        print dateDay
        date = dateYear + "-" + dateMonth + "-" + dateDay
        print date
        timeHour = documentStr[45:-6]
        timeMinute = documentStr[50:-2]
        time = timeHour + ":" + timeMinute
        print timeHour
        print timeMinute
        print time

        dt = date + " " + time
        print dt
        destinationTime = datetime.strptime(dt,"%Y-%m-%d %H:%M")
        print destinationTime

        print type(destinationTime)
        diff = currentTime - destinationTime
        print diff
 
   	 """ The feedback request should be send after endTime"""
   		if (diff) > timedelta(seconds = 100):
   			send_notification_to_authentication()

RetrieveDB()

#Step 3: Receive feedbacks comming from client-app

#step4: Store the feedbacks coming from client-app

client.close()

