#!/bin/bash


echo $PATH

cd $WORKSPACE

python -m compileall *.py
python -m compileall */*.py
python -m compileall */*/*.py
python -m compileall */*/*/*.py
python -m compileall */*/*/*/*.py

#uncomment this when erlang script are uploaded
#erl -compile **/*.erl
