#!/bin/bash
sudo pkill -f bot.py &
cd /home/brutalzinn/discord/
sudo python3 bot.py &
echo 'Rodando o boberto...' &
disown