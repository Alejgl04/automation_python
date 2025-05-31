import os
import shutil
import getpass
import threading
import time

from tkinter import Tk, filedialog, Button, Label
from datetime import datetime


from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
  '.mp4': 'Videos MP4',
}

class EventHandler(FileSystemEventHandler):
  
  def on_created(self, event):
    if not event.is_directory:
      print(f"New file detected: {event.src_path}")
      sort_files(root)

def expectfile_tobe_free(file_root, attemps=10, wait=0.5):
  
  for _ in range(attemps):
    try:
      with open(file_root, "rb"):
        return True
    except (PermissionError, OSError):
      time.sleep(wait)
  
  return False

def sort_files(root):
  
  for file in os.listdir(root):
  
    file_root= os.path.join(root,file)
  
    if os.path.isfile(file_root) and file !="log_detail.txt":
    
      if not expectfile_tobe_free(file_root):
        print(f"We cannot access the file {file} because is being used")
        continue
      
      name, ext= os.path.splitext(file)
      ext = ext.lower()
      
      if ext in extensions:
        
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

for folder in set(extensions.values()):
  
  folder_root = os.path.join(root, folder)
  if not os.path.exists(folder_root):
    os.makedirs(folder_root)


sort_files(root)

event_handler = EventHandler()
observer = Observer()
observer.schedule(event_handler, root, recursive=False)

def start_monitoring():
  observer.start()

def stop_monitoring():
  observer.stop()
  observer.join()
  window.quit()


window.deiconify()
window.title("Monitoring Folder")
window.geometry("400x150")

Label(window, text=f"Monitoring the folder: \n{root}", wraplength=350).pack(pady=10)
Button(window, text="Stop monitoring and out", command=stop_monitoring).pack(pady=10)

threads_monitoring = threading.Thread(target=start_monitoring, daemon=True )
threads_monitoring.start()

window.mainloop()
