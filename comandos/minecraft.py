from models.commands.command_model import command_model
from models.commands.command_register import command_register
from container_manager import list_container, start_container, stop_container
from mcstatus import MinecraftServer

async def status(command : command_model, message):
    try:
        server = MinecraftServer.lookup("127.0.0.1:25565")
        status = server.status()
        return "O servidor tem {0} jogadores jogando com {1} ms".format(status.players.online, status.latency)
    except(ConnectionRefusedError):
        return "O servidor está offline ou não responde."
    
async def list(command : command_model, message):
    return list_container()

async def stop(command : command_model, message):          
    if stop_container(command.args[2]):
        return f"Parando servidor.. {command.args[2]}"
    else:
        return f"Ocorreu um erro ao parar servidor {command.args[2]} .."
  
async def start(command : command_model, message):
    if start_container(command.args[2]):
        return f"Iniciando servidor.. {command.args[2]}"
    else:
        return f"Ocorreu um erro ao iniciar servidor {command.args[2]} .."

def register(commands : command_register):
  command_model(optional_alias='minecraft', alias='status',descricao="Exibir status do servidor de minecraft \n uso: minecraft status <nome>", method=status, register=commands)
  command_model(optional_alias='minecraft', alias='list', descricao="Exibir uma lista de servidores de minecraft", method=list, register=commands)
  command_model(optional_alias='minecraft', alias='stop', descricao="Parar um servidor de minecraft \n uso: minecraft stop <nome>", max_arg=2, method=stop, register=commands)
  command_model(optional_alias='minecraft', alias='start',descricao="Iniciar um servidor de minecraft \n uso: minecraft start <nome>", max_arg=2, method=start, register=commands)

  
