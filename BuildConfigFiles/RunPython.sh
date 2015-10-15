#!/bin/bash

cd /var/lib/jenkins/jobs/"ProjectCS 2015 Development"/workspace

python -m compileall -f -q ./
python -m pytest --junitxml pythonResults.xml

#uncomment this when erlang script are uploaded
#erl -compile **/*.erl
