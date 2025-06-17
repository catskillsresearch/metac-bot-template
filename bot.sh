#!/bin/bash -x
while true
do
  echo "start"
  date
  python catskills_bot.py 
  echo "done"
  date
  sleep 1200              # Sleep for 1200 seconds (15 minutes)
done
