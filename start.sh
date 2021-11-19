#!/bin/bash
pkill -f boberto.py
sleep 5
python3.9 -u boberto.py >> error.log 2>&1 &
