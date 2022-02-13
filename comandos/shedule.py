
import message_handler
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from models.commands.command_args import command_args
from models.commands.command_args_register import command_args_register
import discord
import config
import json
import cronjob
class Dialogo:
    nome = 'NOME'
    desc = 'DESC'
    server = 'SERVER'
    expresion = 'EXPRESSION'
    command = 'COMMAND'
    enabled = 'ENABLED'

async def job(command : command_model, message, user, client):

    def private(m):
        return message.author != user


    msg_modo = await message_handler.send_ask_question(client, private, 10, message, user, 'digite criar/editar/listar ou deletar para gerenciamento de jobs')
    await message_handler.send_message_private(message, user,f'Criando job no modo: {msg_modo}')
    if msg_modo == 'criar':

        msg_name = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite um nome para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Nome: {msg_name}')

        msg_desc = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite uma descrição para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Descrição: {msg_desc}')

        msg_server = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite um container para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Container: {msg_server}')

        msg_expression = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite uma expressão cron para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Expressão cron: {msg_expression}')

        msg_command = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite um comando o job ser criado.')
        await message_handler.send_message_private(message, user,f'Comando: {msg_command}')
        commands = msg_command.split(',')

        msg_enabled = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite um enabled o job ser criado.')
        await message_handler.send_message_private(message, user,f'Status cron: {msg_enabled}')

        with config.engine.connect() as conn:
            conn.execute(config.text(f"""INSERT INTO jobs(
        "id", "name", "description", "server", "expression", "command", "enabled")
        VALUES (DEFAULT, '{msg_name}', '{msg_desc}', '{msg_server}', '{msg_expression}', '{json.dumps(commands)}', '{msg_enabled}');"""))

        await message_handler.send_message_private(message, user, f'Job {msg_name} criado..')

        cronjob.UpdateJobs()

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

        id = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite o id do job.')
        if id.isdigit() is False:
            await message_handler.send_message_private(message, user, 'É necessário que o id seja um número.')
            return
        await message_handler.send_message_private(message, user,f'Editando job com id: {id}')
        with config.engine.connect() as conn:
            result = conn.execute(config.text(f"select id from jobs WHERE id='{id}'"))
            row = result.fetchone()
            if row is None:
                await message_handler.send_message_private(message, user, 'Não foi encontrado.. :(')
                return

        update = []

        msg_name = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite um nome para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Nome: {msg_name}')
        if not msg_name.startswith('x'):
            update.append(f"name='{msg_name}'")

        msg_desc = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite uma descrição para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Descrição: {msg_desc}')        
        if not msg_desc.startswith('x'):
            update.append(f"description='{msg_desc}'")
            
        msg_server = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite um container para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Container: {msg_server}')
        if not msg_server.startswith('x'):
            update.append(f"server='{msg_server}'")

        msg_expression = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite uma expressão cron para o job ser criado.')
        await message_handler.send_message_private(message, user,f'Expressão cron: {msg_expression}')
        if not msg_expression.startswith('x'):
            update.append(f"expression='{msg_expression}'")

        msg_command = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite um comando o job ser criado.')
        await message_handler.send_message_private(message, user,f'Comando: {msg_command}')
        if not msg_command.startswith('x'):
            commands = msg_command.split(',')
            update.append(f"command='{json.dumps(commands)}'")
        

        msg_enabled = await message_handler.send_ask_question(client, private, 30, message, user, 'Digite 1 ou 0 para ativar/desativar o job')
        await message_handler.send_message_private(message, user,f'Você escolheu: {msg_enabled}')       
        if not msg_enabled.startswith('x'):
            update.append(f"enabled='{msg_enabled}'")

        if len(update) == 0:
            await message_handler.send_message_private(message, user,f'Edit do job cancelado.')
            return

        update_string = ",".join(update)

        with config.engine.connect() as conn:
                conn.execute(config.text(f"UPDATE jobs SET {update_string} WHERE id='{id}'"))
        
        await message_handler.send_message_private(message, user,f'Job editado com sucesso.')

        cronjob.UpdateJobs()

    elif msg_modo == 'deletar':
        s = []
        id = await message_handler.send_ask_question(client, private, 10, message, user, 'Digite o id do job.')
        if id.isdigit() is False:
            await message_handler.send_message_private(message, user, 'É necessário que o id seja um número.')
            return
        await message_handler.send_message_private(message, user,f'Deletando job com id: {id}')
        with config.engine.connect() as conn:
            conn.execute(config.text(f"DELETE from jobs WHERE id='{id}'"))
            await message_handler.send_message_private(message, user, 'Deletado com sucesso :(')

            cronjob.UpdateJobs()

def register(commands : command_register):
    command_model('job', method=job, descricao="criar/editar/listar/deletar jobr", register=commands)
  