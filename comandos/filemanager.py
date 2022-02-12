import jwt
from models.commands.command_model import command_model
from models.commands.command_register import command_register
import config
import message_handler
import os
import json
import string    
import random # define the random module   
async def edit(command : command_model, message, user, client):
    print('userid',command.author)
    if not message_handler.isPrivate(message, user):
      await message.channel.send('Esse comando só pode ser executado em mensagem privada.') 
    await message_handler.send_message_private(message, user, 'Esse link será expirado em 60 segundos.')
    with config.engine.connect() as conn:
      result = conn.execute(config.text(f"select * from usuario where discord_id='{command.author}'"))
      row = result.fetchone()
      if row is None:
        await message_handler.send_message_private(message, user, 'Você não foi encontrado no banco de dados.. :(')
        return
      ##
      random_session = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10)) 
      with config.engine.connect() as conn:
        conn.execute(config.text(f"UPDATE usuario SET sessao='{random_session}' WHERE discord_id='{command.author}'"))
      discord_id = row._mapping['discord_id']
      nivel = row._mapping['nivel']
      email = row._mapping['email']
      whitelist = row._mapping['whitelist']
   
      payload = {"discord_id": discord_id, "nivel":nivel,"whitelist":whitelist,"email":email, "session_id":random_session}
      #config.redis_cache.set(random_session, json.dumps(payload))
      resultado = f"http://{os.getenv('URL')}/index.php?p=&user={config.jwt.gerar_jwt(payload)}"
      await message_handler.send_message_private(message, user, resultado)

    
def register(commands : command_register):
  command_model('edit',method=edit, descricao="Abrir editor de arquivos", register=commands, private=True,nivel=3)
  
