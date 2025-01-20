import ctypes
import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon

import Producer
from window import Plan_Dialog, Search_Dialog, Select_Route, Main_Error as Error, Pack_Dialog


ERROR = "请先关闭当前除主窗口外的所有窗口"
JUDGE = False

class main(QtWidgets.QDialog):
    def __init__(self):
        self.num = 0
        
        super().__init__()
        self.ui = uic.loadUi(Producer.route.resourcePath("window/ui/main.ui"), self)
        
        self.ui.plus.clicked.connect(self.scroll_plus)
        self.ui.cut.clicked.connect(self.scroll_cut)

        # 添加广告内容
        self.covers = [
            Producer.route.resourcePath("window/ad/cover_1.png"),
            Producer.route.resourcePath("window/ad/cover_2.png"),
            Producer.route.resourcePath("window/ad/cover_3.png")
        ]
        self.ui.cover.setPixmap(QPixmap(self.covers[self.num]))
        
        if self.num == len(self.covers) - 1:
            self.ui.plus.setIcon(QIcon(Producer.route.resourcePath("window/ui/right_pushed.png")))
        if self.num == 0:
            self.ui.cut.setIcon(QIcon(Producer.route.resourcePath("window/ui/left_pushed.png")))
        
        self.ui.route.clicked.connect(self.Route)
        self.ui.plan.clicked.connect(self.Plan)
        self.ui.search.clicked.connect(self.Search)
        self.ui.pack.clicked.connect(self.Pack)
        self.setObjectName("Main")
        
        
    def Route(self):
        global JUDGE
        if JUDGE == False:
            JUDGE = True
            Select_Route.select_route().show()
        else:
            errorWindow = Error.error()
            errorWindow.show()
            ctypes.windll.user32.MessageBeep(0x00000010)
            
    def Plan(self):
        global JUDGE
        if JUDGE == False:
            JUDGE = True
            Plan_Dialog.plan_dialog().show()
        else:
            errorWindow = Error.error()
            errorWindow.show()
            ctypes.windll.user32.MessageBeep(0x00000010)
        
    def Search(self):
        global JUDGE
        if JUDGE == False:
            JUDGE = True
            Search_Dialog.search_dialog().show()
        else:
            errorWindow = Error.error()
            errorWindow.show()
            ctypes.windll.user32.MessageBeep(0x00000010)
            
    def Pack(self):
        global JUDGE
        if JUDGE == False:
            JUDGE = True
            Pack_Dialog.pack_dialog().show()
        else:
            errorWindow = Error.error()
            errorWindow.show()
            ctypes.windll.user32.MessageBeep(0x00000010)
            
    def scroll_plus(self):
        if self.num < len(self.covers) - 1:
            self.num += 1
            self.ui.cover.setPixmap(QPixmap(self.covers[self.num]))  # 设置广告图片
            self.ui.cover.setScaledContents(True)
            self.ui.cut.setIcon(QIcon(Producer.route.resourcePath("window/ui/left.png")))
        if self.num == len(self.covers) - 1:
            self.ui.plus.setIcon(QIcon(Producer.route.resourcePath("window/ui/right_pushed.png")))
            
    def scroll_cut(self):
        if self.num > 0:
            self.num -= 1
            self.ui.cover.setPixmap(QPixmap(self.covers[self.num]))  # 设置广告图片
            self.ui.cover.setScaledContents(True)
            self.ui.plus.setIcon(QIcon(Producer.route.resourcePath("window/ui/right.png")))
        if self.num == 0:
            self.ui.cut.setIcon(QIcon(Producer.route.resourcePath("window/ui/left_pushed.png")))
            
    def closeEvent(self, event):
        event.accept()
        sys.exit()