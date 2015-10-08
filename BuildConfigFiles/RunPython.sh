#!/bin/bash


echo $PATH

cd $WORKSPACE
pwd
python -m compileall *.py
python -m compileall */*.py
python -m compileall */*/*.py
python -m compileall */*/*/*.py
python -m compileall */*/*/*/*.py

echo $PATH
pwd
ls
