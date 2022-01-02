#!/bin/bash
pkill -f boberto.py
python -m pip install -r requirements.txt --user
sleep 5
python -u boberto.py >> error.log 2>&1 &