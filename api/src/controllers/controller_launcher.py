import os
from pyunpack import Archive
from flask import json, request
from flask_restx import  abort
from src.server.instance import server
from src.utils.api_utils import *
from glob import glob
from flask.helpers import make_response

app, api = server.app, server.api

@app.route('/launcher/modpacks/list', methods = ['GET'])
def get_modpacks():
    if request.headers.get('api-key') != os.getenv('API_TOKEN'):
        return abort(401, custom='No api key')
    modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
    f = open(modpacks)
    data = json.load(f)
    f.close()
    return json.jsonify(data)

@app.route('/launcher/config', methods = ['POST'])
def update_config():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return abort(401, custom='No api key')
      config_launcher = os.path.join("web","data","cliente","launcher","config-launcher","config.json")
      content = request.json
      with open(config_launcher, 'w', encoding='utf-8') as f:
         json.dump(content, f, ensure_ascii=False, indent=4)
      return make_response('',200)


#This route is called when a modpack is updated by modpack creator.
#We need clear redis cache before update the new modpack 
#and we need to put launcher in maintance mod too.

@app.route('/launcher/modpacks/upload', methods = ['POST'])
def upload_file():
   if request.headers.get('api-key') != os.getenv('API_TOKEN'):
      return abort(401)
   if request.method == 'POST':
      f = request.files['file']
      directory = request.form.get('directory')
      os.umask(0)
      if not os.path.exists(os.path.join('web','data','cliente','files','files',directory)):
          os.umask(0)
          os.makedirs(os.path.join('web','data','cliente','files','files',directory), mode=0o777)
      if f.filename.split('.')[1]  != 'zip':
        return abort(400)
      file_zip = os.path.join('web','data','cliente','files','files', f.filename)
      file_zip_out = os.path.join('web','data','cliente','files','files',directory)
      try:
         f.save(file_zip)
         Archive(file_zip).extractall(file_zip_out)
         os.unlink(file_zip)
      except:
         print('Deu erro.')
         return abort(400)
      return make_response('',200)


#THIS ROUTE IS TO BE USED TO SEND MULTIPLE LAUNCHER ZIPS WITH THE LAUNCHER UPDATED VERSIONS.

@app.route('/launcher/version/upload', methods = ['POST'])
def update_launcher_zips():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return abort(401)
      if request.method == 'POST':
         files = request.files.getlist('file')
         for file in files:
            if file and allowed_file(file.filename):
               file_zip = os.path.join('web','data','cliente','launcher','update-launcher', file.filename)
               file.save(file_zip)
      return make_response('',200)

# UPDATE LAUNCHER VERSION FILE. YOU WILL CALL THIS ROUTE BEFORE /LAUNCHER/UPLOAD/UPDATE.
# THIS ROUTE WILL CHECK THE LAUNCHER VERSION FOR WIN,MAC AND LINUX. 
# THIS ROUTE WILL DELETE OLD LAUNCHER VERSION FILE TOO.

@app.route('/launcher/version', methods = ['POST', 'GET'])
def update_launcher_version():
      if request.headers.get('api-key') != os.getenv('API_TOKEN'):
         return abort(401)
      config_launcher = os.path.join('web','data','cliente','launcher','package.json')
      launcher_dir = os.path.join('web','data','cliente','launcher','update-launcher')
      olds = []
      old_launcher = glob(os.path.join('web','data','cliente','launcher','update-launcher',"*"), recursive = True)
   
      for path in old_launcher:
         olds.append(FileDir(getFileNameByURL(path),path))
      if request.method == 'POST':
         content = request.get_json()
         if os.path.exists(config_launcher):
            package = open(config_launcher)
            backup_launcher = json.load(package)
            for item in content['packages']:
               sistema = content['packages'][item]
               if sistema is None:
                  content['packages'][item] = backup_launcher['packages'][item]
               else:
                  filename = getFileNameByURL(sistema['url'])
                  teste = checkFilename(filename, olds)
                  if not teste:
                     antigo = getFileNameByURL(backup_launcher['packages'][item]['url'])
                     dir_antigo = os.path.join(launcher_dir, antigo)
                     if os.path.exists(dir_antigo):
                        os.unlink(dir_antigo)
      
         with open(config_launcher, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
         return make_response('',200)
      elif request.method == 'GET':
         f = open(config_launcher)
         return json.load(f)