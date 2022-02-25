from models.commands.command_model import command_model
from models.commands.command_register import command_register

class command_handler:
    def __init__(self,command_reg : command_register):
        self.commands = command_reg.getCommands()

    def solve(self, command: command_model, args):
        s1=''
        s2=''
        all_args = []
        if command.command_args != False:
            args_optional = command.command_args.getOptionalArgsLen()
            if args_optional > 0:
            print(args_optional)

            all_args = args[:-command.max_arg]
        else:
            all_args = args

    
        for i in command.alias:
            s1+=i
        for i in all_args:
            s2+=i
        return s2 in s1

    def checkCommand(self, args, author):
        try:
            for obj in self.commands:
            
                if self.solve(obj, args):
                    obj.author = author
                    obj.args = args
                    return obj
                # else:
                #     for v in obj.alias:
                #         if len(self.commands) >= 1 and obj.obrigatory_alias == args[0].strip() and v == args[1].strip():
                #             obj.author = author
                #             obj.args = args
                #             return obj
        except:
            return None