
from models.commands.command_register import command_register
import config
class command_model:
    def __init__(self ,alias :str, min_arg :int = 0, max_arg:int  = 2, method = False, optional_alias: str = False, 
                 register: command_register = False, nivel = 0, private = False):
        self.alias = alias
        self.method = method
        self.nivel = nivel
        self.args = None
        self.author = None
        self.private = private
        self.max_arg = max_arg
        self.optional_alias = optional_alias
        self.min_arg = min_arg
        register.addCommand(self)
    async def execute(self, message, user):
        if self.method is not False:
            if not config.perm_handler.check_permission(self.author, self.nivel): return "Você não tem permissão para executar esse comando"
            if len(self.args) >= self.min_arg and len(self.args) <= self.max_arg:
                return await self.method(self, message, user)
        else:
            return False