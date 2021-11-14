from models.permissions.permission_model import permission_model
from models.permissions.permission_register import permission_register
class permission_handler:
    def __init__(self, perm_register : permission_register):
        self.GetUsers = perm_register.get_user_permissions()
    def check_permission(self, author, nivel = 0):
        exists = False
        for obj in self.GetUsers:
            print(f'{obj.discord_id}-{author}')
            if str(author) == obj.discord_id and nivel <= obj.nivel:
                exists = True
                break
            else:
                exists = False
        return exists