#!/bin/bash
trap 'kill $(jobs -p)' EXIT
export PYTHONPATH=.
./drivers/go_server.py &
sleep .5 && ./drivers/go_client.py &
while :
do
  sleep 1
done
