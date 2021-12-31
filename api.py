from flask import Flask, render_template, request, Response
import os
from pyunpack import Archive

app = Flask(__name__)

@app.route('/uploader', methods = ['GET', 'POST'])
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
		
