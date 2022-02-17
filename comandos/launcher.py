import psutil
import message_handler
from psutil._common import bytes2human
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from models.commands.command_args import command_args
from models.commands.command_args_register import command_args_register


async def download(command : command_model, message, user, client):
    resultado = ''
    is_show_command = False
    new_args = command.args[1:]
    await message_handler.send_message_normal(message,  user,   resultado)
    
  
def register(commands : command_register):
    args_register = command_args_register()
    args_register.addArg(command_args(unique_id='nome_comando', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.'))
    command_model('download', method=download, descricao="Exibir todos os comandos e opções de ajuda", register=commands, command_args=args_register)
  