from models.commands.command_handler import command_handler
from models.commands.command_register import command_register
from models.permissions.permission_handler import permission_handler
from models.permissions.permission_model import permission_model
import docker
from models.permissions.permission_register import permission_register
import jwt_handler
import os
#import redis
from dotenv import load_dotenv
load_dotenv()
filename = 'whitelist.txt'
#redis_cache = redis.Redis(host='localhost',password='SUASENHA', port=6379, db=0)
perm_register = permission_register()
perm_handler = permission_handler(perm_register)
jwt = jwt_handler.Gerador_JWT(os.getenv('JWT_SECRET'))
dockerClient = docker.from_env()
with open(filename) as file:
    for line in file:
        line_splited = line.rstrip().split(',')
        user = permission_model(line_splited[0], line_splited[1])
        perm_register.add_user_permission(user)
        
commands_register = command_register()
commands_handle = command_handler(commands_register)



    

    
    
