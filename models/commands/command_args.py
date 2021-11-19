from models.commands.command_register import command_register


class command_args:

    def __init__(self, unique_id: str, name: str, type_var: str, optional_alias = False, required = False, help = False):
        self.unique_id = unique_id
        self.name = name
        self.type_var = self.getType(type_var)
        self.help = help
        self.required = required
        self.optional_alias = optional_alias

    def getType(self,type_var):
        return ({
            'str' : str,
            'int' : int
        }[type_var])
