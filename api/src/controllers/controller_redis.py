

from src.server.instance import server, redis_cache
import os
from flask import  json, request
from flask_restx import abort
from src.utils.api_utils import *
from flask.helpers import make_response

app, api = server.app, server.api


@app.route('/redis/del', methods = ['POST'])
def del_redis():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return abort(401)
      content = request.get_json()
      if redis_cache.delete(content['id']):
        return make_response('',200)
      else:
        return make_response('modpack not found',400)


@app.route('/redis/clear', methods = ['POST'])
def clear_redis():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return abort(401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      obj = open(modpacks)
      data = json.load(obj)
      if len(data) == 0:
         return make_response('none modpacks are found.',400)
      for content in data:
         redis_cache.delete(content['id'])
      return make_response('',200)