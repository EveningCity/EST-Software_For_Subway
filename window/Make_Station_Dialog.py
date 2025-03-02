import ast
import copy
import ctypes
import importlib
import inspect
import itertools
import json
import os
import re
import shutil
import sys
from tkinter import colorchooser
import zipfile
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QSizePolicy, QApplication, QMainWindow, QLabel, QVBoxLayout, QFrame, QScrollArea, QWidget, QDialog
from PyQt5.QtGui import QFont, QPainter, QPen, QBrush, QIcon
from PyQt5.QtCore import Qt, QSize

import New_Producer
import Producer
from window import Main, Make_Dialog



def resourcePath(relative_path):
    """获取资源的绝对路径，适用于Dev和PyInstaller"""
    try:
        # PyInstaller 会创建一个临时文件夹并将路径存储在 _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
    
    
def getAim(file_path, aim):
    """获取指定.json文件内的键值"""
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        return(data.get(aim))
        
        
def transFormal(name, mode):
    """将正名改为可读名"""
    if mode == "CN":
        informal_name = name.replace("'","1q1").replace("/","_").replace(" ","1o1").replace("·","1d1").replace("-","1h1")
    elif mode == "EN":
        informal_name = name.replace("'","1q1").replace("/","_").replace(" ","1o1").replace(".","1d1").replace("-","1h1").replace("&","1a1").replace(",","1c1")
    return informal_name


def clearLayout(layout):
    """清空布局"""
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget() 
        if widget:
            widget.deleteLater()  
        else:
            clearLayout(item.layout()) 
            
            
passCode_QLineEdit = """
QLineEdit {
    border: 2px solid black;      
    border-radius: 10px;            
    padding-left: 10px;             
    padding-right: 10px;                          
    background-color: #FFFFFF;   
    color: black;  
}
"""
        
errorCode_QLineEdit = """
QLineEdit {
    border: 2px solid red;      
    border-radius: 10px;            
    padding-left: 10px;             
    padding-right: 10px;                            
    background-color: #FFFFFF; 
    color: blacks;      
}
"""

ignoreCode_QLineEdit = """
QLineEdit {
    border: 2px solid gray;      
    border-radius: 10px;            
    padding-left: 10px;             
    padding-right: 10px;                            
    background-color: #FFFFFF;    
}
"""

passCode_QGroupBox = """
QGroupBox {
    border: 2px solid black;      
    border-radius: 10px;            
    padding-left: 10px;             
    padding-right: 10px;            
    color: #000000;                 
    background-color: #FFFFFF;      
}
"""
        
errorCode_QGroupBox = """
QGroupBox {
    border: 2px solid red;      
    border-radius: 10px;            
    padding-left: 10px;             
    padding-right: 10px;            
    color: #000000;                 
    background-color: #FFFFFF;      
}
"""

passCode_QPushButton = """
QPushButton {
	border-radius: 10px;
	border: 2px solid #33373E;
    background-color: #FFFFFF;
    color: black;      
}
QPushButton:hover {
    background-color: rgb(209, 209, 209);
}
QPushButton:pressed {
    background-color: rgb(190, 190, 190); 
}
"""

errorCode_QPushButton = """
QPushButton {
	border-radius: 10px;
	border: 2px solid red;
    background-color: #FFFFFF;   
    color: red;       
}
QPushButton:hover {
    background-color: rgb(209, 209, 209);
}
QPushButton:pressed {
    background-color: rgb(190, 190, 190); 
}
"""



