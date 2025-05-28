#!/bin/bash
sleep 6000
while true
do
  echo "start"
  date
  python training_bot.py 
  echo "done"
  date
  sleep 120
done
