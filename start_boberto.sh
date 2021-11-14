#!/bin/bash
pkill -f bot
sleep 20
python3 -u bot.py >> error.log 2>&1 &