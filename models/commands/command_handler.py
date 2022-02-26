from models.commands.command_model import command_model
from models.commands.command_register import command_register

class command_handler:
    def __init__(self,command_reg : command_register):
        self.commands = command_reg.getCommands()

    def solve(self, command: command_model, args):
        encontrado = False
        for idx, arg in enumerate(command.alias):
            if len(args) >= len(command.alias) and command.alias[idx] == args[idx]:
                encontrado = True
        return encontrado

    def checkCommand(self, args, author):
 
        for obj in self.commands:
        
            if self.solve(obj, args):
                obj.author = author
                obj.args = args
                return obj
        return None