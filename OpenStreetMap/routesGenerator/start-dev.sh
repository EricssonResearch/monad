#!/bin/sh
exec erl \
    -pa ebin deps/*/ebin \
    -boot start_sasl \
    -sname routesGenerator_dev \
    -s routesGenerator \
    -s reloader
