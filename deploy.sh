#!/bin/bash
pkill -f bot
nohup python3 ./bot.py &
echo 'Rodando o boberto...'
exit 0