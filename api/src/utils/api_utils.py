class FileDir:
      def __init__(self,filename, path):
         self.filename = filename
         self.path = path

ALLOWED_EXTENSIONS = set(['zip'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkExistId(store_list, value):
   exist = False
   for item in store_list:
         if item['id'] == value:
            exist = True
   return exist

def checkFilename(item, list):
   exist = False
   for f in list:
         if f.filename == item:
            exist = True
   return exist

def getFileNameByURL(url:str):
   splitter = url.split('/')
   index = len(splitter) - 1
   return splitter[index]