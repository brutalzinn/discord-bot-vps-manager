from models.commands.command_register import command_register

class command_handler:
    def __init__(self,command_reg : command_register):
        self.commands = command_reg.getCommands()

    def checkCommand(self, args, author):
        for obj in self.commands:
          try:
            if not obj.optional_alias:  
                if obj.alias == args[0].strip():
                    obj.author = author
                    obj.args = args
                    return obj
            else:
                if len(self.commands) >= 1 and obj.optional_alias == args[0].strip() and obj.alias == args[1].strip():
                    obj.author = author
                    obj.args = args
                    return obj
          except:
              return "Comando não reconhecido."