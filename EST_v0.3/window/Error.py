from PyQt5 import QtWidgets, uic

import Producer
from window import Plan_Dialog


class error(QtWidgets.QDialog):
    
    def __init__(self):

        super().__init__()
        self.errorDialog = uic.loadUi(Producer.route.resourcePath("window/ui/error.ui"), self)
        
        self.errorDialog.error.setText(Plan_Dialog.ERROR)
        