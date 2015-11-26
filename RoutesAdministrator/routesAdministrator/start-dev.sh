#!/bin/sh
exec erl \
    -pa ebin deps/*/ebin \
    -boot start_sasl \
    -sname routesAdministrator_dev \
    -s routesAdministrator \
    -s reloader
