from models.commands.command_model import command_model
import discord

async def send_message_private(message, user, resposta = ''):

    if isinstance(message.channel, discord.channel.DMChannel) and message.author != user:
        await message.channel.send(resposta)

async def send_message_normal(message, user, resposta = ''):
        await message.channel.send(resposta)


async def send_ask_question(client, check, timeout, message_channel, user, ask):
    '''
    Send a ask question to discord bot. Originally created to be used with Boberto bot.
    @input:
        client = discord client param,
        check = bool to check when this ask will be checked,
        timeout = timeout to reply message,
        message_channel = a discord channel to be used,
        user = the discord user,
        ask = the question to user
    @output: user response
    '''
    await send_message_private(message_channel, user, ask)
    wait_reply = await client.wait_for('message', check=check,timeout=timeout)
    return wait_reply.content

def isPrivate(message, user):
    return isinstance(message.channel, discord.channel.DMChannel) and message.author != user
