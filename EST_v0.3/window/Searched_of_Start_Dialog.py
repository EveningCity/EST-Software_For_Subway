from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QFrame, QSizePolicy, QGroupBox, QHBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import Producer, window.Plan_Dialog as Plan_Dialog, window.Route_Dialog as Route_Dialog, window.Search_Plan_Dialog as Search_Plan_Dialog


END_DATA = None
STATION = None

class searched_start_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        self.num = 0
        
        super().__init__()
        self.searchedDialog = uic.loadUi(Producer.route.resourcePath("window/ui/start_dialog.ui"), self)
        
        self.searchedDialog.nameChinese.setText(self.splitStringLine(Search_Plan_Dialog.NAME)[0])
        self.searchedDialog.nameEnglish.setText(self.splitStringUnderline(self.splitStringLine(Search_Plan_Dialog.NAME)[1]))
        
        self.number_1.setAlignment(Qt.AlignCenter)
        self.number_1.setSpacing(6)
        self.number_2.setAlignment(Qt.AlignCenter)
        self.number_2.setSpacing(6)
        self.numberSet(self.splitStringLine(Search_Plan_Dialog.NAME)[0])
        
        self.searchedDialog.start.clicked.connect(self.startClicked)
        
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
        
        for servel_route in Producer.route.stationRouteServel(self.splitStringLine(Search_Plan_Dialog.NAME)[0]):
            
            route = QLabel(f"Route{num}")
            route.setText(f" {Producer.ruleText.formatLineList([servel_route])[0]} ")  
            route.setFont(QFont("黑体", 12))
            
            if len(servel_route) < 5:
                route.setFixedSize(160, 30)
                
            elif len(servel_route) >= 5:
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
        
        global STATION, END_DATA
        STATION = self.splitStringLine(Search_Plan_Dialog.NAME)[0]
        END_DATA = Search_Plan_Dialog.END_DATA
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
        
        for line_and_number in line_and_number_list:
            
            if len(line_and_number[0]) == 1:
                Line = f"0{line_and_number[0]}"
            else:
                Line = line_and_number[0]
                
            if len(str(line_and_number[1])) == 1:
                Number = f"0{str(line_and_number[1])}"
            else:
                Number = str(line_and_number[1])
            
            if line_and_number[0] == "HL20SW":
                continue
            
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