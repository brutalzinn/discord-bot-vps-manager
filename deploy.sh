#!/bin/bash
pkill -f bot.py &
cd /home/brutalzinn/discord/
python3 bot.py &
echo 'Rodando o boberto...' &
disown