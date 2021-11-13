import os
import psutil
import discord
from psutil._common import bytes2human
from minecraft import MinecraftHandleCommand
from dotenv import load_dotenv
load_dotenv()
discordToken = os.getenv('DISCORD')
#precisa refatorar tudo isso.
class statsQuery(discord.Client):
    async def on_ready(self):
        print('Logado como', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '/ram':
            mem_usage = psutil.virtual_memory()
            total_mem = bytes2human(mem_usage[0])
            used_mem = bytes2human(mem_usage[3])
            await message.channel.send(used_mem + " de " + total_mem + "RAM usada.")
            
        if 'minecraft' in message.content:
            response = MinecraftHandleCommand(message.content.split())
            await message.channel.send(response)
 
        if message.content == '/cpu':
            fetchCPU = psutil.cpu_freq()
            currCPU = str(fetchCPU[0]) 
            maxCPU = str(fetchCPU[2])
            loadAvg = str(psutil.getloadavg())
            await message.channel.send("Velocidade de clock: " + currCPU[0:1] + "." + currCPU[1:2] + "Ghz" + " de " + maxCPU[0:1] + "." + maxCPU[1:2] + "Ghz")
            await message.channel.send("Carga média: " + loadAvg)
            
client = statsQuery()
client.run(discordToken)
