#!/bin/bash

cd ..
pwd
python -m compileall *.py
python -m compileall */*.py
python -m compileall /*/*.py
