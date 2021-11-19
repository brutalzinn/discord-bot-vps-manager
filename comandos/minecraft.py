from models.commands.command_args import command_args
from models.commands.command_args_register import command_args_register
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from container_manager import list_container, start_container, stop_container, create_container
from mcstatus import MinecraftServer
import message_handler
import os
from pathlib import Path


async def status(command : command_model, message):
    try:
        server = MinecraftServer.lookup("127.0.0.1:25565")
        status = server.status()
        return "O servidor tem {0} jogadores jogando com {1} ms".format(status.players.online, status.latency)
    except(ConnectionRefusedError):
        return "O servidor está offline ou não responde."
    
async def list(command : command_model, message):
    return list_container()

async def stop(command : command_model, message, user):          
    if stop_container('boberto-database'):
        return f"Parando servidor.. boberto-database"
    else:
        return f"Ocorreu um erro ao parar servidor boberto-database .."
  
async def start(command : command_model, message):
    if start_container(command.args[2]):
        return f"Iniciando servidor.. {command.args[2]}"
    else:
        return f"Ocorreu um erro ao iniciar servidor {command.args[2]} .."

async def create(command : command_model, message, user):
    environment = {"EULA": "TRUE", "TYPE": "FORGE", "VERSION": "1.16.5", "FORGEVERSION": "36.1.32", "ONLINE_MODE": "FALSE"}
    new_args = command.args[2:]
    print(new_args)
    nome = new_args[command.command_args.get_arg_unique('nome').index]     
    porta = new_args[command.command_args.get_arg_unique('porta').index]     
    versao = new_args[command.command_args.get_arg_unique('versao').index]     
    versaoforge = new_args[command.command_args.get_arg_unique('versaoforge').index]     
    await message_handler.send_message_normal(message,  user, f'Criando servidor {nome} ..')


    root_directory = Path(__file__).parent.parent
    arquivos = os.path.join(root_directory,'web','data')
    if not os.path.isdir(arquivos):
        os.mkdir(arquivos)
    server_path = os.path.join(arquivos, nome)
    if not os.path.isdir(server_path):
        os.mkdir(server_path)
        await message_handler.send_message_normal(message,  user, f'Preparando servidor {nome}')

    environment['FORGEVERSION'] = versaoforge
    environment['VERSION'] = versao
    resultado = create_container(server_path,nome,porta,environment)
    if resultado['status']:
        await message_handler.send_message_normal(message,  user, f'Servidor criado.. {nome}')
    else:
        await message_handler.send_message_normal(message,  user, resultado['mensagem'])

def register(commands : command_register):
  command_model(optional_alias='minecraft', alias='status',descricao="Exibir status do servidor de minecraft \n uso: minecraft status <nome>", method=status, register=commands)
  command_model(optional_alias='minecraft', alias='list', descricao="Exibir uma lista de servidores de minecraft", method=list, register=commands)
  command_model(optional_alias='minecraft', alias='stop', descricao="Parar um servidor de minecraft \n uso: minecraft stop <nome>", method=stop, register=commands)
  command_model(optional_alias='minecraft', alias='start',descricao="Iniciar um servidor de minecraft \n uso: minecraft start <nome>", method=start, register=commands)
  
  args_create = command_args_register()
  
  args_create.addArg(command_args(unique_id='nome', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))
  args_create.addArg(command_args(unique_id='porta', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))
  args_create.addArg(command_args(unique_id='versao', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))
  args_create.addArg(command_args(unique_id='versaoforge', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))

  command_model(optional_alias='minecraft', alias='create',descricao="Criar um servidor de minecraft \n uso: minecraft start <nome>", method=create, register=commands, command_args=args_create)

  
