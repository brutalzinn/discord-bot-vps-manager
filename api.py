from flask import Flask, render_template, request, Response
import os
from pyunpack import Archive
import json
from flask import jsonify


app = Flask(__name__)

@app.route('/list/modpacks', methods = ['GET'])
def get_modpacks():
      if request.headers.get('api-key') != 'teste':
         return Response(status=401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      f = open(modpacks)
      data = json.load(f)
      f.close()
      return jsonify(data)

@app.route('/update/modpacks', methods = ['POST'])
def add_modpack():
      if request.headers.get('api-key') != 'teste':
         return Response(status=401)
      modpacks = os.path.join("web","data","cliente","launcher","config-launcher","modpacks.json")
      content = request.json
      with open(modpacks, 'w', encoding='utf-8') as f:
         json.dump(content, f, ensure_ascii=False, indent=4)
      return Response(status=200)

@app.route('/config/launcher', methods = ['POST'])
def add_modpack():
      if request.headers.get('api-key') != 'teste':
         return Response(status=401)
      config_launcher = os.path.join("web","data","cliente","launcher","config-launcher","config.json")
      content = request.json
      with open(config_launcher, 'w', encoding='utf-8') as f:
         json.dump(content, f, ensure_ascii=False, indent=4)
      return Response(status=200)

@app.route('/upload/moodpacks', methods = ['GET', 'POST'])
def upload_file():
   if request.headers.get('api-key') != 'teste':
      return Response(status=401)
   if request.method == 'POST':
      f = request.files['file']
      directory = request.form.get('directory')
      if not os.path.exists(os.path.join("web","data","cliente","files","files",directory)):
         os.mkdir(os.path.join("web","data","cliente","files","files",directory))
      if f.filename.split('.')[1]  != 'zip':
        return Response(status=401)
      file_zip = os.path.join("web","data","cliente","files","files", f.filename)
      file_zip_out = os.path.join("web","data","cliente","files","files",directory)
      try:
         f.save(file_zip)
         Archive(file_zip).extractall(file_zip_out)
         os.unlink(file_zip)
      except:
         print("Deu erro.")
         return Response(status=401)
      return Response(status=200)
		
