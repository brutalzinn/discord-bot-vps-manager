import os
import psutil
import discord
from psutil._common import bytes2human
from minecraft import MinecraftHandleCommand
from datetime import datetime
from dotenv import load_dotenv
from models.permissions.permission_handler import permission_handler

from models.permissions.permission_model import permission_model
from models.permissions.permission_register import permission_register

load_dotenv()
discordToken = os.getenv('DISCORD')
filename = 'whitelist.txt'
alias = 'b!'
lastExec = datetime.today()
perm_register = permission_register()
perm_handler = permission_handler(perm_register)
#precisa refatorar tudo isso.
with open(filename) as file:
    for line in file:
        line_splited = line.rstrip().split(',')
        user = permission_model(line_splited[0], line_splited[1])
        perm_register.add_user_permission(user)
class statsQuery(discord.Client):

    async def on_message(self, message):
        if message.author == self.user: return
        if not alias in message.content: return
        channel = message.channel
        author = message.author
        if not perm_handler.check_permission(author):
            await message.channel.send(f"Você não tem permissão para falar comigo. Sorry :(")
            return
            
        print(f'canal:{channel} - autor:{author}')
        
        if 'info' in message.content:
            await message.channel.send(f"TESTANDO")
            await message.channel.send(f"Iniciado em :{lastExec}")
            for group in self.private_channels:
                print(group)
       
        if  'ram' in message.content:
            mem_usage = psutil.virtual_memory()
            total_mem = bytes2human(mem_usage[0])
            used_mem = bytes2human(mem_usage[3])
            await message.channel.send(used_mem + " de " + total_mem + " RAM usada.")
            
        if  'minecraft' in message.content:
            response = MinecraftHandleCommand(message, perm_handler)
            await message.channel.send(response)
 
        if 'cpu' in message.content:
            fetchCPU = psutil.cpu_freq()
            currCPU = str(fetchCPU[0]) 
            maxCPU = str(fetchCPU[2])
            loadAvg = str(psutil.getloadavg())
            await message.channel.send("Velocidade de clock: " + currCPU[0:1] + "." + currCPU[1:2] + "Ghz" + " de " + maxCPU[0:1] + "." + maxCPU[1:2] + "Ghz")
            await message.channel.send("Carga média: " + loadAvg)
            
client = statsQuery()
client.run(discordToken)
