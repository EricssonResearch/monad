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
	
