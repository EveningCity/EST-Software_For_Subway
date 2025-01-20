import ctypes
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication

import Producer
from window import Pack_Dialog

TEXT = None
BTN = None
KEYED = None

class sure(QtWidgets.QDialog):
    
    def __init__(self):

        ctypes.windll.user32.MessageBeep(0x00000010)
        
        super().__init__()
        self.sureDialog = uic.loadUi(Producer.route.resourcePath("window/ui/sure.ui"), self)
        
        self.sureDialog.que.setText(TEXT)
        
        self.sureDialog.yes.clicked.connect(self.ifYes)
        self.sureDialog.cancel.clicked.connect(self.ifCancel)
        
    def ifYes(self):
        yes = "no"
        global BTN, KEYED
        KEYED = Pack_Dialog.KEYED
        Pack_Dialog.KEYED = ""
        
        for name in Pack_Dialog.pack_dialog().names:
            if name[0] == BTN:
                yes = "yes"
                NAME = name
        
        if yes == "yes":
            os.remove(Producer.route.resourcePath(f"pack/{NAME[1]}"))
            
            for window in QApplication.topLevelWidgets():
                if window.objectName() != "Main":
                    window.close()
            
        Pack_Dialog.pack_dialog().show()
        KEYED = None
        
    def ifCancel(self):
        self.sureDialog.deleteLater()
        
    def closeEvent(self, event):
        self.sureDialog.deleteLater()
        event.accept()