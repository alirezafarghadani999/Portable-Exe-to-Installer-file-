import os
from tkinter import filedialog
from tkinter import *
import tkinter as tk
import shutil
import sys
import time

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


root = tk.Tk()
root.withdraw()

file_path = filedialog.askdirectory()


if(os.path.isdir("installer_folder")):
    shutil.rmtree("installer_folder")

os.system("mkdir installer_folder")
time.sleep(2)
shutil.copytree(file_path,"installer_folder/app")
time.sleep(2)

shutil.copy(resource_path("Install_program.py"),"installer_folder")
shutil.copy(resource_path("Uiinstall.ui"),"installer_folder")

nameapp = input("App name : ")
versionapp = input("App version : ")
formats = input("App Format(exe/py/..) : ")
time.sleep(0.5)
open("installer_folder/ap.ab","w").write(f"{nameapp}_,_{versionapp}_,_{formats}")
open("create_exe.py","w").write(f"""

import os
import shutil
os.system("pip install pyinstaller")
os.system('pyinstaller --noconfirm --onefile --windowed --add-data "installer_folder/app;app/" --add-data "installer_folder/ap.ab;." --add-data "installer_folder/Uiinstall.ui;."   "installer_folder/Install_program.py"')

shutil.rmtree("installer_folder")
shutil.rmtree("build")
os.rmdir("build")
os.remove("Install_program.spec")
os.remove("create_exe.py")



""")

