#!/bin/bash
pkill -f boberto
sleep 1
nohup python3 -u boberto.py >> error.log 2>&1 &