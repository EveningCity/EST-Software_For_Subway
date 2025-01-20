import ctypes
import os
import shutil
import subprocess
import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication

import Producer
from window import Main, Pack_Dialog

TEXT = None
BTN = None

class sure(QtWidgets.QDialog):
    
    def __init__(self):

        ctypes.windll.user32.MessageBeep(0x00000010)
        
        super().__init__()
        self.sureDialog = uic.loadUi(Producer.route.resourcePath("window/ui/sure.ui"), self)
        
        self.sureDialog.que.setText(TEXT)
        
        self.sureDialog.yes.clicked.connect(self.ifYes)
        self.sureDialog.cancel.clicked.connect(self.ifCancel)
        
    def ifYes(self):
        global BTN
        for name in Pack_Dialog.pack_dialog().names:
            
            if name[0] == BTN:
                
                src_file = Producer.route.resourcePath(f"pack/{name[1]}")
                dst_folder = Producer.route.resourcePath("")
                dst_file = os.path.join(dst_folder, Producer.route.resourcePath("data/Data.py"))

                shutil.copy(src_file, dst_file)
                
                Main.JUDGE = False  
                python = sys.executable
                subprocess.Popen([python] + sys.argv)
                sys.exit(0)
        
    def ifCancel(self):
        self.sureDialog.deleteLater()
        
    def closeEvent(self, event):
        self.sureDialog.deleteLater()
        event.accept()