#!/bin/bash
pkill -f bot.py
nohup python3 ./bot.py &
echo 'Rodando o boberto...'