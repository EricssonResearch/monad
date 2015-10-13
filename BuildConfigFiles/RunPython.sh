#!/bin/bash


echo $PATH

cd $WORKSPACE

python -m compileall *.py
python -m compileall */*.py
python -m compileall */*/*.py
python -m compileall */*/*/*.py
python -m compileall */*/*/*/*.py

erl -compile **/*.erl
