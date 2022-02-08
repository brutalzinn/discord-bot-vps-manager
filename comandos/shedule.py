from inspect import ArgSpec
import message_handler
from models.commands.command_model import command_model
from models.commands.command_register import command_register
from models.commands.command_args import command_args
from models.commands.command_args_register import command_args_register

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
    await message_handler.send_message_normal('say hello')
    def check(m):
        return m.content == 'hello'
    msg = await client.wait_for('message', check=check)
    await message_handler.send_message_normal('Hello {.author}!'.format(msg))

  
def register(commands : command_register):
    args_register = command_args_register()
    command_model('job', method=job, descricao="criar/editar/deletar jobr", register=commands)
  