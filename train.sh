#!/bin/bash
while true
do
  echo "start"
  date
  python training_bot.py 
  echo "done"
  date
  sleep 1              # Sleep for 1200 seconds (15 minutes)
done
