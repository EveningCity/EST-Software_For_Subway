import importlib
import inspect
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QSizePolicy, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import window.Searched_of_Search_Dialog as Searched_of_Search_Dialog, Producer, window.Searched_of_Route_Dialog as Searched_of_Route_Dialog, window.Select_Route as Select_Route
from window import Plan_View_Dialog, Main

ROUTE_NAME = None

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

Data = load("Data",Producer.route.resourcePath("data/Data.py"))

class route_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        self.num = 0
        
        super().__init__()
        self.routeDialog = uic.loadUi(Producer.route.resourcePath("window/ui/route_dialog.ui"), self)
        
        self.p_layout = QVBoxLayout()  
        self.routeDialog.scrollArea.widget().setLayout(self.p_layout) 
        self.p_layout.setAlignment(Qt.AlignTop)
        
        self.routeDialog.pushButton.clicked.connect(self.button)
        
        self.afterClick(Data.ALL_LINE_LIST[0])
        self.routeView(Data.ALL_LINE_LIST[0])
        
        self.routeLayout.setAlignment(Qt.AlignLeft)
        
        if Searched_of_Search_Dialog.ROUTE != None:
            self.afterClick(Searched_of_Search_Dialog.ROUTE)
            self.routeView(Searched_of_Search_Dialog.ROUTE)
            Searched_of_Search_Dialog.ROUTE = None
            
        if Select_Route.ROUTE != None:
            self.afterClick(Select_Route.ROUTE)
            self.routeView(Select_Route.ROUTE)
            Select_Route.ROUTE = None
            
        if Plan_View_Dialog.ROUTE != None:
            self.afterClick(Plan_View_Dialog.ROUTE)
            self.routeView(Plan_View_Dialog.ROUTE)
            Plan_View_Dialog.ROUTE = None
            
        
    def afterClick(self, route):
        
        btn_number = 0
        self.buttons = {}
        self.names = []

        result = self.routeSearch(route).values()
        
        if self.num != 0:
            self.clearLayout(self.p_layout)
            
        self.num = self.num + 1
        
        for station_name in result:
            
            button = QPushButton(f"StationButton{btn_number}")
            button.setText(station_name.replace("_", "/"))  # 设置按钮文本
            button.setFont(QFont("等线", 12))
            button.setMinimumSize(60, 30)  # 设置按钮最小尺寸
            button.setStyleSheet("""
            QPushButton {
                border: 2px solid gray; 
                background-color: white; 
                border-radius: 10px; 
            }
            QPushButton:hover {
                background-color: rgb(209, 209, 209); 
            }
            QPushButton:pressed {
                background-color: rgb(190, 190, 190); 
                border: 2px solid #33373E; 
            }
            """)
            self.p_layout.addWidget(button)  # 将按钮添加到布局中
            
            button.clicked.connect(lambda checked, btn=btn_number: self.afterButtonClick(btn))
            self.buttons[btn_number] = button
            self.names.append([btn_number, station_name])
            
            btn_number = btn_number + 1
                 
        
    def routeView(self, servel_route):
        
        self.clearLayout(self.routeLayout)
            
        route = QLabel("Route")
        route.setText(f"当前查询的线路是 {Producer.ruleText.formatLineList([servel_route])[0]} ")  # 设置文本
        route.setFont(QFont("黑体", 12))
        route.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.routeLayout.addWidget(route) # 添加到布局中         
                 
            
    def afterButtonClick(self, button_number):
        
        for name in self.names:
            
            if name[0] == button_number:
                
                global ROUTE_NAME
                ROUTE_NAME = name[1]
        
        self.searchedDialog = Searched_of_Route_Dialog.searched_route_dialog()
        self.searchedDialog.show()    
        
        
    def button(self):
        
        select = Select_Route.select_route()
        select.show()
        self.close()
    
         
    def clearLayout(self, layout):
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() 
            if widget:
                widget.deleteLater()  
            else:
                self.clearLayout(item.layout())  
                
                
    def routeSearch(self, route):
        
        station_dict = {}
        
        for station in Producer.station:
            
            if route in Producer.route.flatten(station):
                
                for name, value in inspect.getmembers(Data.Station, lambda a: not(inspect.isroutine(a))):
                    
                    if value == station:
                        
                        for element in value[:-1]:
                            
                            if element[0] == route:
                                station_dict[element[1]] = f"{station[-1]} | {Producer.ruleText.betterEnglish(name)}"
        
        station_dict = dict(sorted(station_dict.items()))
        
        return station_dict
    
    
    def closeEvent(self, event):
        self.routeDialog.deleteLater()
        event.accept()