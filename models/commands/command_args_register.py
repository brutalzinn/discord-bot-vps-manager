class command_args_register:
    def __init__(self):
        self.allArgs = []

    def addArg(self, command_args):
        self.allArgs.append(command_args)

    def getArgsCount(self):
        return len(self.allArgs)

    def getArgs(self):
        return self.allArgs

    def get_arg_unique(self, unique_id):
        for idx, arg in enumerate(self.allArgs):
            if arg.unique_id == unique_id:
                arg.index = idx
                return arg

     