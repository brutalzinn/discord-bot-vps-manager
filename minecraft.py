from mcstatus import MinecraftServer
from container_manager import list_container, start_container, stop_container
def MinecraftHandleCommand(message):
    command = message[1]
    
    if 'status' in command:
        try:
            server = MinecraftServer.lookup("127.0.0.1:25565")
            status = server.status()
            return "O servidor tem {0} jogadores jogando com {1} ms".format(status.players.online, status.latency)
        except(ConnectionRefusedError):
            return "O servidor está offline ou não responde."
                
    if 'ip' in command:
        return "jogar.robertocpaes.dev"
        
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
