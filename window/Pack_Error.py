import ctypes
from PyQt5 import QtWidgets, uic

import Producer
from window import Pack_Dialog


class error(QtWidgets.QDialog):
    
    def __init__(self):

        super().__init__()
        self.errorDialog = uic.loadUi(Producer.route.resourcePath("window/ui/error.ui"), self)
        
        ctypes.windll.user32.MessageBeep(0x00000010)
        self.errorDialog.error.setText(Pack_Dialog.ERROR)
        