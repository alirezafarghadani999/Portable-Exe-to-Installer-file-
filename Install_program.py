
from PyQt5 import QtWidgets, uic
import sys
import os
from tkinter import filedialog
from tkinter import *
import tkinter as tk
import shutil
import os, winshell
from win32com.client import Dispatch

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


install_path = "C:\Program Files"
name = open(resource_path("ap.ab"),"r").read().split("_,_")[0]
version = open(resource_path("ap.ab"),"r").read().split("_,_")[1]
formatapp = open(resource_path("ap.ab"),"r").read().split("_,_")[2]

appfolder_toinstall = resource_path("app/")
exefiletoinstall = resource_path(f"{install_path}/{name}.{formatapp}")
shortcut = False
log = "------ Start Log --------\n"
installed = False

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        global install_path,name,version,installed
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi(resource_path('Uiinstall.ui'), self) # Load the .ui file

        self.adrdir.setText(f"{install_path}/{name}")
        self.Appname.setText(f"Name : {name}")
        self.Version.setText(f"Version : {version}")

        self.browser = self.findChild(QtWidgets.QPushButton, 'selectdir')
        self.browser.clicked.connect(self.openfilebrowser) 

        self.scd = self.findChild(QtWidgets.QRadioButton , 'surtcut')
        self.scd.toggled.connect(self.shortcutsel)

        self.installb = self.findChild(QtWidgets.QPushButton, 'install')

        if installed :
            self.installb.clicked.connect(self.exitapp)
            self.installb.setText("Exit")
        else:
            self.installb.clicked.connect(self.installss)
            



        self.show() # Show the GUI

    def openfilebrowser(self):
        global install_path,name,version,exefiletoinstall
        
        root = tk.Tk()
        root.withdraw()

        install_path = filedialog.askdirectory()
        if install_path != "":
            self.adrdir.setText(f"{install_path}/{name}")
            exefiletoinstall = resource_path(f"{install_path}/{name}.{formatapp}")
        else:
            install_path = "C:\Program Files"
            

    def shortcutsel(self, selected):
        global shortcut
        if selected:
            shortcut = True
        else:
            shortcut = False

    def installss(self):
        global install_path,name,version,exefiletoinstall,log,shortcut,installed

        log +=f"- Extract file in {install_path}\{name}\n"
        shutil.copytree(resource_path("app"),f"{install_path}\{name}")
        self.log.setText(log)
        if shortcut :
            log +=f"- create shortcut {install_path}\{name}\n"
            self.log.setText(log)
            desktop = winshell.desktop()
            path = os.path.join(desktop, f"{name}.lnk")
            target = f"{install_path}/{name}/{name}.{formatapp}"
            wDir = f"{install_path}/{name}"
            icon = f"{install_path}/{name}/{name}.{formatapp}"
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
        log += "------ End Log --------\n"
        self.log.setText(log)
        installed = True
    
    def exitapp():
        print("hi")


                
app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()

