#!/bin/sh
exec erl \
    -pa ebin deps/*/ebin \
    -boot start_sasl \
    -sname authentication_dev \
    -s authentication \
    -s reloader
