#refatorar nome para user_model
class permission_model:
    def __init__(self, discord_id, nivel = 0):
        self.discord_id = discord_id
        self.nivel = int(nivel)