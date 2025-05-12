#!/bin/bash
while true
do
  echo "start"
  date
  python community_benchmark.py 
  echo "done"
  date
  sleep 1200              # Sleep for 1200 seconds (20 minutes)
done
