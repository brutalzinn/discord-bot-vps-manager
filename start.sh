#!/bin/bash
nohup pkill -f boberto &
sleep 1 & 
python3 -u boberto.py >> error.log 2>&1 &