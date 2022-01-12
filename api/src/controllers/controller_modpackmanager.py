import shutil
import os
from flask import json, request
from flask.helpers import make_response
from flask_restx import abort
from src.server.instance import server
from src.utils.api_utils import *
from glob import glob

app, api = server.app, server.api

@app.route('/modpackcreator/modpacks/sync', methods = ['POST'])
def add_modpack():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return abort(401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      content = request.get_json()
      old_modpacks = glob(os.path.join("web","data","cliente","files","files","*"), recursive = True)
      modspacks_new = []
      for modpack in content:
            modpack_dir = os.path.join(os.path.join("web","data","cliente","files","files",modpack["directory"]))
            modspacks_new.append(modpack_dir)
      
      for item in old_modpacks:
         if item not in modspacks_new:
            shutil.rmtree(item)
      
      with open(modpacks, 'w', encoding='utf-8') as f:
         json.dump(content, f, ensure_ascii=False, indent=4)
      return make_response('',200)

@app.route('/modpackcreator/modpacks/append', methods = ['POST'])
def append_modpack():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return abort(401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      modpacks_json = json.load(open(modpacks))
      content = request.get_json()

      store_list = []
      for item in modpacks_json:
         store_list.append(item)

    
      for index, item in enumerate(store_list):
         if item['id'] == content['id']:
            store_list[index] = content
         elif item['id'] != content['id'] and checkExistId(store_list, content['id']) == False:
            store_list.append(content)

      if len(store_list) == 0:
         store_list.append(content)

      print('teste',store_list)
      
      with open(modpacks, 'w', encoding='utf-8') as f:
         json.dump(store_list, f, ensure_ascii=False, indent=4)
      return make_response('',200)