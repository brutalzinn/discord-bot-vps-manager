
from models.commands.command_register import command_register
from models.commands.command_args_register import command_args_register
import config
class command_model:
    def __init__(self, 
                alias,
                 min_arg :int = 0, 
                 method = False,
                 obrigatory_alias: str = False,
                 register: command_register = False,
                 command_args: command_args_register = False,
                 nivel = 0,
                 private = False, descricao = ''):

        self.max_arg = command_args.getArgsCount() if command_args != False else 0
        self.min_arg = min_arg
        self.alias = alias
        self.method = method
        self.nivel = nivel
        self.descricao = descricao + '\n'
        self.author = None
        self.private = private
        self.obrigatory_alias = obrigatory_alias
       #len(args.getArgs())
        self.command_args = command_args
        register.addCommand(self)
        self.register = register

    async def execute(self, message, user, cliente):
        if self.method is not False:
            if not config.perm_handler.check_permission(self.author, self.nivel):
                 await message.channel.send("Você não tem permissão para executar esse comando") 
                 return
            # if self.command_args is not False and len(self.command_args.getArgs()) >= self.min_arg and len(self.command_args.getArgs()) <= self.max_arg:
            #     return await self.method(self, message, user)
            # else:
            #     return await self.method(self, message, user)
            return await self.method(self, message, user, cliente)
        else:
            return False