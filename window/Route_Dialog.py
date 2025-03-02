import importlib
import inspect
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QSizePolicy, QApplication, QHBoxLayout, QGroupBox, QFrame, QSizePolicy, QSpacerItem, QMainWindow
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt

import New_Producer
import Station_Search
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
        
        self.routeDialog.routeLayout.setAlignment(Qt.AlignLeft)
        
        if Searched_of_Search_Dialog.ROUTE != None:
            self.afterClick(Searched_of_Search_Dialog.ROUTE)
            self.routeView(Searched_of_Search_Dialog.ROUTE)
            Searched_of_Search_Dialog.ROUTE = None
            
        elif Select_Route.ROUTE != None:
            self.afterClick(Select_Route.ROUTE)
            self.routeView(Select_Route.ROUTE)
            Select_Route.ROUTE = None
            
        elif Plan_View_Dialog.ROUTE != None:
            self.afterClick(Plan_View_Dialog.ROUTE)
            self.routeView(Plan_View_Dialog.ROUTE)
            Plan_View_Dialog.ROUTE = None
            
        else:
            self.routeView(Data.ALL_LINE_LIST[0])
            self.afterClick(Data.ALL_LINE_LIST[0])
            
        self.setObjectName("Route")
        for window in QApplication.topLevelWidgets():
            if window.objectName() not in ["Main", "Route"]:
                window.deleteLater()
            
        
    def afterClick(self, route):
        
        btn_number = 0
        self.names = []
        
        if self.num != 0:
            self.clearLayout(self.p_layout)
            
        self.num += 1
        
        for station in self.routeSearch(route).values():
            
            name_CN = New_Producer.betterChinese(station[0])
            name_EN = New_Producer.betterEnglish(station[1])
                
            if len(station) == 2:
                button = RichTextButton("""
                <span style="font-size:16px; color:black;">{}</span><br>
                <span style="font-size:12px; color:black;">{}</span><br>
                <span></span>
                """.format(name_CN,name_EN), station[0])
                
            else:
                if station[2] == None:
                    sub_name_EN = New_Producer.betterEnglish(station[3])
                    
                    button = RichTextButton("""
                    <span style="font-size:16px; color:black;">{}</span><br>
                    <span style="font-size:16px; color:black;">{}</span>
                    <span style="font-size:12px; color:gray;"> ({})</span><br>
                    <span></span>
                    """.format(name_CN,name_EN,sub_name_EN), station[0])
                    
                elif station[3] == None:
                    sub_name_CN = New_Producer.betterChinese(station[2])
                    
                    button = RichTextButton("""
                    <span style="font-size:16px; color:black;">{}</span>
                    <span style="font-size:16px; color:gray;"> {}</span><br>
                    <span style="font-size:12px; color:black;">{}</span><br>
                    <span></span>
                    """.format(name_CN,sub_name_CN,name_EN), station[0])
                else:
                    sub_name_CN = New_Producer.betterChinese(station[2])
                    sub_name_EN = New_Producer.betterEnglish(station[3])
                    
                    button = RichTextButton("""
                    <span style="font-size:16px; color:black;">{}</span>
                    <span style="font-size:16px; color:gray;"> {}</span><br>
                    <span style="font-size:12px; color:black;">{}</span>
                    <span style="font-size:12px; color:gray;"> ({})</span><br>
                    <span></span>
                    """.format(name_CN,sub_name_CN,name_EN,sub_name_EN), station[0])
                
            button.setFlat(True)
            button.setStyleSheet("""
            QPushButton {
                border-radius: 10px;
                border: 2px solid #33373E;
                background-color: #FFFFFF;      
            }
            QPushButton:hover {
                background-color: rgb(209, 209, 209);
            }
            QPushButton:pressed {
                background-color: rgb(190, 190, 190); 
            }
            """)
            self.p_layout.addWidget(button)
            
            button.clicked.connect(lambda checked, btn=btn_number: self.afterButtonClick(btn))
            self.names.append([btn_number, station])
            
            btn_number += 1
                 
        
    def routeView(self, servel_route):
        
        self.clearLayout(self.routeDialog.routeLayout)
            
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
        self.routeDialog.routeLayout.addWidget(route)        
                 
            
    def afterButtonClick(self, button_number):
        
        for name in self.names:
            
            if name[0] == button_number:
                
                global ROUTE_NAME
                ROUTE_NAME = name[1]
        
        self.searchedDialog = Searched_of_Route_Dialog.searched_route_dialog()
        self.searchedDialog.show()    
        
        
    def button(self):
        
        for window in QApplication.topLevelWidgets():
            if window.objectName() == "Select":
                window.deleteLater()
                break
            
        select = Select_Route.select_route()
        select.show()
    
         
    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
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
                                for st in Station_Search.station_name:
                                    if station[-1] == st[0]:
                                        station_dict[max(element[1:])] = st
        
        station_dict = dict(sorted(station_dict.items()))
        
        return station_dict
        
    
    def closeEvent(self, event):
        self.routeDialog.deleteLater()
        event.accept()
        
        
        
class RichTextButton(QPushButton):
    def __init__(self, text, name, parent=None):
        super().__init__(parent)
        
        self.qlayout_1 = QVBoxLayout()
        self.qlayout_2 = QVBoxLayout()
        
        self.numberSet(name)
        
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setStyleSheet("""
        QLabel {
            font-family: 微软雅黑;
            background-color: transparent;
            border: 0px solid transparent;
            padding: 6px;
        }
        """)
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.layout = QHBoxLayout(self)
        self.layout.insertWidget(0, self.label)
        self.layout.insertLayout(1, self.qlayout_2)
        self.layout.insertLayout(2, self.qlayout_1)
        
        self.layout.setAlignment(self.label, Qt.AlignLeft | Qt.AlignVCenter)
        
        self.layout.setStretch(0, 518)
        self.layout.setStretch(1, 100)
        self.layout.setStretch(2, 100)
        self.setLayout(self.layout)

        self.initUI()

    def initUI(self):
        # 设置按钮的样式
        self.setStyleSheet("""
        QPushButton {
            border-radius: 10px;
            border: 2px solid #33373E;
            background-color: #FFFFFF;      
        }
        QPushButton:hover {
            background-color: rgb(209, 209, 209);
        }
        QPushButton:pressed {
            background-color: rgb(190, 190, 190); 
        }
        """)
        self.label.resize(self.size())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.label.resize(self.size())

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.transparent, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.NoBrush))
        painter.drawRect(self.rect().adjusted(1, 1, -1, -1))
        
        
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
            groupBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            groupBox.setFixedWidth(90)
            
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
            
            route = QLabel()
            route.setText(Line)
            route.setFont(QFont("微软雅黑", 10, QFont.Bold))
            route.setAlignment(Qt.AlignCenter)
            route.setStyleSheet("color: {};".format(Producer.ruleText.colorRoute(line_and_number[0])))
            route.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            
            groupBoxLayout.insertWidget(0, route)
            groupBoxLayout.insertWidget(1, vertical_line)
            groupBoxLayout.insertWidget(2, number)
            
            if num % 2 == 0:
                self.qlayout_1.addWidget(groupBox)
                
            else:
                self.qlayout_2.addWidget(groupBox)
                
            num = num + 1
            
            if self.qlayout_1.count() > 2:
                self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.setFixedHeight(36 + self.qlayout_1.count()*30)
            else:
                self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.setFixedHeight(66)