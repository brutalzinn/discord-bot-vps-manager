
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
        await message_handler.send_message_private(message, user,f'Expressão cron: {msg_command}')
        commands = msg_command.split(',')

        msg_enabled = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite um enabled o job ser criado.')
        await message_handler.send_message_private(message, user,f'Expressão cron: {msg_enabled}')

        with config.engine.connect() as conn:
            conn.execute(config.text(f"""INSERT INTO jobs(
        "id", "name", "desc", "server", "expression", "command", "enabled")
        VALUES (DEFAULT, '{msg_name}', '{msg_desc}', '{msg_server}', '{msg_expression}', '{json.dumps(commands)}', '{msg_enabled}');"""))

        await message_handler.send_message_private(message, user, f'Job {msg_name} criado..')
    elif msg_modo == 'listar':
        s = ['ID      Nome      Descrição      Container      Cron      Comando      Enabled']

        with config.engine.connect() as conn:
            result = conn.execute(config.text(f"select *from jobs"))
            rows = result.fetchall()
 
            for user in rows:
                s.append('    '.join([str(item).center(0, ' ') for item in user]))

            d = '```'+'\n'.join(s) + '```'
            await message_handler.send_message_private(message, user, d)


def register(commands : command_register):
    args_register = command_args_register()
    command_model('job', method=job, descricao="criar/editar/listar/deletar jobr", register=commands)
  