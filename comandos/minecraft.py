from models.commands.command_model import command_model
from models.commands.command_register import command_register
from container_manager import list_container, start_container, stop_container
from mcstatus import MinecraftServer

def status(args):
    try:
        server = MinecraftServer.lookup("127.0.0.1:25565")
        status = server.status()
        return "O servidor tem {0} jogadores jogando com {1} ms".format(status.players.online, status.latency)
    except(ConnectionRefusedError):
        return "O servidor está offline ou não responde."
    
def list(args):
    return list_container()

def stop(args):          
    if stop_container(args[2]):
        return f"Parando servidor.. {args[2]}"
    else:
        return f"Ocorreu um erro ao parar servidor {args[2]} .."
  
def start(args):
    if start_container(args[2]):
        return f"Iniciando servidor.. {args[2]}"
    else:
        return f"Ocorreu um erro ao iniciar servidor {args[2]} .."

def register(commands : command_register):
  command_model(optional_alias='minecraft', alias='status',method=status, register=commands)
  command_model(optional_alias='minecraft', alias='list', method=list, register=commands)
  command_model(optional_alias='minecraft', alias='stop', max_arg=2, method=stop, register=commands)
  command_model(optional_alias='minecraft', alias='start', max_arg=2, method=start, register=commands)

  
