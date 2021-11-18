import psutil
from psutil._common import bytes2human
from models.commands.command_model import command_model
from models.commands.command_register import command_register
import message_handler


async def ajuda(command : command_model, message, user):
    desc = ''
    for comando in command.register.allCommands:
        if not comando.optional_alias: 
            desc += f'{comando.alias} - {comando.descricao} \n'
        else:
            desc += f'{comando.optional_alias} {comando.alias} - {comando.descricao} \n'
    
    await message_handler.send_message_normal(message,user,desc)
    
  
def register(commands : command_register):
  command_model('ajuda',method=ajuda, descricao="Exibir todos os comandos e opções de ajuda", register=commands)
  