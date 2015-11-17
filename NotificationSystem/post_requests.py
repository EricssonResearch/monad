import sys
from string import *

import requests
import json

def surround_in_quotes(astring):
	return "'%s'" % astring

def send_notification(user_to_send_to,message_title_to_send,message_body_to_send):

	API_KEY='key=AIzaSyAPIZuvmfsf8TZHz3q09G_9evAmGUekdrI'
	url = 'https://gcm-http.googleapis.com/gcm/send'
        
	message_title_to_send=surround_in_quotes(message_title_to_send)
        message_body_to_send=surround_in_quotes(message_body_to_send)
	user_to_send_to=surround_in_quotes(user_to_send_to)
	print repr(message_body_to_send)
	#todo if startswith and endswith "
	print repr(message_title_to_send)
	user_to_send_to=user_to_send_to[1:-1]
	
 	custom_header={
		'Content-Type':'application/json',
		'Authorization': API_KEY
		}

	message_payload={
                'title':message_title_to_send,
                'message':message_body_to_send
                 }	

	message_body={
  		'to':user_to_send_to,
  		'data':message_payload
		}

	try:
		response=requests.post(url,data=json.dumps(message_body),headers=custom_header)
		if (response.status_code==200):
			print(response.content)
			print(response.status_code)
		else:
			print("Error with http status_code "+str(response.status_code))
	except Exception as ex:
                template = "An exception of type {0} occured. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message




if __name__ == "__main__":
	
    if len(sys.argv)!= 4:
	print 'Error in arguments'
	exit(1)	
	
    else:
	user_to_send_to=sys.argv[1]
        message_title_to_send=sys.argv[2]
        message_body_to_send=sys.argv[3]    
        send_notification(user_to_send_to,message_title_to_send,message_body_to_send)
	#exit(0)
