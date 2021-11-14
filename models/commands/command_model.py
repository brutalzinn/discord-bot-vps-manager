
from models.commands.command_register import command_register
class command_model:
    def __init__(self ,alias, min_arg=0, max_arg = 2, method = False, register: command_register = False):
        self.alias = alias
        self.method = method
        self.max_arg = max_arg
        self.min_arg = min_arg
        register.addCommand(self)
    def execute(self, command):
        if self.method is not False:
            if len(command) >= self.min_arg and len(command) <= self.max_arg:
                return self.method(command)
        else:
            return False