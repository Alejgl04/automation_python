import os
import shutil

from tkinter import Tk, filedialog

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
      
      target = os.path.join(root, extensions[ext], file)
      
      shutil.move(file_root, target)