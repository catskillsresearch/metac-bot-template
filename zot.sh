#!/bin/bash -x
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
while true
do
  echo "start"
  date
  python forecast_open_questions.py 
  echo "done"
  date
done
