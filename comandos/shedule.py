from inspect import ArgSpec
import message_handler
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from models.commands.command_args import command_args
from models.commands.command_args_register import command_args_register
import discord

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
    def modo(m):
        return isinstance(m.channel, discord.channel.DMChannel) and message.author != user and m.content == 'criar'
    def private(m):
        if isinstance(m.channel, discord.channel.DMChannel) and message.author != user:
            return True

    await message_handler.send_message_private(message, user, 'digite criar/editar ou deletar para gerenciamento de jobs')
    msg_modo = await client.wait_for('message', check=modo)
    await message_handler.send_message_private(message, user,'Criando job no modo: {.content}'.format(msg_modo))

    #get name of job

    await message_handler.send_message_private(message, user,'Digite um nome para o job ser criado.')
    msg_nome = await client.wait_for('message', check=private)
    await message_handler.send_message_private(message, user,'Job: {.content}'.format(msg_nome))

    #get  desc
    await message_handler.send_message_private(message, user,'Digite uma descrição para o job ser criado.')
    msg_desc = await client.wait_for('message', check=private)
    await message_handler.send_message_private(message, user,'Descrição: {.content}'.format(msg_desc))

    #get  server

    await message_handler.send_message_private(message, user,'Digite um container para o job ser criado.')
    msg_server = await client.wait_for('message', check=private)
    await message_handler.send_message_private(message, user,'Container: {.content}'.format(msg_server))

    #get  expression
    await message_handler.send_message_private(message, user,'Digite um expresion para o job ser criado.')
    msg_expression = await client.wait_for('message', check=private)
    await message_handler.send_message_private(message, user,'Expressão cron: {.content}'.format(msg_expression))
    
    #get command

    await message_handler.send_message_private(message, user,'Digite um command para o job ser criado.')
    msg_command = await client.wait_for('message', check=private)
    await message_handler.send_message_private(message, user,'Comando: {.content}'.format(msg_command))

    #get enabled

    await message_handler.send_message_private(message, user,'Digite um enabled para o job ser criado.')
    msg_enabled = await client.wait_for('message', check=private)
    await message_handler.send_message_private(message, user,'enabled: {.content}'.format(msg_enabled))


def register(commands : command_register):
    args_register = command_args_register()
    command_model('job', method=job, descricao="criar/editar/deletar jobr", register=commands)
  