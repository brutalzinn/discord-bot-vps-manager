from models.commands.command_register import command_register

class command_handler:
    def __init__(self,command_reg : command_register):
        self.commands = command_reg.getCommands()

    def checkCommand(self, args, author):
        for obj in self.commands:
          try:
            if not obj.obrigatory_alias:
                for v in obj.alias:
                    if v in args:
                        obj.author = author
                        obj.args = args
                        return obj
            else:
                for v in obj.alias:
                    if len(self.commands) >= 1 and obj.obrigatory_alias == args[0].strip() and v == args[1].strip():
                        obj.author = author
                        obj.args = args
                        return obj
          except:
              return "Comando não reconhecido."