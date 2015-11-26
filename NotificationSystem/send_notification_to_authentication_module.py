import requests

AUTHENTICATION_MODULE_HOST = 'http://130.238.15.114:'
AUTHENTICATION_MODULE_PORT = '9999'

def send_notification_to_authentication(user_id, message_title, message_body):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    url = AUTHENTICATION_MODULE_HOST + AUTHENTICATION_MODULE_PORT + '/send_notification'
    data = {'user_id': user_id, 'message_title': message_title, 'message_body': message_body}
    requests.post(url, headers = headers, data = data)

