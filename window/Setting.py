from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

import Producer
import Station_Search
from window import Make_Dialog


class setting_dialog(QtWidgets.QDialog):
    
    def __init__(self):

        super().__init__()
        self.settingDialog = uic.loadUi(Producer.route.resourcePath("window/ui/setting.ui"), self)
        
        self.settingDialog.version.setText("版本号：0.6\n分享软件请注明作者（雨城Evening_City）\n\n当前已加载的站点数为{}座\n当前已加载的线路数为{}条".format(len(Station_Search.station_name),self.get_route_amount()))
        self.settingDialog.bilibili.clicked.connect(self.open_bilibili_url)
        self.settingDialog.github.clicked.connect(self.open_github_url)
        self.settingDialog.aifadian.clicked.connect(self.open_aifadian_url)
        self.settingDialog.make.clicked.connect(self.open_make)
        self.get_route_amount()
        
    def open_bilibili_url(self):
        url = "https://space.bilibili.com/157769701"
        QDesktopServices.openUrl(QUrl(url))

    def open_github_url(self):
        url = "https://github.com/EveningCity"
        QDesktopServices.openUrl(QUrl(url))
        
    def open_aifadian_url(self):
        url = "https://afdian.com/a/evening_city233"
        QDesktopServices.openUrl(QUrl(url))
        
    def open_make(self):
        Make_Dialog.make_dialog().exec_()
        
    def get_route_amount(self):
        rl = []
        for ran in Producer.station:
            rl.append(Producer.route.filterStr(Producer.route.flatten(ran[:-1])))
            
        rl_last = list(set(Producer.route.flatten(rl)))
            
        return(len(rl_last))