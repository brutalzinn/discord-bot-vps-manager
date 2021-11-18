import jwt
from models.commands.command_model import command_model
from models.commands.command_register import command_register
import config
from sqlalchemy import event, text
from sqlalchemy import create_engine

async def edit(command : command_model, message):
    await message.channel.send('Testando mensagem') 


    engine = create_engine("postgresql://root:root@localhost/boberto")
    with engine.connect() as conn:
      result = conn.execute(text("select * from usuario where id=1"))
      payload = {"discord_id": command.author}
      await message.channel.send(result) 

    
    resultado = f"http://127.0.0.1:3060/index.php?p=&user={config.jwt.gerar_jwt(payload)}"
    return resultado
    
def register(commands : command_register):
  command_model('edit',method=edit, register=commands, private=True)
  
