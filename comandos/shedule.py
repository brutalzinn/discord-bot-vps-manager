
import message_handler
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from models.commands.command_args import command_args
from models.commands.command_args_register import command_args_register
import discord
import config
import json

class Dialogo:
    nome = 'NOME'
    desc = 'DESC'
    server = 'SERVER'
    expresion = 'EXPRESSION'
    command = 'COMMAND'
    enabled = 'ENABLED'

async def job(command : command_model, message, user, client):

    new_args = command.args[1:]
    passos = ['nome','desc','server','expresion','command','enabled']

    def private(m):
        if isinstance(m.channel, discord.channel.DMChannel) and message.author != user :
            return True

    msg_modo = await message_handler.send_ask_question(client, private, 30, message, user, 'digite criar/editar/listar ou deletar para gerenciamento de jobs')
    await message_handler.send_message_private(message, user,f'Criando job no modo: {msg_modo}')
    if msg_modo == 'criar':
        msg_name = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um nome para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Nome: {msg_name}')

        msg_desc = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite uma descrição para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Descrição: {msg_desc}')

        msg_server = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um container para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Container: {msg_server}')

        msg_expression = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite uma expressão cron para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Expressão cron: {msg_expression}')

        msg_command = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um comando o job ser criado.')
        await message_handler.send_message_private(message, user,f'Comando: {msg_command}')
        commands = msg_command.split(',')

        msg_enabled = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um enabled o job ser criado.')
        await message_handler.send_message_private(message, user,f'Status cron: {msg_enabled}')

        with config.engine.connect() as conn:
            conn.execute(config.text(f"""INSERT INTO jobs(
        "id", "name", "description", "server", "expression", "command", "enabled")
        VALUES (DEFAULT, '{msg_name}', '{msg_desc}', '{msg_server}', '{msg_expression}', '{json.dumps(commands)}', '{msg_enabled}');"""))

        await message_handler.send_message_private(message, user, f'Job {msg_name} criado..')
    elif msg_modo == 'listar':
        s = []
        with config.engine.connect() as conn:
            result = conn.execute(config.text(f"select id, name, description, server, expression, enabled from jobs"))
            rows = result.fetchall()
 
            for user in rows:
                s.append('   '.join([str(item).center(0, ' ') for item in user]))

            d = '```'+'\n'.join(s) + '```'
            await message_handler.send_message_private(message, user, d)

    elif msg_modo == 'editar':
        s = []
        id = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite o id do job.')
        if id.isdigit() is False:
            await message_handler.send_message_private(message, user, 'É necessário que o id seja um número.')
            return
        await message_handler.send_message_private(message, user,f'Editando job com id: {id}')
        with config.engine.connect() as conn:
            result = conn.execute(config.text(f"select id, name, description, server, expression, enabled from jobs WHERE id='{id}'"))
            row = result.fetchone()
            if row is None:
                await message_handler.send_message_private(message, user, 'Não foi encontrado.. :(')
                return
            s.append('   '.join([str(item).center(0, ' ') for item in row]))
            d = '```'+'\n'.join(s) + '```'
            await message_handler.send_message_private(message, user, d)

            update = []

            msg_name = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um nome para o job ser criado.')
            await message_handler.send_message_private(message, user,f'Nome: {msg_name}')
            if not 'x' in  msg_name:
                update.append(f"name='{msg_name}'")

            msg_desc = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite uma descrição para o job ser criado.')
            await message_handler.send_message_private(message, user,f'Descrição: {msg_desc}')        
            if not 'x' in msg_desc:
                update.append(f"description='{msg_desc}'")
                
           
            msg_server = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um container para o job ser criado.')
            await message_handler.send_message_private(message, user,f'Container: {msg_server}')
            if not 'x' in msg_server:
                update.append(f"server='{msg_server}'")

            msg_expression = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite uma expressão cron para o job ser criado.')
            await message_handler.send_message_private(message, user,f'Expressão cron: {msg_expression}')
            if not 'x' in msg_expression:
                update.append(f"expression='{msg_expression}'")

            msg_command = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um comando o job ser criado.')
            await message_handler.send_message_private(message, user,f'Comando: {msg_command}')
            if not 'x' in msg_command:
                update.append(f"command='{msg_command}'")
            commands = msg_command.split(',')

            msg_enabled = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um enabled o job ser criado.')
            await message_handler.send_message_private(message, user,f'Status cron: {msg_enabled}')       
            if not 'x' in msg_enabled:
                update.append(f"enabled='{msg_enabled}'")
            
            update_string = ",".join(update)
            with config.engine.connect() as conn:
                    conn.execute(config.text(f"UPDATE jobs SET {update_string} WHERE id='{id}'"))
            
            await message_handler.send_message_private(message, user,f'Job editado com sucesso.')       



def register(commands : command_register):
    args_register = command_args_register()
    command_model('job', method=job, descricao="criar/editar/listar/deletar jobr", register=commands)
  