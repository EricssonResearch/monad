from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
import datetime

def start(host):
    global mongo_client
    global db
    global bus_trip_collection
    global bus_stop_collection

    mongo_client = MongoClient(host, 27017)
    db = mongo_client.monad1
    bus_trip_collection = db.BusTrip
    bus_stop_collection = db.BusStop

def vehicle_get_next_trip(bus_id):
    trips = list(bus_trip_collection.find({'busID' : bus_id}))
    now = datetime.datetime.now()# - datetime.timedelta(days = 1)

    min = datetime.timedelta(weeks = 1)

    for trip in trips:
        if now < trip['startTime']:

            if trip['startTime'] - now < min:
                min = trip['startTime'] - now
                nearest_trip = trip

    # print min
    # print nearest_trip['startTime']

    if nearest_trip is None:
        return -1

    trajectory = nearest_trip['trajectory']

    # print trajectory[0]['busStop']
    # print bus_stop_collection.find_one({'_id' : ObjectId(trajectory[0]['busStop'])})

    for trajectory_point in trajectory:
        trajectory_point['busStop']= bus_stop_collection.find_one({'_id' : ObjectId(trajectory_point['busStop'])})

    # print nearest_trip['trajectory']

    return dumps(nearest_trip)

# if __name__ == "__main__":
#     start("130.238.15.114")
#     get_current_bus_trip(1)

def send_notification_binary(user_to_send_to, message_title, message_body):
	message_title_to_send = ''.join([chr(c) for c in message_title])
	message_body_to_send = ''.join([chr(c) for c in message_body])
	send_notification(user_to_send_to, message_title_to_send, message_body_to_send)

def send_notification(user_to_send_to, message_title_to_send, message_body_to_send):
    API_KEY='key=AIzaSyAPIZuvmfsf8TZHz3q09G_9evAmGUekdrI'
    url = 'https://gcm-http.googleapis.com/gcm/send'

    message_title_to_send = surround_in_quotes(message_title_to_send)
    message_body_to_send = surround_in_quotes(message_body_to_send)
    user_to_send_to = surround_in_quotes(user_to_send_to)

    # print repr(message_body_to_send)
    # print repr(message_title_to_send)

    user_to_send_to = user_to_send_to[1:-1]

    custom_header = {
        'Content-Type' : 'application/json',
        'Authorization' : API_KEY
    }

    message_payload = {
        'title' : message_title_to_send,
        'message' : message_body_to_send
    }

    message_body = {
        'to' : user_to_send_to,
        'data' : message_payload
    }

    try:
        response = requests.post(url, headers = custom_header, data = json.dumps(message_body))

        if (response.status_code == 200):
            print(response.content)
            print(response.status_code)
        else:
            print("Error with http status_code " + str(response.status_code))
    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message
