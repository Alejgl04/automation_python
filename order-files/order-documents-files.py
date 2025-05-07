import os
import shutil
import getpass

from tkinter import Tk, filedialog
from datetime import datetime

user = getpass.getuser() 

window = Tk()

window.withdraw()

root = filedialog.askdirectory(title="Select the folder to order")

extensions = {
  '.jpg': 'Images',
  '.png': 'Images',
  '.pdf': 'PDFs',
  '.docx': 'Documents_word',
  '.txt': 'Documents_txt',
}

for folder in set(extensions.values()):
  
  folder_root = os.path.join(root, folder)
  if not os.path.exists(folder_root):
    os.makedirs(folder_root)


for file in os.listdir(root):
  
  file_root= os.path.join(root,file)
  
  if os.path.isfile(file_root):
    
    name, ext= os.path.splitext(file)
    ext = ext.lower()
    
    if ext in extensions:
      
      # target = os.path.join(root, extensions[ext], file)
      # Get date by latest modification
        
      get_folder_mod = datetime.fromtimestamp(os.path.getmtime(file_root))
      subfolder_by_date = get_folder_mod.strftime("%m-%Y") #Format to "2025-05"# 
      
      #Create sub folder if does not exist 
      folder_type = os.path.join(root, extensions[ext])
      folder_date = os.path.join(folder_type,subfolder_by_date)
      
      if not os.path.exists(folder_date):
        os.makedirs(folder_date)
      
      target = os.path.join(folder_date, file)
      
      shutil.move(file_root, target)
      
      with open( os.path.join(root, "log_detail.txt"), "a", encoding="utf-8") as log:
        log.write(f"{datetime.now().strftime('%m-%d-%Y')} - Username: {user} - Moved: {file} -> {target}\n")