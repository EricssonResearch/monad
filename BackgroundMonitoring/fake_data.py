from pymongo import MongoClient
import datetime
import csv
client = MongoClient('130.238.15.114')
db = client.monad1

START = datetime.datetime.now()
test1 = []
passengers = []
for i in db.UserTrip.find({}, {'userID':1, '_id':0}):
	test1.append(i['userID'])
test1 = list(set(test1))
for i in range(100):
	res = list(db.UserTrip.find({'userID':test1[i]}))
	for j in res:
		duration = 0
		for k in j['trajectory']:
			res1 = list(db.BusStop.find({'name': k}))
			if len(res1)!=0:
				passengers.append((test1[i], res1[0]['longitude'], res1[0]['latitude'], j['startTime'] + datetime.timedelta(minutes=duration)))
				duration = duration + 2
with open('passengers.csv', 'wb') as csvfile:
	spamwriter = csv.writer(csvfile, delimiter=',')
	for i in passengers:
			spamwriter.writerow([i[0], i[1], i[2], i[3]])

END = datetime.datetime.now()
print (END - START)