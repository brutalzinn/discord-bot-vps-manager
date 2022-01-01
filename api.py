from discord.enums import ContentFilter
from flask import Flask, render_template, request, Response
import os
from pyunpack import Archive
import json
from flask import jsonify
import config
import shutil
from glob import glob
app = Flask(__name__)

#First boberto api try. This is pure gamb. Please, dont reply in any production server.
#This file contains method that doesnt secure to use in production early. 
#Boberto needs be happy with this api :) 
@app.route('/launcher/list/modpacks', methods = ['GET'])
def get_modpacks():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      f = open(modpacks)
      data = json.load(f)
      f.close()
      return jsonify(data)

#gamb to delete all modpacks that dont include in the new modpack update
#need refactor this some later
@app.route('/launcher/update/modpacks', methods = ['POST'])
def add_modpack():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      content = request.get_json()
      old_modpacks = glob(os.path.join("web","data","cliente","files","files","*"), recursive = True)
      for modpack in content:
            modpack_dir = os.path.join("web","data","cliente","files","files",modpack["directory"])
            modpacks_exists = []
            if modpack_dir in old_modpacks:
               modpacks_exists.append(modpack_dir)
      for old_folder in old_modpacks:
         if not old_folder in modpacks_exists:
            shutil.rmtree(old_folder)
      with open(modpacks, 'w', encoding='utf-8') as f:
         json.dump(content, f, ensure_ascii=False, indent=4)
      return Response(status=200)

@app.route('/launcher/config', methods = ['POST'])
def update_config():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      config_launcher = os.path.join("web","data","cliente","launcher","config-launcher","config.json")
      content = request.json
      with open(config_launcher, 'w', encoding='utf-8') as f:
         json.dump(content, f, ensure_ascii=False, indent=4)
      return Response(status=200)

#This route is called when a modpack is updated by modpack creator.
#We need clear redis cache before update the new modpack 
#and we need to put launcher in maintance mod too.
@app.route('/launcher/del/redis', methods = ['POST'])
def clear_redis():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      content = request.get_json()
      config.redis_cache.delete(content['id'])
      return Response(status=200)

@app.route('/launcher/upload/modpacks', methods = ['POST'])
def upload_file():
   if request.headers.get('api-key') != os.getenv('API_TOKEN'):
      return Response(status=401)
   if request.method == 'POST':
      f = request.files['file']
      directory = request.form.get('directory')
      if not os.path.exists(os.path.join("web","data","cliente","files","files",directory)):
         # os.mkdir(os.path.join("web","data","cliente","files","files",directory))
          os.umask(0)
          os.makedirs(os.path.join("web","data","cliente","files","files",directory), mode=0o777)
      if f.filename.split('.')[1]  != 'zip':
        return Response(status=401)
      file_zip = os.path.join("web","data","cliente","files","files", f.filename)
      file_zip_out = os.path.join("web","data","cliente","files","files",directory)
      try:
         f.save(file_zip)
         Archive(file_zip).extractall(file_zip_out)
         #os.unlink(file_zip)
      except:
         print("Deu erro.")
         return Response(status=401)
      return Response(status=200)
		
