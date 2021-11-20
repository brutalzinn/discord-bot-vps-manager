import datetime
import jwt
class Gerador_JWT:
    def __init__(self, secret):
        self.secret = secret

    def gerar_jwt(self, payload):
        encoded_jwt = jwt.encode({"payload":payload,"exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=60), "algorithm":"HS256"}, self.secret)
        print(f'Chave:{self.secret}')
        return encoded_jwt

