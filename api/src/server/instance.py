from flask import Flask
from flask_restx import Api
from flask_cors import CORS
import redis
import os

class Server():
    def __init__(self, ):
        self.app = Flask(__name__)
        CORS(self.app)
        self.api = Api(self.app,
        version='1.0',
        title='ModPack manager API',
        doc='/docs',
        )
        
    def run(self, ):
        self.app.run(
            host='0.0.0.0',
            debug=True
        )
server = Server()
redis_cache = redis.Redis(host=os.getenv('BOBERTO_HOST'),password=os.getenv("REDIS_PASSWORD"), port=6379)
