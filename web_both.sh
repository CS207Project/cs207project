#!/bin/bash
trap 'kill $(jobs -p)' EXIT
export PYTHONPATH=.
./drivers/go_server.py 2>&1> .tsdb_server.log &
sleep .5 && ./drivers/go_webserver.py 2>&1> .web_server.log &
while :
do
  sleep 1
done
