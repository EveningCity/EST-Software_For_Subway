from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QApplication, QGroupBox, QFrame, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from window import Plan_Dialog, Route_Dialog
import Producer


ROUTE = None

class planView(QtWidgets.QDialog):
    
    def __init__(self):
        
        self.num = 0
        self.buttons = {}
        self.routes = []
        
        super().__init__()
        self.searchDialog = uic.loadUi(Producer.route.resourcePath("window/ui/plan_result_dialog.ui"), self)
        
        self.searchDialog.pushButton.clicked.connect(self.afterClick)
        
        self.p_layout = QVBoxLayout()  
        self.searchDialog.scrollArea.widget().setLayout(self.p_layout) 
        
        #首先执行的命令
        self.planView()
            
        
    def planView(self):
        
        btn_number = 0
            
        self.p_layout.setAlignment(Qt.AlignTop)
        
        for plan_list, plan_name in zip(Plan_Dialog.RESULT.values(), Plan_Dialog.RESULT.keys()):
            
            groupBoxLayout = QVBoxLayout()
            
            groupBox = QGroupBox(f"GroupBox{btn_number}")
            groupBox.setTitle("")
            groupBox.setLayout(groupBoxLayout)
            groupBox.setStyleSheet("""
            QGroupBox {
                color: black;
                border: 2px solid #33373E; /* 边框宽度和颜色 */
                border-radius: 10px; /* 边框圆度 */;
                background-color: white;
            }
            """)
            self.p_layout.addWidget(groupBox)  
            
            
            planLayout = QHBoxLayout()
            groupBoxLayout.addLayout(planLayout)
            
            plan_text = QLabel(f"Route{btn_number}")
            plan_text.setText(plan_name) 
            plan_text.setFont(QFont("黑体", 16))
            planLayout.addWidget(plan_text)  
            
            side_text = QLabel()
            side_text.setText(f"当前方案所需站点数为{plan_list[4][0]}座")
            side_text.setFont(QFont("黑体", 10))
            side_text.setAlignment(Qt.AlignBottom | Qt.AlignRight)
            planLayout.addWidget(side_text)  
            
            
            horizontal_line = QFrame()
            horizontal_line.setFrameShape(QFrame.HLine)
            horizontal_line.setFrameShadow(QFrame.Plain)
            horizontal_line.setLineWidth(2)
            horizontal_line.setStyleSheet("color: #33373E;")
            groupBoxLayout.addWidget(horizontal_line)

            
            for stationNumber,stationName,route,direction in zip(plan_list[1],plan_list[2],plan_list[3],plan_list[5]):
                
                nameLayout = QHBoxLayout()
                nameLayout.setAlignment(Qt.AlignLeft)
                groupBoxLayout.addLayout(nameLayout)
        
                servelStationName = QLabel(f"Label{btn_number}")
                servelStationName.setText(stationName)
                servelStationName.setFont(QFont("黑体", 12))
                nameLayout.addWidget(servelStationName)
                nameLayout.addWidget(self.routeButton(route))
                
                
                usefulLayout = QHBoxLayout()
                usefulLayout.setAlignment(Qt.AlignLeft)
                groupBoxLayout.addLayout(usefulLayout)
                
                vertical_line = QFrame()
                vertical_line.setFrameShape(QFrame.VLine)
                vertical_line.setFrameShadow(QFrame.Plain)
                vertical_line.setLineWidth(1)
                vertical_line.setStyleSheet("color: #33373E;")
                usefulLayout.addWidget(vertical_line)
                
                
                if direction != 0:
                    
                    informationLayout = QVBoxLayout()
                    informationLayout.setAlignment(Qt.AlignTop)
                    usefulLayout.addLayout(informationLayout)
                
                    servelStationNumber = QLabel(f"Number{btn_number}")
                    servelStationNumber.setText(f"所需的站点数为{stationNumber}座")
                    servelStationNumber.setFont(QFont("黑体", 10))
                    informationLayout.addWidget(servelStationNumber)
                
                    servelDirection = QLabel(f"Direction{btn_number}")
                    servelDirection.setText(direction)
                    servelDirection.setFont(QFont("黑体", 10))
                    informationLayout.addWidget(servelDirection)
            
            
            btn_number = btn_number + 1
            
            
    def afterClick(self):
        
        for window in QApplication.topLevelWidgets():
            if window.objectName() != "Main":
                window.deleteLater()
                
        Plan_Dialog.plan_dialog().show()
        
    
    def routeButton(self, servel_route):
        
        button = QPushButton(f"Route{self.num}")
        button.setText(f" {Producer.ruleText.formatLineList([servel_route])[0]} ")  
        button.setFont(QFont("黑体", 10))
        button.setFixedHeight(20)
            
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
        button.clicked.connect(lambda checked, btn=self.num: self.afterRouteClick(btn))
        self.buttons[self.num] = button
        self.routes.append([self.num, servel_route])
            
        self.num = self.num + 1
        
        return(button)
    
    
    def afterRouteClick(self, num):
        
        for route in self.routes:
            
            if route[0] == num:
                global ROUTE
                ROUTE = route[1]
        
        self.routeDialog = Route_Dialog.route_dialog()
        self.routeDialog.show()
        
        
    def closeEvent(self, event):
        self.searchDialog.deleteLater()
        event.accept()