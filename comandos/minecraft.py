from models.commands.command_args import command_args
from models.commands.command_args_register import command_args_register
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from container_manager import list_container, start_container, stop_container, create_container,remove_container, get_container
from mcstatus import MinecraftServer
import message_handler
import os
from pathlib import Path


async def status(command : command_model, message, user, client):
    resultado = ''
    try:
        new_args = command.args[2:]
        nome = new_args[command.command_args.get_arg_unique('nome').index]   
        serverport = get_container(nome)
        if serverport is None:
            await message_handler.send_message_normal(message,  user, 'Esse servidor não existe.')
            return
        server = MinecraftServer.lookup(f"{os.getenv('BOBERTO_HOST')}:{serverport['port']}")
        status = server.status()
        resultado = "O servidor tem {0} jogadores jogando com {1} ms".format(status.players.online, status.latency)
    except(ConnectionRefusedError):
        resultado = "O servidor está offline ou não responde."
    
    await message_handler.send_message_normal(message,  user, resultado)

    
async def list(command : command_model, message, user, client):
    await message_handler.send_message_normal(message,  user, list_container())

async def stop(command : command_model, message, user, client):  
    new_args = command.args[2:]
    nome = new_args[command.command_args.get_arg_unique('nome').index]     
    resultado = ''
    if stop_container(nome):
        resultado = f"Parando servidor.. {nome}"
    else:
        resultado = f"Ocorreu um erro ao parar servidor {nome} .."
    await message_handler.send_message_normal(message,  user, resultado)

async def remove(command : command_model, message, user, client):  
    new_args = command.args[2:]
    nome = new_args[command.command_args.get_arg_unique('nome').index]     
    resultado = ''
    docker_connection = remove_container(nome)
    if docker_connection:
        resultado = f"servidor.. {nome} removido"
    else:
        resultado = f"Ocorreu um erro ao remover servidor {nome} ---  {docker_connection}"
    await message_handler.send_message_normal(message,  user, resultado)
  
async def start(command : command_model, message, user, client):
    new_args = command.args[2:]
    nome = new_args[command.command_args.get_arg_unique('nome').index]    
    docker_connection = start_container(nome)
    if docker_connection:
        await message_handler.send_message_normal(message,  user, f"Iniciando servidor.. {nome}")
    else:
        await message_handler.send_message_normal(message,  user,  f"Ocorreu um erro ao iniciar servidor {nome} ---  {docker_connection}")


async def create(command : command_model, message, user, client):
    environment = {"EULA": "TRUE", "ONLINE_MODE": "FALSE", "USE_AIKAR_FLAGS":"TRUE", "EXEC_DIRECTLY":"TRUE"}
    new_args = command.args[2:]
    versaojava = "latest"
    print(new_args)
    nome = new_args[command.command_args.get_arg_unique('nome').index]     
    porta = new_args[command.command_args.get_arg_unique('porta').index]     
    versao = new_args[command.command_args.get_arg_unique('versao').index]     
    memoria = new_args[command.command_args.get_arg_unique('memoria').index]
    tipo = new_args[command.command_args.get_arg_unique('tipo').index]

    if tipo == "forge":
        versaoforge = new_args[command.command_args.get_arg_unique('versaojavaouforge').index]
        environment['FORGEVERSION'] = versaoforge
        environment['TYPE'] = "FORGE"
        versaojava = "java8"
    else:
        versaojava = new_args[command.command_args.get_arg_unique('versaojavaouforge').index]

        

    if int(memoria) > 7:
        await message_handler.send_message_normal(message,  user, f'Memória limite atingida. Use menos de 6G')
        return
    await message_handler.send_message_normal(message,  user, f'Criando servidor {nome} ..')


    root_directory = Path(__file__).parent.parent
    arquivos = os.path.join(root_directory,'web','data','servidores')
    if not os.path.isdir(arquivos):
        os.mkdir(arquivos)
    server_path = os.path.join(arquivos, nome)
    if not os.path.isdir(server_path):
        os.mkdir(server_path)
        await message_handler.send_message_normal(message,  user, f'Preparando servidor {nome}')

    docker_volume =  os.path.abspath(os.path.join(os.getenv('PROJECT_ROOT'), 'web','data','servidores', nome))
    environment['VERSION'] = versao
    environment['INIT_MEMORY'] = f'4G'
    environment['MAX_MEMORY'] = f'{memoria}G'
    resultado = create_container(docker_volume, versaojava, nome,porta,environment)
    print('chamando docker create..')
    if resultado['status']:
        await message_handler.send_message_normal(message,  user, f'Servidor criado.. {nome}')
    else:
        await message_handler.send_message_normal(message,  user, resultado['mensagem'])

async def console(command : command_model, message, user, client):
    new_args = command.args[2:]
    nome = new_args[command.command_args.get_arg_unique('nome').index]    
    await message_handler.send_message_normal(message,  user, f"Acesse o terminal em \n http://boberto.net/data/console?servidor={nome}")
    

def register(commands : command_register):
    
  args_default = command_args_register()  
  args_default.addArg(command_args(unique_id='nome', name='nome do servidor',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))
  
  command_model(alias=['minecraft', 'status'],descricao="Exibir status do servidor de minecraft \n uso: minecraft status <nome>", method=status, register=commands, command_args=args_default)
  command_model(alias=['minecraft', 'stop'], descricao="Parar um servidor de minecraft \n uso: minecraft stop <nome>", method=stop, register=commands, command_args=args_default) 
  command_model(alias=['minecraft', 'start'],descricao="Iniciar um servidor de minecraft \n uso: minecraft start <nome>", method=start, register=commands, command_args=args_default)
  command_model(alias=['minecraft', 'remove'],descricao="Iniciar um servidor de minecraft \n uso: minecraft start <nome>", method=remove, register=commands, command_args=args_default)
  command_model(alias=['minecraft', 'console'],descricao="abrir um console \n uso: minecraft console <nome>", method=console, register=commands, command_args=args_default)
  command_model(alias=['minecraft', 'list'], descricao="Exibir uma lista de servidores de minecraft", method=list, register=commands)

  
  args_create = command_args_register()
  args_create.addArg(command_args(unique_id='nome', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))
  args_create.addArg(command_args(unique_id='porta', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))
  args_create.addArg(command_args(unique_id='versao', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))
  args_create.addArg(command_args(unique_id='memoria', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.',required=True))
  args_create.addArg(command_args(unique_id='tipo', name='nome do comando',type_var='str',help='Configura o tipo do servidor.', required=True))
  args_create.addArg(command_args(unique_id='versaojavaouforge', name='nome do comando',type_var='str',help='Versão do forge',required=False))

  command_model(alias=['minecraft', 'create'],descricao="Criar um servidor de minecraft \n uso: minecraft start <nome>", method=create, register=commands, command_args=args_create)

  
