import datetime
import jwt
import os
class Gerador_JWT:
    def __init__(self):
        self.secret = os.getenv('JWT_SECRET')

    def gerar_jwt(self, payload):
        encoded_jwt = jwt.encode({"payload":payload,"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=60)}, self.secret)
        print(f'Chave:{self.secret}')
        return encoded_jwt


