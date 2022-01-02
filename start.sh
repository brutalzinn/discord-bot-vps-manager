#!/bin/bash
pkill -f boberto.py
python3 -m pip install -r requirements.txt --user
sleep 5
python3 -u boberto.py >> error.log 2>&1 &
