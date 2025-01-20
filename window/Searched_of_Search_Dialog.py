import importlib
import itertools
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QFrame, QSizePolicy, QGroupBox, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import window.Search_Dialog as Search_Dialog, Producer, window.Route_Dialog as Route_Dialog, window.Plan_Dialog as Plan_Dialog


ROUTE = None
STATION_START = None
STATION_END = None

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

Data = load("Data",Producer.route.resourcePath("data/Data.py"))

class searched_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        self.num = 0
        
        super().__init__()
        self.searchedDialog = uic.loadUi(Producer.route.resourcePath("window/ui/searched_dialog.ui"), self)
        
        self.searchedDialog.nameChinese.setText(self.splitStringLine(Search_Dialog.NAME)[0])
        self.searchedDialog.nameEnglish.setText(self.splitStringUnderline(self.splitStringLine(Search_Dialog.NAME)[1]))
        
        self.number_1.setAlignment(Qt.AlignCenter)
        self.number_1.setSpacing(6)
        self.number_2.setAlignment(Qt.AlignCenter)
        self.number_2.setSpacing(6)
        self.numberSet(self.splitStringLine(Search_Dialog.NAME)[0])
        
        self.searchedDialog.start.clicked.connect(self.startClicked)
        self.searchedDialog.end.clicked.connect(self.endClicked)
        
        self.scroll_layout = QVBoxLayout()  
        self.scroll_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.searchedDialog.scrollArea.widget().setLayout(self.scroll_layout)  

        self.addRouteText()
        self.addRouteView()
        
        
    def addRouteText(self):
            
        route_text = QLabel("Route")
        route_text.setText("线路概览")
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
        self.buttons = {}
        self.routes = []
        
        for servel_route in Producer.route.stationRouteServel(self.splitStringLine(Search_Dialog.NAME)[0]):
            
            button = QPushButton(f"Route{num}")
            button.setText(f" {Producer.ruleText.formatLineList([servel_route])[0]} ")
            button.setFont(QFont("黑体", 12))
            
            if len(Producer.ruleText.formatLineList([servel_route])[0]) < 5:
                button.setFixedSize(160, 30)
                
            elif len(Producer.ruleText.formatLineList([servel_route])[0]) >= 5:
                button.setFixedSize(250, 30)
                
            button.setStyleSheet("""
            QPushButton {{
                color: rgb(255,255,255);
                border: 2px solid {}; 
                background-color: {}; 
                border-radius: 10px; 
            }}
            QPushButton:hover {{
                background-color: {}; 
            }}
            QPushButton:pressed {{
                border: 2px solid {}; 
                background-color: {}; 
            }}
            """.format(Producer.ruleText.colorRoute(servel_route),
                       Producer.ruleText.colorRoute(servel_route),
                       Producer.ruleText.darkerColor(Producer.ruleText.colorRoute(servel_route)),
                       Producer.ruleText.darkerColor(Producer.ruleText.colorRoute(servel_route)),
                       Producer.ruleText.darkerColor(Producer.ruleText.colorRoute(servel_route))))
            button.clicked.connect(lambda checked, btn=num: self.afterRouteClick(btn))
            self.scroll_layout.addWidget(button)  
            
            self.routeDescription(servel_route, num)
            self.buttons[num] = button
            self.routes.append([num, servel_route])
            
            num = num + 1
        
    
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
        
        
    def afterRouteClick(self, num):
        
        for route in self.routes:
            
            if route[0] == num:
                global ROUTE
                ROUTE = route[1]
        
        self.routeDialog = Route_Dialog.route_dialog()
        self.routeDialog.show()
        self.close()
    
     
    def startClicked(self):
        
        global STATION_START
        STATION_START = self.splitStringLine(Search_Dialog.NAME)[0]
        Plan_Dialog.plan_dialog().show()
        
        
    def endClicked(self):
        
        global STATION_END
        STATION_END = self.splitStringLine(Search_Dialog.NAME)[0]
        Plan_Dialog.plan_dialog().show()
     
     
    def splitStringLine(self, input):
        
        list = input.split(" | ")
        result = [item.strip() for item in list]
        
        return result
    
    
    def splitStringUnderline(self, input):
        
        list = input.split("_")
        result = '/'.join([item.strip() for item in list])
        
        return result
       
       
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