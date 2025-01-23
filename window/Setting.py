from PyQt5 import QtWidgets, uic

import Producer


class setting_dialog(QtWidgets.QDialog):
    
    def __init__(self):

        super().__init__()
        self.settingDialog = uic.loadUi(Producer.route.resourcePath("window/ui/setting.ui"), self)
        
        self.settingDialog.version.setText("版本号：0.5")