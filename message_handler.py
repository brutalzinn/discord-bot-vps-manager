from models.commands.command_model import command_model
import discord

async def send_message_private(message_channel, user, message = ''):

    if isinstance(message_channel.channel, discord.channel.DMChannel) and message_channel.author != user:
        await message_channel.channel.send(message)

async def send_message_normal(message_channel, user, message = ''):
        await message_channel.channel.send(message)


async def send_ask_question(client, timeout, message_channel, user, ask):
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
    wait_reply = await client.wait_for('message', check=lambda message: message.author != user)
    return wait_reply.content

def isPrivate(message, user):
    return isinstance(message.channel, discord.channel.DMChannel) and message.author != user
