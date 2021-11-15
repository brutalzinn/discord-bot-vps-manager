from models.commands.command_register import command_register

class command_handler:
    def __init__(self,command_reg : command_register):
        self.commands = command_reg.getCommands()

    def checkCommand(self, command,author):
        for obj in self.commands:
          try:
            if not obj.optional_alias:  
                if obj.alias == command[0].strip():
                    return obj.execute(command, author)
            else:
                if len(self.commands) >= 1 and obj.optional_alias == command[0].strip() and obj.alias == command[1].strip():
                    return obj.execute(command, author)
          except:
              return "Comando não reconhecido."