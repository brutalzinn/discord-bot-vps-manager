from models.permissions.permission_model import permission_model
class permission_register:
    def __init__(self):
        self.allUsers = []

    def add_user_permission(self, user : permission_model):
        self.allUsers.append(user)

    def get_user_permissions(self):
        return self.allUsers