import jwt
from models.commands.command_model import command_model
from models.commands.command_register import command_register
import config
from sqlalchemy import event, text
from sqlalchemy import create_engine
import message_handler

async def edit(command : command_model, message, user):
    await message.channel.send('Testando mensagem') 
    await message_handler.send_message_private(message, user, 'Esse link será expirado em 60 segundos.')
    engine = create_engine("postgresql://root:root@localhost/boberto")
    with engine.connect() as conn:
      result = conn.execute(text(f"select * from usuario where discord_id='{command.author}'"))
      row = result.fetchone()
      if row is None:
        await message_handler.send_message_private(message, user, 'Você não foi encontrado no banco de dados.. :(')
        return
      discord_id = row._mapping['discord_id']
      nivel = row._mapping['nivel']
      email = row._mapping['email']
      whitelist = row._mapping['whitelist']
      payload = {"discord_id": discord_id, "nivel":nivel,"whitelist":whitelist,"email":email}
      resultado = f"http://127.0.0.1:3060/index.php?p=&user={config.jwt.gerar_jwt(payload)}"
      await message_handler.send_message_private(message, user, resultado)

    
def register(commands : command_register):
  command_model('edit',method=edit, descricao="Abrir editor de arquivos", register=commands, private=True)
  
