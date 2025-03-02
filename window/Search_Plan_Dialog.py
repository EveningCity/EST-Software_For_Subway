import importlib
import itertools
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QSizePolicy, QFrame, QHBoxLayout, QGroupBox
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, pyqtSignal

import New_Producer
import Producer
import window.Searched_of_Start_Dialog as Searched_of_Start_Dialog, window.Searched_of_End_Dialog as Searched_of_End_Dialog, window.Plan_Dialog as Plan_Dialog, Station_Search


NAME = None

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

Data = load("Data",Producer.route.resourcePath("data/Data.py"))

class search_plan_dialog(QtWidgets.QDialog):
    
    def __init__(self, function=None):
        
        self.num = 0
        self.callback = function
        
        super().__init__()
        self.searchDialog = uic.loadUi(Producer.route.resourcePath("window/ui/search_dialog.ui"), self)
        
        self.searchDialog.pushButton.clicked.connect(self.afterClick)
        
        self.p_layout = QVBoxLayout()  # 创建竖直布局
        self.searchDialog.scrollArea.widget().setLayout(self.p_layout)  
        
        self.setObjectName("Search_Plan_Dialog")
        
        #首先执行的命令
        self.afterClick()
            
        
    def afterClick(self):
        
        query = self.searchDialog.searchText.text()
        result = Station_Search.fuzzy_search(query, [item[0]+"\\"+item[1] for item in Station_Search.station_name])
        res_lst = []
        
        for res,lst in itertools.product([item.split("\\")[0] for item in result], Station_Search.station_name):
            
            if res in lst:
                res_lst.append(lst)
        
        if self.num != 0:
            self.clearLayout(self.p_layout)
            
        self.num = self.num + 1
        
        if isinstance(result, list):
            
            btn_number = 0
            self.names = []
            
            self.p_layout.setAlignment(Qt.AlignTop)
            
            for station in res_lst:
            
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
                
                btn_number = btn_number + 1
                
        else:
            
            self.p_layout.setAlignment(Qt.AlignCenter)
            
            p_text = QLabel()
            p_text.setText("未找到匹配项，请检查输入或尝试其他查询")  
            p_text.setFont(QFont("黑体", 12))
            p_text.setAlignment(Qt.AlignCenter) 
            p_text.setMinimumSize(60, 30)  
            self.p_layout.addWidget(p_text)  
            
            
    def afterButtonClick(self, button_number):
        
        for name in self.names:
            
            if name[0] == button_number:
                global NAME
                NAME = name[1]
        
        if Plan_Dialog.DIRECTION == "Start":
            self.callback(NAME, "Start")
            
        elif Plan_Dialog.DIRECTION == "End":
            self.callback(NAME, "End")
            
            
    def clearLayout(self, layout):
        
        # 遍历布局中的所有子项
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() 
            if widget:
                widget.deleteLater()  
            else:
                self.clearLayout(item.layout())  
                
    
    def closeEvent(self, event):
        self.searchDialog.deleteLater()
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