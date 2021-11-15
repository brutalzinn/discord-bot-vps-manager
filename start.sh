#!/bin/bash
pkill -f boberto
sleep 20
python3 -u boberto.py >> error.log 2>&1 &