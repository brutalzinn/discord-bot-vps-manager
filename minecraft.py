from mcstatus import MinecraftServer
from container_manager import list_container, start_container, stop_container
from models.permissions.permission_handler import permission_handler
def MinecraftHandleCommand(message, perm_handler: permission_handler):
    command = message.content.split()[1]
    author = message.author
    if 'status' in command:
        
        try:
            server = MinecraftServer.lookup("127.0.0.1:25565")
            status = server.status()
            return "O servidor tem {0} jogadores jogando com {1} ms".format(status.players.online, status.latency)
        except(ConnectionRefusedError):
            return "O servidor está offline ou não responde."
                
    if 'ip' in command:
        return "jogar.robertocpaes.dev"
    
    if perm_handler.check_permission(author,1):
        if 'teste1' in command:
            return "Testandooo permissão 1"
    else:
        return "Você não permissão pra isso."
    
    if perm_handler.check_permission(author,2):
        if 'teste2' in command:
            return "Testandooo permissão 2"
    else:
        return "Você não permissão pra isso."
            
        
    if 'list' in command:
        return list_container()
    
    if len(message) > 2:
        if 'stop' in command:
                
            if stop_container(message[2]):
                return f"Parando servidor.. {message[2]}"
            else:
                return f"Ocorreu um erro ao parar servidor {message[2]} .."

        if 'start' in command:
                    
            if start_container(message[2]):
                return f"Iniciando servidor.. {message[2]}"
            else:
                return f"Ocorreu um erro ao iniciar servidor {message[2]} .."
    else:
        return f"Informe o nome do servidor."
