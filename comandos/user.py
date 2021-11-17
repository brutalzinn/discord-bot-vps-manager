import jwt
from models.commands.command_model import command_model
from models.commands.command_register import command_register
import config

async def edit(command : command_model, message):
    await message.channel.send('Testando mensagem') 
    payload = {"discord_id": command.author}
    resultado = f"http://127.0.0.1:3060/index.php?p=&user={config.jwt.gerar_jwt(payload)}"
    return resultado
    
def register(commands : command_register):
  command_model('edit',method=edit, register=commands, private=True)
  
