#!/bin/bash
pkill -f boberto.py
pip3 install -r requirements.txt --upgrade --no-deps --force-reinstall
sleep 5
python3 -u boberto.py >> error.log 2>&1 &
