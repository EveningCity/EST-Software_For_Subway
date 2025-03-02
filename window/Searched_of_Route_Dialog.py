import importlib
import itertools
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame, QSizePolicy, QGroupBox, QHBoxLayout
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import Producer, window.Plan_Dialog as Plan_Dialog, window.Route_Dialog as Route_Dialog


ROUTE = None

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

Data = load("Data",Producer.route.resourcePath("data/Data.py"))

class searched_route_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        self.num = 0
        
        super().__init__()
        self.searchedDialog = uic.loadUi(Producer.route.resourcePath("window/ui/searched_dialog.ui"), self)
        
        self.searchedDialog.nameChinese.setText(Producer.ruleText.betterChinese(Route_Dialog.ROUTE_NAME[0]))
        self.searchedDialog.nameEnglish.setText(Producer.ruleText.betterEnglish(Route_Dialog.ROUTE_NAME[1]))
        self.subTitle(Route_Dialog.ROUTE_NAME)
        
        self.number_1.setAlignment(Qt.AlignCenter)
        self.number_1.setSpacing(6)
        self.number_2.setAlignment(Qt.AlignCenter)
        self.number_2.setSpacing(6)
        self.numberSet(Route_Dialog.ROUTE_NAME[0])
        
        self.searchedDialog.start.clicked.connect(self.startClicked)
        self.searchedDialog.end.clicked.connect(self.endClicked)
        
        self.scroll_layout = QVBoxLayout()
        self.scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.searchedDialog.scrollArea.widget().setLayout(self.scroll_layout)

        self.addText("线路概览")
        self.addRouteView()
        self.addAir()
        self.addText("车站信息")
        self.addstationView()
        self.loadPic()
        
        
    def addText(self, word):
            
        route_text = QLabel("Text")
        route_text.setText(word)
        route_text.setFont(QFont("黑体", 16))
        route_text.setAlignment(Qt.AlignLeft)
        self.scroll_layout.addWidget(route_text)
        
        horizontal_line = QFrame()
        horizontal_line.setFrameShape(QFrame.HLine)
        horizontal_line.setFrameShadow(QFrame.Plain)
        horizontal_line.setLineWidth(2)
        horizontal_line.setStyleSheet("color: #33373E;")
        horizontal_line.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
        self.scroll_layout.addWidget(horizontal_line)
        
        
    def addRouteView(self):
        
        num = 0
        
        for servel_route in Producer.route.stationRouteServel(Route_Dialog.ROUTE_NAME[0]):
            
            route = QLabel(f"Route{num}")
            route.setText(f" {Producer.ruleText.formatLineList([servel_route])[0]} ")
            route.setFont(QFont("黑体", 12))
            
            if len(Producer.ruleText.formatLineList([servel_route])[0]) < 5:
                route.setFixedSize(160, 30)
                
            elif len(Producer.ruleText.formatLineList([servel_route])[0]) >= 5:
                route.setFixedSize(250, 30)
                
            route.setStyleSheet("""
            QLabel {{
                color: rgb(255,255,255);
                border: 2px solid {}; 
                background-color: {}; 
                border-radius: 10px; 
            }}
            """.format(Producer.ruleText.colorRoute(servel_route),
                       Producer.ruleText.colorRoute(servel_route),
                       Producer.ruleText.darkerColor(Producer.ruleText.colorRoute(servel_route)),
                       Producer.ruleText.darkerColor(Producer.ruleText.colorRoute(servel_route)),
                       Producer.ruleText.darkerColor(Producer.ruleText.colorRoute(servel_route))))
            route.setAlignment(Qt.AlignCenter)
            self.scroll_layout.addWidget(route)
            
            self.routeDescription(servel_route, num)
            
            num = num + 1
            
            
    def addstationView(self):
        
        name = Route_Dialog.ROUTE_NAME[1]
        for des in Data.DESCRIPTION:
            if des[0] == name:
                n = QLabel("Station")
                n.setText(des[1])  
                n.setFont(QFont("黑体", 12))
                n.setAlignment(Qt.AlignLeft)
                n.setWordWrap(True)
                self.scroll_layout.addWidget(n)
                
                
    def addAir(self):
        
        a = QLabel("Air")
        a.setText(" ")
        self.scroll_layout.addWidget(a)
        
        
    def subTitle(self, lst):
        
        if len(lst) != 2:
            self.searchedDialog.subNameChinese.setText(Producer.ruleText.betterChinese(lst[2]))
            self.searchedDialog.subNameEnglish.setText(f"({Producer.ruleText.betterEnglish(lst[3])})")
        else:
            self.searchedDialog.subNameChinese.setText(" ")
            self.searchedDialog.subNameEnglish.setText(" ")
        
    
    def routeDescription(self, route, Times):
        
        route_description = QLabel(f"Desciption{Times}")
        route_description.setText(Producer.ruleText.describeRoute(route))
        route_description.setFont(QFont("黑体", 12))
        route_description.setStyleSheet("""
        QLabel {
            border: None; 
        }
        """)
        route_description.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.scroll_layout.addWidget(route_description)
    
     
    def startClicked(self):
        
        STATION_START = Route_Dialog.ROUTE_NAME[0]
        Dialog = Plan_Dialog.plan_dialog()
        Dialog.show()
        Dialog.fillAir([STATION_START, "Start"])
        
        
    def endClicked(self):
        
        STATION_END = Route_Dialog.ROUTE_NAME[0]
        Dialog = Plan_Dialog.plan_dialog()
        Dialog.show()
        Dialog.fillAir([STATION_END, "End"])
        
        
    def loadPic(self):
        
        files_name_list = []
        for filename in os.listdir(Producer.route.resourcePath("data/stations/")):
            file_path = os.path.join(Producer.route.resourcePath("data/stations/"), filename)
            if os.path.isfile(file_path):
                files_name_list.append(filename)
            if filename.replace(".png", "").replace(".jpg", "").replace(".jpeg", "")  == Route_Dialog.ROUTE_NAME[1]:
                self.label = QLabel()
                self.label.setAlignment(Qt.AlignCenter)
                self.label.setWordWrap(True)
                self.pixmap = QPixmap(file_path)
                self.scroll_layout.addWidget(self.label)
                
           
    def updateImageSize(self):
        """根据窗口大小调整图片大小"""
            
        try:
            # 获取窗口的可用宽度和高度
            window_width = self.searchedDialog.scrollArea.width() - 40
            window_height = self.height()

            # 计算图片的最大显示尺寸，保持宽高比
            scaled_pixmap = self.pixmap.scaled(window_width, window_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(scaled_pixmap)
        except:
            return
           
                
    def resizeEvent(self, event):
        """重写窗口大小改变事件"""
        
        try:
            super().resizeEvent(event)
            self.updateImageSize()  # 更新图片大小  
        except:
            return

       
    def numberSet(self, name):
        
        line_and_number_list = Producer.route.stationRouteAndNumberServel(name)
        num = 0
        Lines = []
        lines = []
        
        for ln_original in line_and_number_list:
            SKIP = False
            for l_branch in Data.BRANCH_LINE_LIST:
                if ln_original[0] == l_branch[1]:
                    SKIP = True
                    if l_branch[0] != 'False':
                        lines.append(l_branch[0])
                    break
            if SKIP == True:
                continue
            else:
                lines.append(ln_original[0])
            
        lines_setted = list(set(lines))
        
        for line_and_number in line_and_number_list:
            END = False
            Y = False
            
            for direct_line in Data.DIRECT_LINE_LIST:
                if line_and_number[0] == direct_line[0]:
                    END = True
            
            if len(line_and_number[0]) == 1:
                Line = f"0{line_and_number[0]}"
            else:
                Line = line_and_number[0]
                
            if len(str(line_and_number[1])) == 1:
                Number = f"0{str(line_and_number[1])}"
            else:
                Number = str(line_and_number[1])
            
            for branch in Data.BRANCH_LINE_LIST:
                if line_and_number[0] == branch[1]:
                    
                    if branch[0] == "False":
                        END = True
                    
                    else:
                        Line = branch[0]
                        
                    if len(lines_setted) == len(lines):
                        Y = True
            
            if END == True:
                continue
            
            if Y == True:
                Number = f"Y{Number}"
            
            if Line in Lines:
                continue
            Lines.append(Line)
                        
            groupBoxLayout = QHBoxLayout()
            groupBoxLayout.setContentsMargins(8,0,8,0)
                
            groupBox = QGroupBox()
            groupBox.setTitle("")
            groupBox.setLayout(groupBoxLayout)
            groupBox.setStyleSheet("""
            QGroupBox {{
                color: black;
                border: 2px solid {};
                border-radius: 10px;
            }}
            """.format(Producer.ruleText.colorRoute(line_and_number[0])))
            
            number = QLabel()
            number.setText(Number)
            number.setFont(QFont("微软雅黑", 10, QFont.Bold))
            number.setAlignment(Qt.AlignCenter)
            number.setStyleSheet("color: {};".format(Producer.ruleText.colorRoute(line_and_number[0])))
            number.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            groupBoxLayout.addWidget(number)
            
            vertical_line = QFrame()
            vertical_line.setFrameShape(QFrame.VLine)
            vertical_line.setFrameShadow(QFrame.Plain)
            vertical_line.setLineWidth(2)
            vertical_line.setStyleSheet("color: {};".format(Producer.ruleText.colorRoute(line_and_number[0])))
            groupBoxLayout.addWidget(vertical_line)
            
            route = QLabel()
            route.setText(Line)
            route.setFont(QFont("微软雅黑", 10, QFont.Bold))
            route.setAlignment(Qt.AlignCenter)
            route.setStyleSheet("color: {};".format(Producer.ruleText.colorRoute(line_and_number[0])))
            route.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            groupBoxLayout.addWidget(route)
            
            if num % 2 == 0:
                self.number_1.addWidget(groupBox)
                
            else:
                self.number_2.addWidget(groupBox)
                
            num = num + 1
            
            
    def closeEvent(self, event):
        self.searchedDialog.deleteLater()
        event.accept()