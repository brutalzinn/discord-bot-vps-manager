import os
import discord
from minecraft import MinecraftHandleCommand
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

from models.commands.command_handler import command_handler
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from models.permissions.permission_handler import permission_handler
import requests
from models.permissions.permission_model import permission_model
from models.permissions.permission_register import permission_register
from chat_comandos.infra import cpu


load_dotenv()
discordToken = os.getenv('DISCORD_TOKEN')
discordUrl = os.getenv('DISCORD_URL')
filename = 'whitelist.txt'
alias = 'b!'
lastExec = datetime.today()
#permissões
perm_register = permission_register()
perm_handler = permission_handler(perm_register)
#comandos

commands_register = command_register()
commands_handle = command_handler(commands_register)
command_model('cpu', 1,0, cpu, register=commands_register)
#precisa refatorar tudo isso.

with open(filename) as file:
    for line in file:
        line_splited = line.rstrip().split(',')
        user = permission_model(line_splited[0], line_splited[1])
        perm_register.add_user_permission(user)

class statsQuery(discord.Client):

    async def on_message(self, message):
        if message.author == self.user: return
        # if not alias in message.content: return
        # channel = message.channel
        # author = message.author
        # if not perm_handler.check_permission(author):
        #     await message.channel.send(f"Você não tem permissão para falar comigo. Sorry :(")
        #     return
        print(message.content.split())
        commands_handle.checkCommand(message.content.split())  
        # print(f'canal:{channel} - autor:{author}')
        
        # if 'info' in message.content:
        #     await message.channel.send(f"TESTANDO")
        #     await message.channel.send(f"Iniciado em :{lastExec}")
        #     for group in self.private_channels:
        #         print(group)
       
        # if  'ram' in message.content:
        #     mem_usage = psutil.virtual_memory()
        #     total_mem = bytes2human(mem_usage[0])
        #     used_mem = bytes2human(mem_usage[3])
        #     await message.channel.send(used_mem + " de " + total_mem + " RAM usada.")
            
        # if  'minecraft' in message.content:
        #     response = MinecraftHandleCommand(message, perm_handler)
        #     await message.channel.send(response)
 
        # if 'cpu' in message.content:
        #     fetchCPU = psutil.cpu_freq()
        #     currCPU = str(fetchCPU[0]) 
        #     maxCPU = str(fetchCPU[2])
        #     loadAvg = str(psutil.getloadavg())
        #     await message.channel.send("Velocidade de clock: " + currCPU[0:1] + "." + currCPU[1:2] + "Ghz" + " de " + maxCPU[0:1] + "." + maxCPU[1:2] + "Ghz")
        #     await message.channel.send("Carga média: " + loadAvg)

def discord_notification(message):   
    myobj = {'content': message}
    #requests.post(discordUrl, data = myobj)
    
client = statsQuery()
try:
    discord_notification(f'Boberto iniciado em {lastExec}')
    client.run(discordToken)
except:
    discord_notification(f'Boberto caiu na água em {lastExec}')
