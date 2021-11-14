from models.commands.command_register import command_register

class command_handler:
    def __init__(self,command_reg : command_register):
        self.commands = command_reg.getCommands()

    def checkCommand(self, command):
        print(f'comandos:{len(self.commands)}')
        for obj in self.commands:
          if obj.alias == command[0].strip():
                return obj.execute(command)