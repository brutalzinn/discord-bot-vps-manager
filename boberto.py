import config
import discord
import importlib
import os
from datetime import datetime
import pkgutil
import sys
from threading import Thread
from cronjob import Start

alias = '!b'
lastExec = datetime.today()
config.loadPermissions()
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
        author = str(message.author.id)
        comando = config.commands_handle.checkCommand(message.content.lower().replace(alias,'').split(), author)                                                              
        if comando is None:
            await message.channel.send('Esse comando não existe.') 
            return
        await comando.execute(message, self.user, client)

client = Boberto()
# try:
#     #api.app.run(port=int(os.getenv('API_PORT')),debug = True, use_reloader=True)
#     if "API" not in os.getenv("MODE"):
#         api.app.run(host="0.0.0.0", port=int(os.getenv('API_PORT')),debug = True, use_reloader=False)
#     else:
#         threading.Thread(target=lambda: api.app.run(host="0.0.0.0", port=int(os.getenv('API_PORT')),debug = False, use_reloader=False)).start()
#     config.discord_notification(f'A API de boberto iniciou com sucesso.{lastExec}!')

# except:
#     config.discord_notification(f'A API de boberto parou de funcionar.{lastExec}!')
#     pass
#Thread(target=Start).start()
#thread.join()
try:
    print(f'Boberto foi finalmente iniciado em {lastExec}!')
    config.discord_notification(f'Boberto foi finalmente iniciado em {lastExec}!')
    client.run(config.discordToken)
except:
    config.discord_notification(f'Boberto caiu na água em {datetime.today()}!')
    

