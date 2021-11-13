#!/bin/bash
pkill -f bot.py -c &
echo 'bobertos mortos.' &
python3 /home/brutalzinn/discord/bot.py &
echo 'Rodando o boberto...' &
disown