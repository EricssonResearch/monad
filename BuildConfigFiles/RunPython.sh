#!/bin/bash

cd /var/lib/jenkins/jobs/"ProjectCS 2015 Development"/workspace

python -m compileall *.py
python -m compileall */*.py
python -m compileall */*/*.py
python -m compileall */*/*/*.py
python -m compileall */*/*/*/*.py

#uncomment this when erlang script are uploaded
#erl -compile **/*.erl
