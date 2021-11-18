import discord
import config
import requests
import importlib
import os
from datetime import datetime
from dotenv import load_dotenv
import pkgutil
import sys
load_dotenv()
alias = 'b!'
lastExec = datetime.today()
discordToken = os.getenv('DISCORD_TOKEN')
discordUrl = os.getenv('DISCORD_URL')
def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            module = importlib.import_module(full_package_name)
            module.register(config.commands_register)
load_all_modules_from_dir('comandos')

class Boberto(discord.Client):
    async def on_message(self, message):
        if message.author == self.user: return
        if not alias in message.content.lower(): return
        author = str(message.author).lower()
        print(author)
        comando = config.commands_handle.checkCommand(message.content.lower().replace(alias,'').split(), author)                                                              
        if comando is None:
            await message.channel.send('Esse comando não existe.') 
            return

        await comando.execute(message, self.user)

        # if not comando.private:
        #     await message.channel.send(resposta)
        #     return

        # if isinstance(message.channel, discord.channel.DMChannel) and message.author != self.user:
        #     await message.channel.send(resposta)

        #await message.channel.send(f'Privada: {resposta}')
        

       

def discord_notification(message):   
    myobj = {'content': message}
  #  requests.post(discordUrl, data = myobj)
client = Boberto()
try:
    discord_notification(f'Boberto iniciado em {lastExec}')
    client.run(discordToken)
except:
    discord_notification(f'Boberto caiu na água em {lastExec}')
    

