from models.commands.command_handler import command_handler
from models.commands.command_register import command_register
from models.permissions.permission_handler import permission_handler
from models.permissions.permission_model import permission_model
import docker
from models.permissions.permission_register import permission_register
import jwt_handler
import os
import redis
import requests
from sqlalchemy import event, text,create_engine
from dotenv import load_dotenv
load_dotenv()
discordToken = os.getenv('DISCORD_TOKEN')
discordUrl = os.getenv('DISCORD_URL')

engine = create_engine(f"postgresql://{os.getenv('BOBERTO_USER')}:{os.getenv('BOBERTO_PASSWORD')}@{os.getenv('BOBERTO_HOST')}/{os.getenv('BOBERTO_DATABASE')}")

redis_cache = redis.Redis(host=os.getenv('BOBERTO_HOST'),password=os.getenv("REDIS_PASSWORD"), port=6379)

jwt = jwt_handler.Gerador_JWT(os.getenv('JWT_SECRET'))
dockerClient = docker.from_env()

perm_register = permission_register()
perm_handler = permission_handler(perm_register)
def loadPermissions():
    with engine.connect() as conn:
        result = conn.execute(text(f"select * from usuario"))
        rows = result.fetchall()
        for user in rows:
            discord_id = user._mapping['discord_id']
            nivel = user._mapping['nivel']
            user = permission_model(discord_id, nivel)
            perm_register.add_user_permission(user)



def discord_notification(message):   
    myobj = {'content': message}
    #requests.post(discordUrl, data = myobj)



commands_register = command_register()
commands_handle = command_handler(commands_register)



    

    
    
