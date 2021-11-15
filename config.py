from models.commands.command_handler import command_handler
from models.commands.command_register import command_register
from models.permissions.permission_handler import permission_handler
from models.permissions.permission_model import permission_model
from models.permissions.permission_register import permission_register
filename = 'whitelist.txt'
perm_register = permission_register()
perm_handler = permission_handler(perm_register)

with open(filename) as file:
    for line in file:
        line_splited = line.rstrip().split(',')
        user = permission_model(line_splited[0], line_splited[1])
        perm_register.add_user_permission(user)
        
commands_register = command_register()
commands_handle = command_handler(commands_register)


    

    
    
