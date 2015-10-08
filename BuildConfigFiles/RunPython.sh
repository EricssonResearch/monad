#!/bin/bash

cd $WORKSPACE
pwd
python -m compileall *.py
python -m compileall */*.py
python -m compileall */*/*.py
python -m compileall */*/*/*.py
python -m compileall */*/*/*/*.py