class make_dialog(QtWidgets.QDialog):
    
    def __init__(self, Station_Name, Now_Route):
        
        # uic
        super().__init__()
        self.makeDialog = uic.loadUi(resourcePath("window/ui/make_station_dialog.ui"), self)
        
        # QPushButton
        self.makeDialog.checkCN.clicked.connect(self.check_CN)
        self.makeDialog.checkEN.clicked.connect(self.check_EN)
        self.makeDialog.plus.clicked.connect(self.plus1n1)
        self.makeDialog.cut.clicked.connect(self.cut1n1)
        
        # QCheckBox
        self.makeDialog.YesNoSubCN.toggled.connect(self.yes_or_No_CN)
        self.makeDialog.YesNoSubEN.toggled.connect(self.yes_or_No_EN)
        
        # QLineEdit
        self.makeDialog.MainCN.textChanged.connect(lambda: self.line_edit_change_color("MainCN"))
        self.makeDialog.SubCN.textChanged.connect(lambda: self.line_edit_change_color("SubCN"))
        self.makeDialog.MainEN.textChanged.connect(lambda: self.line_edit_change_color("MainEN"))
        self.makeDialog.SubEN.textChanged.connect(lambda: self.line_edit_change_color("SubEN"))
        
        # 传递的车站信息
        self.station_name = Station_Name
        self.now_route = Now_Route
        
        self.begin()
        
        
    def begin(self):
        
        routes = []
        self.makeDialog.stationID.setText(f"唯一识别码：{self.station_name}")
        clearLayout(self.makeDialog.routePlacerLayout)
        
        lines = getAim(resourcePath("mader/folder/data.json"), "lines")
        color = getAim(resourcePath("mader/folder/data.json"), "color")
        
        for station_general in lines.items():
            
            for station in station_general[1].items():
                
                if station[0] == self.station_name:
                
                    name = [station[0], station[1][1]]
                    line = station_general[0].replace("Line_","")
                    routes.append([line, color[line]])
                    
        if "1tc1" in name[1]:
            main_name_CN = New_Producer.betterChinese(name[1].split("1tc1")[0])
            sub_name_CN = New_Producer.betterChinese(name[1].split("1tc1")[1])
            self.makeDialog.MainCN.setText(main_name_CN)
            self.makeDialog.SubCN.setText(sub_name_CN)
            
            self.makeDialog.nameCN.setText(main_name_CN)
            self.makeDialog.subNameCN.setText(sub_name_CN)
            
            self.makeDialog.YesNoSubCN.setChecked(True)
        else:
            main_name_CN = New_Producer.betterChinese(name[1])
            self.makeDialog.MainCN.setText(main_name_CN)
            self.makeDialog.SubCN.setText("")
            
            self.makeDialog.nameCN.setText(main_name_CN)
            self.makeDialog.subNameCN.setText("")
            
            self.makeDialog.YesNoSubCN.setChecked(False)
            
        if "1te1" in name[0]:
            main_name_EN = New_Producer.betterEnglish(name[0].split("1te1")[0])
            sub_name_EN = New_Producer.betterEnglish(name[0].split("1te1")[1])
            self.makeDialog.MainEN.setText(main_name_EN)
            self.makeDialog.SubEN.setText(sub_name_EN)
            
            self.makeDialog.nameEN.setText(main_name_EN)
            self.makeDialog.subNameEN.setText(f"({sub_name_EN})")
            
            self.makeDialog.YesNoSubEN.setChecked(True)
        else:
            main_name_EN = New_Producer.betterEnglish(name[0])
            self.makeDialog.MainEN.setText(main_name_EN)
            self.makeDialog.SubEN.setText("")
            
            self.makeDialog.nameEN.setText(main_name_EN)
            self.makeDialog.subNameEN.setText("")
            
            self.makeDialog.YesNoSubEN.setChecked(False)
            
        for route in routes:
                
            label = QLabel()
            label.setText(route[0])
            label.setFont(QFont("黑体", 12))
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            if len(route[0]) < 5:
                label.setFixedWidth(60)
            else:
                label.setFixedWidth(80)
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            label.setStyleSheet("""
            QLabel {{
                color: rgb(255,255,255);
                border: 2px solid {}; 
                background-color: {}; 
                border-radius: 10px; 
            }}
            """.format(route[1], New_Producer.darkerColor(route[1])))
            self.makeDialog.routePlacerLayout.addWidget(label)
            
        empty_element_amount = str(self.station_name.count("1n1"))
        self.makeDialog.EmptyElement.setText(f" {empty_element_amount} ")
        
        
    def line_edit_change_color(self, mode):
        
        if mode == "MainCN":
            name = self.makeDialog.MainCN.text()
            pattern = r'^[\u4e00-\u9fffa-zA-Z0-9·/ \-\']{1,10}$'
            if bool(re.match(pattern, name)) == True:
                self.makeDialog.MainCN.setStyleSheet(passCode_QLineEdit)
                self.makeDialog.MainCN.setFont(QFont("黑体", 12))
                self.makeDialog.checkCN.setEnabled(True)
            else:
                self.makeDialog.MainCN.setStyleSheet(errorCode_QLineEdit)
                self.makeDialog.MainCN.setFont(QFont("黑体", 12))
                self.makeDialog.checkCN.setEnabled(False)
                
        elif mode == "SubCN":
            name = self.makeDialog.SubCN.text()
            pattern = r'^[\u4e00-\u9fffa-zA-Z0-9·/ \-\']{0,10}$'
            if bool(re.match(pattern, name)) == True:
                self.makeDialog.SubCN.setStyleSheet(passCode_QLineEdit)
                self.makeDialog.SubCN.setFont(QFont("黑体", 12))
                self.makeDialog.checkCN.setEnabled(True)
            else:
                self.makeDialog.SubCN.setStyleSheet(errorCode_QLineEdit)
                self.makeDialog.SubCN.setFont(QFont("黑体", 12))
                self.makeDialog.checkCN.setEnabled(False)
                
        elif mode == "MainEN":
            name = self.makeDialog.MainEN.text()
            pattern = r'^[a-zA-Z0-9.,/& \-\']{1,30}$'
            if bool(re.match(pattern, name)) == True:
                self.makeDialog.groupBoxEN.setStyleSheet(passCode_QGroupBox)
                self.makeDialog.checkEN.setEnabled(True)
            else:
                self.makeDialog.groupBoxEN.setStyleSheet(errorCode_QGroupBox)
                self.makeDialog.checkEN.setEnabled(False)
                
        elif mode == "SubEN":
            name = self.makeDialog.SubEN.text()
            pattern = r'^[a-zA-Z0-9.,/& \-\']{0,30}$'
            if bool(re.match(pattern, name)) == True:
                self.makeDialog.SubEN.setStyleSheet(passCode_QLineEdit)
                self.makeDialog.SubEN.setFont(QFont("黑体", 12))
                self.makeDialog.checkEN.setEnabled(True)
            else:
                self.makeDialog.SubEN.setStyleSheet(errorCode_QLineEdit)
                self.makeDialog.SubEN.setFont(QFont("黑体", 12))
                self.makeDialog.checkEN.setEnabled(False)
        
        
    def check_CN(self):
        
        lines = getAim(resourcePath("mader/folder/data.json"), "lines")
        
        main_name = self.makeDialog.MainCN.text()
        sub_name = self.makeDialog.SubCN.text()
        
        if sub_name != "":
            name = f"{main_name}1tc1{sub_name}"
        else:
            name = main_name
            
        for line in lines.items():
            for station in line[1].items():
                if station[1][1] == transFormal(name, "CN"):
                    if station[0] != self.station_name:
                        self.makeDialog.checkCN.setStyleSheet(errorCode_QPushButton)
                        ERROR = error("请先修改唯一识别码直至其与需要同名化的站点一致")
                        ERROR.exec_()
                        return
            
        if "1tc1" in name:
            self.makeDialog.checkCN.setStyleSheet(errorCode_QPushButton)
            ERROR = error("含有无效语段")
            ERROR.exec_()
            return
            
        pattern = r'^[\u4e00-\u9fffa-zA-Z0-9·/ \-\']{1,10}$'
        
        if bool(re.match(pattern, name.replace("1tc1",""))) == True:
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
                
            if 'lines' in data:
                for line in data["lines"].items():
                    for station in line[1].items():
                        if station[0] == self.station_name:
                            data["lines"][line[0]][station[0]][1] = transFormal(name, "CN")
                            
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
            
            self.begin()
            self.makeDialog.checkCN.setStyleSheet(passCode_QPushButton)
        else:
            self.makeDialog.checkCN.setStyleSheet(errorCode_QPushButton)
            ERROR = error("输入无效")
            ERROR.exec_()
            
            
    def check_EN(self):
        
        main_name = self.makeDialog.MainEN.text()
        sub_name = self.makeDialog.SubEN.text()
        
        if sub_name != "":
            name = f"{main_name}1te1{sub_name}"
        else:
            name = main_name
            
        name += "1n1" * self.station_name.count("1n1")
            
        if "1te1" in name:
            self.makeDialog.checkEN.setStyleSheet(errorCode_QPushButton)
            ERROR = error("含有无效语段")
            ERROR.exec_()
            return
            
        pattern = r'^[a-zA-Z0-9.,/& \-\']{1,30}$'
        
        if name == New_Producer.betterEnglish(self.station_name):
            self.makeDialog.checkEN.setStyleSheet(errorCode_QPushButton)
            ERROR = error("输入重复")
            ERROR.exec_()
            return
        
        if bool(re.match(pattern, name.replace("1te1",""))) == True:
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
                result = copy.deepcopy(data)
                
            if 'lines' in data:
                for line in data["lines"].items():
                    for station in line[1].items():
                        if station[0] == self.station_name:
                            result["lines"][line[0]][transFormal(name, "EN")] = data["lines"][line[0]][station[0]]
                            del result["lines"][line[0]][station[0]]
                            
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(result, file, indent=4)  # 使用 indent 参数美化输出格式
            
            self.station_name = transFormal(name, "EN")
            self.begin()
            self.makeDialog.checkEN.setStyleSheet(passCode_QPushButton)
        else:
            self.makeDialog.checkEN.setStyleSheet(errorCode_QPushButton)
            ERROR = error("输入无效")
            ERROR.exec_()

    
    def yes_or_No_CN(self, checked):
        
        if checked:
            self.makeDialog.SubCN.setReadOnly(False)
            self.makeDialog.SubCN.setStyleSheet(passCode_QLineEdit)
            self.makeDialog.SubCN.setFont(QFont("黑体", 12))
        else:
            self.makeDialog.SubCN.setText("")
            self.makeDialog.SubCN.setReadOnly(True)
            self.makeDialog.SubCN.setStyleSheet(ignoreCode_QLineEdit)
            self.makeDialog.SubCN.setFont(QFont("黑体", 12))
            
            
    def yes_or_No_EN(self, checked):
        
        if checked:
            self.makeDialog.SubEN.setReadOnly(False)
            self.makeDialog.SubEN.setStyleSheet(passCode_QLineEdit)
            self.makeDialog.SubEN.setFont(QFont("黑体", 12))
        else:
            self.makeDialog.SubEN.setText("")
            self.makeDialog.SubEN.setReadOnly(True)
            self.makeDialog.SubEN.setStyleSheet(ignoreCode_QLineEdit)
            self.makeDialog.SubEN.setFont(QFont("黑体", 12))
            
    
    def plus1n1(self):
        
        name = self.station_name + "1n1"
        
        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
            result = copy.deepcopy(data)
            
        if 'lines' in data:
            for line in data["lines"].items():
                for station in line[1].items():
                    if station[0] == self.station_name:
                        result["lines"][line[0]][name] = data["lines"][line[0]][station[0]]
                        del result["lines"][line[0]][station[0]]
                        
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4)  # 使用 indent 参数美化输出格式
            
        self.station_name += "1n1"
        
        self.begin()
        
        
    def cut1n1(self):
        
        if self.station_name.count("1n1") == 0:
            ctypes.windll.user32.MessageBeep(0x00000010)
            return
        
        informal = copy.deepcopy(self.station_name)
        
        name = informal.replace("1n1", "", 1)
        
        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
            result = copy.deepcopy(data)
            
        if 'lines' in data:
            for line in data["lines"].items():
                for station in line[1].items():
                    if station[0] == self.station_name:
                        result["lines"][line[0]][name] = data["lines"][line[0]][station[0]]
                        del result["lines"][line[0]][station[0]]
                        
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4)  # 使用 indent 参数美化输出格式
            
        self.station_name = name
        
        self.begin()

        
            
class error(QtWidgets.QDialog):
    
    def __init__(self, TEXT):

        super().__init__()
        self.errorDialog = uic.loadUi(Producer.route.resourcePath("window/ui/error.ui"), self)
        
        ctypes.windll.user32.MessageBeep(0x00000010)
        self.errorDialog.error.setText(TEXT)