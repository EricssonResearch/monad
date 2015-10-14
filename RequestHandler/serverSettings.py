import multiprocessing

bind = "127.0.0.1:2000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"
logconfig = "/home/monadsrv/Desktop/RequestHandler/logging.conf"
#accesslog = "/home/monadsrv/Desktop/RequestHandler/logs/serverAccess.log"
errorlog = "/home/monadsrv/Desktop/RequestHandler/logs/serverError.log"
backlog = 2048 # Number of requests to keep in the backlog if every worker is busy

def when_ready(server):
	print "\nServer is running..."
	
