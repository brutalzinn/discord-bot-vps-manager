from flask import Flask, render_template, request, Response
import os
from pyunpack import Archive
import json
from flask import jsonify
import redis
import shutil
from glob import glob
app = Flask(__name__)
redis_cache = redis.Redis(host=os.getenv('BOBERTO_HOST'),password=os.getenv("REDIS_PASSWORD"), port=6379)

# we need to convert this api to PHP
#First boberto api try. This is pure gamb. Please, dont reply in any production server.
#This file contains method that doesnt secure to use in production early. 
#Boberto needs be happy with this api :) 

ALLOWED_EXTENSIONS = set(['zip'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkExist(store_list, value):
   exist = False
   for item in store_list:
         if item['id'] == value:
            exist = True

   return exist

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

@app.route('/launcher/update/sync/modpacks', methods = ['POST'])
def add_modpack():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
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
      return Response(status=200)

@app.route('/launcher/update/append/modpacks', methods = ['POST'])
def append_modpack():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      modpacks_json = json.load(open(modpacks))
      content = request.get_json()

      store_list = []
      for item in modpacks_json:
         store_list.append(item)

    
      for index, item in enumerate(store_list):
         if item['id'] == content['id']:
            store_list[index] = content
         elif item['id'] != content['id'] and checkExist(store_list, content['id']) == False:
            store_list.append(content)

      
      with open(modpacks, 'w', encoding='utf-8') as f:
         json.dump(store_list, f, ensure_ascii=False, indent=4)
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
def del_redis():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      content = request.get_json()
      redis_cache.delete(content['id'])
      return Response(status=200)

@app.route('/launcher/clear/redis', methods = ['POST'])
def clear_redis():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      obj = open(modpacks)
      data = json.load(obj)
      for content in data:
         redis_cache.delete(content['id'])
      return Response(status=200)

@app.route('/launcher/upload/modpacks', methods = ['POST'])
def upload_file():
   if request.headers.get('api-key') != os.getenv('API_TOKEN'):
      return Response(status=401)
   if request.method == 'POST':
      f = request.files['file']
      directory = request.form.get('directory')
      os.umask(0)
      if not os.path.exists(os.path.join('web','data','cliente','files','files',directory)):
         # os.mkdir(os.path.join('web','data','cliente','files','files',directory))
          os.umask(0)
          os.makedirs(os.path.join('web','data','cliente','files','files',directory), mode=0o777)
      if f.filename.split('.')[1]  != 'zip':
        return Response(status=401)
      file_zip = os.path.join('web','data','cliente','files','files', f.filename)
      file_zip_out = os.path.join('web','data','cliente','files','files',directory)
      try:
         f.save(file_zip)
         Archive(file_zip).extractall(file_zip_out)
         os.unlink(file_zip)
      except:
         print('Deu erro.')
         return Response(status=401)
      return Response(status=200)

@app.route('/launcher/upload/update', methods = ['POST'])
def update_launcher_zips():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      if request.method == 'POST':
         files = request.files.getlist('file')
         for file in files:
            if file and allowed_file(file.filename):
               file_zip = os.path.join('web','data','cliente','launcher','update-launcher', file.filename)
               file.save(file_zip)
      return Response(status=200)

@app.route('/launcher/version', methods = ['POST'])
def update_launcher_version():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return Response(status=401)
      config_launcher = os.path.join("web","data","cliente","launcher","package.json")
      content = request.json
      if os.path.exists(config_launcher):
         os.unlink(config_launcher)
      with open(config_launcher, 'w', encoding='utf-8') as f:
         json.dump(content, f, ensure_ascii=False, indent=4)
      return Response(status=200)
