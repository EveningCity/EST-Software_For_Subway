import importlib
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QSizePolicy, QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import Producer, window.Route_Dialog as Route_Dialog, Station_Search, window.Main as Main


ROUTE = None

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

Data = load("Data",Producer.route.resourcePath("data/Data.py"))

class select_route(QtWidgets.QDialog):

    def __init__(self):
        
        self.num = 0
        
        super().__init__()
        self.routeDialog = uic.loadUi(Producer.route.resourcePath("window/ui/select_route.ui"), self)
        
        self.p_layout = QVBoxLayout()  
        self.routeDialog.scrollArea.widget().setLayout(self.p_layout)  
        
        self.routeDialog.pushButton.clicked.connect(self.addRoute)
        
        self.addRoute()
        
        self.setObjectName("Select")
        for window in QApplication.topLevelWidgets():
            if window.objectName() != "Main" and window != self:
                window.deleteLater()
        
        
    def addRoute(self):
        
        num = 0
        self.buttons = {}
        self.routes = []
        
        query = self.routeDialog.searchText.text()
        result = Station_Search.fuzzy_search(query, [Producer.ruleText.formatLineList([item])[0] for item in Data.ALL_LINE_LIST])
        
        if self.num != 0:
            self.clearLayout(self.p_layout)
            
        self.num = self.num + 1
        
        if isinstance(result, list):
            self.p_layout.setAlignment(Qt.AlignTop)
            
            result_formal = [Data.ALL_LINE_DICT[key] for key in result]
        
            for servel_route in result_formal:
                
                button = QPushButton(f"Route{num}")
                button.setText(f" {Producer.ruleText.formatLineList([servel_route])[0]} ")  
                button.setFont(QFont("黑体", 12))
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                button.setFixedHeight(30)
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
                button.clicked.connect(lambda checked, btn=num: self.afterClick(btn))
                self.p_layout.addWidget(button)  
                self.buttons[num] = button
                self.routes.append([num, servel_route])
                
                num = num + 1
                
        else:
        
            self.p_layout.setAlignment(Qt.AlignCenter)
            
            p_text = QLabel()
            p_text.setText("未找到匹配项，请检查输入或尝试其他查询")  
            p_text.setFont(QFont("黑体", 12))
            p_text.setAlignment(Qt.AlignCenter) 
            p_text.setMinimumSize(60, 30)  
            self.p_layout.addWidget(p_text)
                
                
    def afterClick(self, button_number):
        
        for route in self.routes:
            
            if route[0] == button_number:
                global ROUTE
                ROUTE = route[1]
                
        for window in QApplication.topLevelWidgets():
            if window.objectName() == "Route":
                window.deleteLater()
                break
        
        self.routeDia = Route_Dialog.route_dialog()
        self.routeDia.show()
        
        
    def clearLayout(self, layout):
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() 
            if widget:
                widget.deleteLater()  
            else:
                self.clearLayout(item.layout())  