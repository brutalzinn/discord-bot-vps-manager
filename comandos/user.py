import message_handler
from psutil._common import bytes2human
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from models.commands.command_args import command_args
from models.commands.command_args_register import command_args_register
import config

async def ajuda(command : command_model, message, user, client):
    resultado = ''
    is_show_command = False
    new_args = command.args[1:]
    is_show_command = len(new_args) > 0
    print(new_args)
    if is_show_command is False:
        for comando in command.register.allCommands:
            if not comando.optional_alias: 
                resultado += f'{comando.alias} - {comando.descricao} \n'
            else:
                resultado += f'{comando.optional_alias} {comando.alias} - {comando.descricao} \n'
    else:
        comando_args = command.command_args.get_arg_unique('nome_comando')      
        command_name = new_args[comando_args.index]

        print(f'testando.. {command_name}')
        for comando in command.register.allCommands:
            resultado = ''
            if not comando.optional_alias and comando.alias == command_name:
                resultado += f'{comando.alias} - {comando.descricao} \n'
                break
            elif len(new_args) > 1 and comando.optional_alias == command_name and comando.alias == new_args[1]:
                resultado += f'{comando.optional_alias} {comando.alias} - {comando.descricao} \n'
                break
    await message_handler.send_message_normal(message,  user,   resultado)
    
async def key_gen(command : command_model, message, user, client):
    with config.engine.connect() as conn:
      result = conn.execute(config.text(f"select * from usuario where discord_id='{command.author}'"))
      row = result.fetchone()
      if row is None:
        await message_handler.send_message_private(message, user, 'Você não foi encontrado no banco de dados.. :(')
        return
    discord_id = row._mapping['discord_id']
    nivel = row._mapping['nivel']
    email = row._mapping['email']
    whitelist = row._mapping['whitelist']
    payload = {"discord_id": discord_id, "nivel":nivel,"whitelist":whitelist,"email":email}
    await message_handler.send_message_normal(message,  user, config.jwt.gerar_jwt(payload, 1440))

def register(commands : command_register):
    args_register = command_args_register()
    args_register.addArg(command_args(unique_id='nome_comando', name='nome do comando',type_var='str',help='Exibe uma ajuda sobre um comando específico.'))
    command_model('ajuda', method=ajuda, descricao="Exibir todos os comandos e opções de ajuda", register=commands, command_args=args_register)
    command_model('login', method=key_gen, descricao="Exibir todos os comandos e opções de ajuda", register=commands, command_args=args_register, private=True)
