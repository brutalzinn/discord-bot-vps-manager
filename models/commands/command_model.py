
from models.commands.command_register import command_register
import config
class command_model:
    def __init__(self ,alias :str, min_arg :int = 0, max_arg:int  = 2, method = False, optional_alias: str = False, 
                 register: command_register = False, nivel = 0):
        self.alias = alias
        self.method = method
        self.nivel = nivel
        self.max_arg = max_arg
        self.optional_alias = optional_alias
        self.min_arg = min_arg
        register.addCommand(self)
    def execute(self, command, author):
        if self.method is not False:
            if not config.perm_handler.check_permission(author,self.nivel): return "Você não tem permissão para executar esse comando"
            if len(command) >= self.min_arg and len(command) <= self.max_arg:
                return self.method(command)
        else:
            return False