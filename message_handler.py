from models.commands.command_model import command_model
import discord

async def send_message_private(message, user, resposta = ''):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != user:
        await message.channel.send(resposta)
async def send_message_normal(message, user, resposta = ''):
        await message.channel.send(resposta)
          
