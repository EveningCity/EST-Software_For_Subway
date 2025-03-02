import ast
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
from window import Main, Make_Dialog, Make_Station_Dialog


ROUTE = None
NAME = None

def resourcePath(relative_path):
        """获取资源的绝对路径，适用于Dev和PyInstaller"""
        
        try:
            # PyInstaller 会创建一个临时文件夹并将路径存储在 _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

class make_dialog(QtWidgets.QDialog):
    
    def __init__(self, searchOldWindow, route):
        
        global NAME, ROUTE
        
        self.num = 0
        self.time = 0
        NAME = Make_Dialog.NAME
        ROUTE = route
        
        super().__init__()
        self.makeDialog = uic.loadUi(resourcePath("window/ui/make_stations_dialog.ui"), self)
        self.makeDialog.changeColor.clicked.connect(self.change_color)
        self.makeDialog.checkName.clicked.connect(self.change_name)
        self.makeDialog.checkCode.clicked.connect(self.change_ID)
        self.makeDialog.testBranch.clicked.connect(self.test_branch)
        self.makeDialog.haveBranch.toggled.connect(self.branch_on_toggled)
        self.makeDialog.oneDirection.toggled.connect(self.direction_on_toggled)
        self.makeDialog.numHidden.toggled.connect(self.num_on_toggled)
        self.makeDialog.loop.toggled.connect(self.loop_on_toggled)
        
        self.get_title()
        self.third_test()
        self.add_stations()
        
        self.searchOldWindow = searchOldWindow
        self.setObjectName("Make_Stations")
        
        self.time += 1
        self.all_CN_list = Producer.route.last(Producer.route.flatten([[x[1][1] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
        self.all_EN_list = Producer.route.last(Producer.route.flatten([[x[0] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
        
        
    def change_color(self):
        
        global ROUTE
        
        color = colorchooser.askcolor()  # 返回一个元组
        if color:  # 如果用户取消选择，则返回 None
            rgb, hex_color = color  # 解包元组
            RGB = f"rgb{rgb}"
        
        if rgb != None:
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
            
            if 'color' in data:
                data['color'][ROUTE] = RGB
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
            
            self.get_title()
            self.add_stations()
         
            
    def get_title(self):
        
        global ROUTE
        
        color = self.getAim(resourcePath("mader/folder/data.json"), "color")[ROUTE]
        routes_CN = self.getAim(resourcePath("mader/folder/data.json"), "routes_CN")
        branch_lines = self.getAim(resourcePath("mader/folder/data.json"), "branch_lines")
        
        branch_list = []
        for branch_line in branch_lines:
            if "False" in branch_line:
                continue
            if ROUTE == branch_line[0]:
                branch_list.append(f"当前线路是{New_Producer.formatLine(branch_line[1], routes_CN)}的主线")
            elif ROUTE == branch_line[1]:
                branch_list.append(f"当前线路是{New_Producer.formatLine(branch_line[0], routes_CN)}的支线")
        if branch_list == []:
            branch_list = ["当前线路是独立线路"]
        branch = "，".join(branch_list)
        
        color_hex = []
        color_list = [hex(int(item))[2:].upper() for item in color.replace("rgb(", "").replace(")", "").split(",")]
        for servel_color in color_list:
            if len(servel_color) == 1:
                color_hex.append(f"0{servel_color}")
            else:
                color_hex.append(servel_color)
        color_hex = f'#{"".join(color_hex)}'
        
        self.makeDialog.colorID.setStyleSheet("""
QLabel {{
	color: rgb(255,255,255);
	border: 2px solid {}; 
	background-color: {}; 
	border-radius: 10px; 
}}                                         
        """.format(color, color))
        self.makeDialog.colorID.setText(color_hex)
        self.makeDialog.name.setText(New_Producer.formatLine(ROUTE, routes_CN))
        self.makeDialog.routeID.setText(f"唯一识别码：{ROUTE}")
        self.makeDialog.branchCondition.setText(branch)
        
        
    def change_name(self):
        
        global ROUTE
        
        passCode = """
        QLineEdit {
        border: 2px solid black;      
        border-radius: 10px;            
        padding-left: 10px;             
        padding-right: 10px;            
        color: #000000;                 
        background-color: #FFFFFF;      
        }
        """
        
        errorCode = """
        QLineEdit {
        border: 2px solid red;      
        border-radius: 10px;            
        padding-left: 10px;             
        padding-right: 10px;            
        color: #000000;                 
        background-color: #FFFFFF;      
        }
        """
        
        routes_CN = self.getAim(resourcePath("mader/folder/data.json"), "routes_CN")
        
        name = self.makeDialog.changeName.text()
        
        if name in routes_CN.keys() or "\\" in name or name == "":
            self.makeDialog.changeName.setStyleSheet(errorCode)
            self.makeDialog.changeName.setFont(QFont("黑体", 12))
            error().show()
        else:
            self.makeDialog.changeName.setStyleSheet(passCode)
            self.makeDialog.changeName.setFont(QFont("黑体", 12))
            
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
            
            if 'routes_CN' in data:
                data['routes_CN'] = {servel[0]: servel[1] for servel in data['routes_CN'].items() if servel[1] != ROUTE}
                data['routes_CN'][name] = ROUTE
                data['routes_CN'] = self.sortDict(data['routes_CN'], "value")
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
            
            self.get_title()
            self.add_stations()
            
    def change_ID(self):
        
        global ROUTE
        
        passCode = """
        QLineEdit {
        border: 2px solid black;      
        border-radius: 10px;            
        padding-left: 10px;             
        padding-right: 10px;            
        color: #000000;                 
        background-color: #FFFFFF;      
        }
        """
        
        errorCode = """
        QLineEdit {
        border: 2px solid red;      
        border-radius: 10px;            
        padding-left: 10px;             
        padding-right: 10px;            
        color: #000000;                 
        background-color: #FFFFFF;      
        }
        """
        
        routes_EN = self.getAim(resourcePath("mader/folder/data.json"), "routes_EN")
        routes_CN = self.getAim(resourcePath("mader/folder/data.json"), "routes_CN")
        
        name = self.makeDialog.changeCode.text()
        
        pattern = r'^[a-zA-Z0-9]+$'
        if re.match(pattern, name) and name not in routes_EN:
            self.makeDialog.changeCode.setStyleSheet(passCode)
            self.makeDialog.changeCode.setFont(QFont("黑体", 12))
            
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
            
            if 'routes_EN' in data:
                data['routes_EN'] = sorted([(name if item == ROUTE else item) for item in data['routes_EN']])
            
            if 'routes_CN' in data:
                data['routes_CN'] = {servel[0]: servel[1] for servel in data['routes_CN'].items() if servel[1] != ROUTE}
                data['routes_CN'][New_Producer.formatLine(ROUTE, routes_CN)] = name
                data['routes_CN'] = self.sortDict(data['routes_CN'], "value")
                
            if 'above' in data:
                data['above'] = self.sortDict({(name if item[0] == ROUTE else item[0]):item[1] for item in data['above'].items()}, "key")
                
            if 'below' in data:
                data['below'] = self.sortDict({(name if item[0] == ROUTE else item[0]):item[1] for item in data['below'].items()}, "key")
                
            if 'color' in data:
                data['color'] = self.sortDict({(name if item[0] == ROUTE else item[0]):item[1] for item in data['color'].items()}, "key")
                
            if 'time' in data:
                data['time'] = self.sortDict({(name if item[0] == ROUTE else item[0]):item[1] for item in data['time'].items()}, "key")
            
            if 'branch_lines' in data:
                pos_list = []
                for servel in data['branch_lines']:
                    if ROUTE in servel:
                        pos_list.append(data['branch_lines'].index(servel))
                        
                pos_list = list(set(pos_list))
                
                for pos in pos_list:
                    data['branch_lines'].append([name if item == ROUTE else item for item in data['branch_lines'][pos]])
                    del data['branch_lines'][pos]
                    data['branch_lines'].sort()
                    
                pos_list = []
                
            if 'direct_lines' in data:
                direct_pos_list = []
                for servel in data['direct_lines']:
                    if ROUTE in servel:
                        direct_pos_list.append(data['direct_lines'].index(servel))
                
                for direct_pos in direct_pos_list:
                    data['direct_lines'].append([name if item == ROUTE and data['direct_lines'][direct_pos].index(item) == 0 else item for item in data['direct_lines'][direct_pos]])
                    del data['direct_lines'][direct_pos]
                    data['direct_lines'].sort()
                    
                direct_pos_list = []
                
            if 'lines' in data:
                data['lines'][f'Line_{name}'] = data['lines'][f'Line_{ROUTE}']
                del data['lines'][f'Line_{ROUTE}']
                data['lines'] = self.sortDict(data['lines'], "key")
                
            ROUTE = name
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
            
            self.get_title()
            self.add_stations()
        
        else:
            self.makeDialog.changeCode.setStyleSheet(errorCode)
            self.makeDialog.changeCode.setFont(QFont("黑体", 12))
            error().show()
        
    
    def third_test(self):
        
        global ROUTE
        
        branch_lines = self.getAim(resourcePath("mader/folder/data.json"), "branch_lines")
        direct_lines = self.getAim(resourcePath("mader/folder/data.json"), "direct_lines")
        lines = self.getAim(resourcePath("mader/folder/data.json"), "lines")
        
        if ROUTE not in [item[0] for item in direct_lines]:
            if len(list(lines[f"Line_{ROUTE}"].values())[0][0]) == 2:
                self.makeDialog.loop.setChecked(True)
        
        for every_branch in branch_lines:
            if ROUTE == every_branch[0]:
                self.makeDialog.haveBranch.setChecked(True)
                
        for every_direct in direct_lines:
            if ROUTE == every_direct[0]:
                self.makeDialog.oneDirection.setChecked(True)
                
        for every_branch in branch_lines:
            if ["False", ROUTE] == every_branch:
                self.makeDialog.numHidden.setChecked(True)
                
                
    def branch_on_toggled(self, checked):
        
        global ROUTE
        
        if checked:
            self.makeDialog.testBranch.setDisabled(False)
            self.makeDialog.keyInBranch.setReadOnly(False)
            
            branch_lines = self.getAim(resourcePath("mader/folder/data.json"), "branch_lines")
        
            branch_list = []
            for branch_line in branch_lines:
                if ROUTE == branch_line[0]:
                    branch_list.append(branch_line[1])
                    
            branch = "-".join(branch_list)
            self.makeDialog.keyInBranch.setText(branch)
            
            self.get_title()
            self.add_stations()
        else:
            self.makeDialog.testBranch.setDisabled(True)
            self.makeDialog.keyInBranch.setReadOnly(True)
            self.makeDialog.keyInBranch.setText("")
            
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
                
            if 'branch_lines' in data:
                pos_list = []
                for servel in data['branch_lines']:
                    if ROUTE == servel[0]:
                        pos_list.append(data['branch_lines'].index(servel))
                        
                pos_list = list(set(pos_list))
                
                for pos in pos_list:
                    del data['branch_lines'][pos]
                    
                data['branch_lines'].sort()
                    
                pos_list = []
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
                
            self.get_title()
            self.add_stations()
            
            
    def test_branch(self):
        
        global ROUTE
        
        passCode = """
        QLineEdit {
        border: 2px solid black;      
        border-radius: 10px;            
        padding-left: 10px;             
        padding-right: 10px;            
        color: #000000;                 
        background-color: #FFFFFF;      
        }
        """
        
        errorCode = """
        QLineEdit {
        border: 2px solid red;      
        border-radius: 10px;            
        padding-left: 10px;             
        padding-right: 10px;            
        color: #000000;                 
        background-color: #FFFFFF;      
        }
        """
        
        routes_EN = self.getAim(resourcePath("mader/folder/data.json"), "routes_EN")
        
        if "\\" in self.makeDialog.keyInBranch.text():
            error().show()
            self.makeDialog.keyInBranch.setStyleSheet(errorCode)
            self.makeDialog.keyInBranch.setFont(QFont("黑体", 12))
            return
        
        branch_line_list = self.makeDialog.keyInBranch.text().split("-")
        
        for servel_branch_line in branch_line_list:
            if servel_branch_line not in routes_EN:
                error().show()
                self.makeDialog.keyInBranch.setStyleSheet(errorCode)
                self.makeDialog.keyInBranch.setFont(QFont("黑体", 12))
                return
            else:
                self.makeDialog.keyInBranch.setStyleSheet(passCode)
                self.makeDialog.keyInBranch.setFont(QFont("黑体", 12))

                
        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
            
        if 'branch_lines' in data:
            pos_list = []
            for servel in data['branch_lines']:
                if ROUTE == servel[0]:
                    pos_list.append(data['branch_lines'].index(servel))
                    
            pos_list = list(set(pos_list))
            
            for pos in pos_list:
                del data['branch_lines'][pos]
            
            for servel_branch_line in branch_line_list:
                data['branch_lines'].append([ROUTE, servel_branch_line])
            data['branch_lines'].sort()
                
            pos_list = []
            
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
                    
        self.get_title()
        self.add_stations()
                
    
    def direction_on_toggled(self, checked):
        
        global ROUTE
        
        above = self.getAim(resourcePath("mader/folder/data.json"), "above")
        
        if checked:
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
                
            if 'direct_lines' in data:
                
                if len(data['direct_lines']) == 0:
                    data['direct_lines'] = [["None","开往 None 方向"]]
                
                direct_list = []
                for servel_item in data['direct_lines']:
                    if servel_item[0] != ROUTE:
                        direct_list.append(servel_item)
                
                direct_list.append([ROUTE, above[ROUTE]])
                
                data['direct_lines'] = direct_list
                    
            if 'lines' in data and self.time != 0:
                data['lines'][f'Line_{ROUTE}'] = {item[0]: [[item[1][0][0], 0]] + item[1][1:] for item in data['lines'][f'Line_{ROUTE}'].items()}
                max_num = max(Producer.route.flatten([item[0] for item in data['lines'][f'Line_{ROUTE}'].values()]))
                        
                for item in data['lines'][f'Line_{ROUTE}'].items():
                    if 1 in item[1][0]:
                        data['lines'][f'Line_{ROUTE}'][item[0]] = [[1, max_num + 1]] + item[1][1:]
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
                
            self.add_stations()
                
            return True
                
        else:
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
                
            if 'direct_lines' in data:
                
                if len(data['direct_lines']) == 0:
                    data['direct_lines'] = [["None","开往 None 方向"]]
                
                direct_list = []
                for servel_item in data['direct_lines']:
                    if servel_item[0] != ROUTE:
                        direct_list.append(servel_item)
                
                data['direct_lines'] = direct_list
                    
            if 'lines' in data:
                data['lines'][f'Line_{ROUTE}'] = {item[0]: [ [min([num for num in item[1][0] if num != 0])] ] + item[1][1:] for item in data['lines'][f'Line_{ROUTE}'].items()}
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
                
            self.add_stations()
            
            
    def num_on_toggled(self, checked):
        
        global ROUTE
        
        if checked:
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
                
            if 'branch_lines' in data:
                bra_list = []
                for servel_item in data['branch_lines']:
                    if servel_item != ["False", ROUTE]:
                        bra_list.append(servel_item)
                
                bra_list.append(["False", ROUTE])
                
                data['branch_lines'] = bra_list
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
                
            return True
                
        else:
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
                
            if 'branch_lines' in data:
                bra_list = []
                for servel_item in data['branch_lines']:
                    if servel_item != ["False", ROUTE]:
                        bra_list.append(servel_item)
                
                data['branch_lines'] = bra_list
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
                
                
    def loop_on_toggled(self, checked):
        
        global ROUTE
        
        if checked:
            self.makeDialog.haveBranch.setCheckable(False)
            self.makeDialog.haveBranch.setStyleSheet('color: gray;')
            self.makeDialog.haveBranch.setFont(QFont("黑体", 12))
            
            self.makeDialog.oneDirection.setCheckable(False)
            self.makeDialog.oneDirection.setStyleSheet('color: gray;')
            self.makeDialog.oneDirection.setFont(QFont("黑体", 12))
            
            self.makeDialog.numHidden.setCheckable(False)
            self.makeDialog.numHidden.setStyleSheet('color: gray;')
            self.makeDialog.numHidden.setFont(QFont("黑体", 12))
            
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
            
            if 'branch_lines' in data:
                pos_list = []
                for servel in data['branch_lines']:
                    if ROUTE in servel:
                        pos_list.append(data['branch_lines'].index(servel))
                        
                pos_list = list(set(pos_list))
                
                for pos in pos_list:
                    del data['branch_lines'][pos]
                    data['branch_lines'].sort()
                    
                pos_list = []
                
            if 'direct_lines' in data:
                direct_pos_list = []
                for servel in data['direct_lines']:
                    if ROUTE in servel:
                        direct_pos_list.append(data['direct_lines'].index(servel))
                
                for direct_pos in direct_pos_list:
                    del data['direct_lines'][direct_pos]
                    data['direct_lines'].sort()
                    
                direct_pos_list = []
                
                if len(data['direct_lines']) == 0:
                    data['direct_lines'] = [["None","开往 None 方向"]]
                    
            if 'lines' in data:
                first_loop = [[min([num for num in item[1][0] if num != 0]), item[0]] for item in data['lines'][f'Line_{ROUTE}'].items()]
                
                max_num = max([item[0] for item in first_loop])
                middle = max_num // 2
                
                all_loop = []
                mid_plus_num = 1
                while True:
                    for item in first_loop:
                        if item[0] == middle + mid_plus_num:
                            all_loop.append([[item[0], max_num + mid_plus_num], item[1]])
                    for item in first_loop:
                        if item[0] == middle + mid_plus_num - max_num:
                            all_loop.append([[item[0], max_num + mid_plus_num], item[1]])
                    if max_num + mid_plus_num == 2 * max_num:
                        break
                    mid_plus_num += 1
                            
                for item, servel in itertools.product(data['lines'][f'Line_{ROUTE}'].items(), all_loop):
                    
                    if item[0] == servel[1]:
                        data['lines'][f'Line_{ROUTE}'][item[0]] = [servel[0]] + data['lines'][f'Line_{ROUTE}'][item[0]][1:]
                    
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
                
            return True
            
        else:
            self.makeDialog.haveBranch.setCheckable(True)
            self.makeDialog.haveBranch.setStyleSheet('color: balck;')
            self.makeDialog.haveBranch.setFont(QFont("黑体", 12))
            
            self.makeDialog.oneDirection.setCheckable(True)
            self.makeDialog.oneDirection.setStyleSheet('color: black;')
            self.makeDialog.oneDirection.setFont(QFont("黑体", 12))
            
            self.makeDialog.numHidden.setCheckable(True)
            self.makeDialog.numHidden.setStyleSheet('color: black;')
            self.makeDialog.numHidden.setFont(QFont("黑体", 12))
            
            file_path = Producer.route.resourcePath("mader/folder/data.json")
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
                
            if 'lines' in data:
                data['lines'][f'Line_{ROUTE}'] = {item[0]: [ [min([num for num in item[1][0] if num != 0])] ] + item[1][1:] for item in data['lines'][f'Line_{ROUTE}'].items()}
                
            # 将修改后的数据写回 JSON 文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
            
        self.get_title()
        self.add_stations()
        
        
    def add_stations(self):

        global ROUTE
        
        btn_number = 0
        self.names = []
        
        if self.num != 0:
            self.clearLayout(self.p_layout)
        else:
            self.p_layout = QVBoxLayout()  
            self.p_layout.setAlignment(Qt.AlignTop)
            self.makeDialog.scrollArea.widget().setLayout(self.p_layout) 
            
        self.num += 1
        
        stations = self.getAim(resourcePath("mader/folder/data.json"), "lines")[f"Line_{ROUTE}"]
        direct_lines = self.getAim(resourcePath("mader/folder/data.json"), "direct_lines")
        
        num_route_list = []
        for station in self.station_get(stations):
            if ROUTE in [item[0] for item in direct_lines]:
                num_route_list += station[2][0]
            else:
                num_route_list.append(station[2][0][0])
            
        num_route_list = sorted([item for item in num_route_list if item != 0])
            
        for servel_num in num_route_list:
            
            for station in self.station_get(stations):
                
                num_route = station[2][0]
                color = station[2][1]
                
                if ROUTE in [item[0] for item in direct_lines]:
                    num_ruled = num_route[0]
                    if servel_num != num_ruled:
                        num_ruled = num_route[1]
                else:
                    num_ruled = num_route[0]
                        
                if servel_num == num_ruled:
                    
                    button_layout = QHBoxLayout()
                    
                    if len(str(num_ruled)) == 1:
                        num_ruled = f"0{num_ruled}"
                        
                    self_color = [item[1] for item in color if item[0] == ROUTE]
                        
                    info = [num_ruled, self_color[0], color]
                    
                    name_CN = New_Producer.betterChinese(station[0])
                    name_EN = New_Producer.betterEnglish(station[1])
                        
                    if len(station) == 3:
                        button = RichTextButton("""
                        <span style="font-size:16px; color:black;">{}</span><br>
                        <span style="font-size:12px; color:black;">{}</span><br>
                        <span></span>
                        """.format(name_CN,name_EN), info)
                        
                    else:
                        if station[3] == None:
                            sub_name_EN = New_Producer.betterEnglish(station[4][1])
                            
                            button = RichTextButton("""
                            <span style="font-size:16px; color:black;">{}</span><br>
                            <span style="font-size:16px; color:black;">{}</span>
                            <span style="font-size:12px; color:gray;"> ({})</span><br>
                            <span></span>
                            """.format(name_CN,name_EN,sub_name_EN), info)
                            
                        elif station[4] == None:
                            sub_name_CN = New_Producer.betterChinese(station[3][1])
                            
                            button = RichTextButton("""
                            <span style="font-size:16px; color:black;">{}</span>
                            <span style="font-size:16px; color:gray;"> {}</span><br>
                            <span style="font-size:12px; color:black;">{}</span><br>
                            <span></span>
                            """.format(name_CN,sub_name_CN,name_EN), info)
                        else:
                            sub_name_CN = New_Producer.betterChinese(station[3][1])
                            sub_name_EN = New_Producer.betterEnglish(station[4][1])
                            
                            button = RichTextButton("""
                            <span style="font-size:16px; color:black;">{}</span>
                            <span style="font-size:16px; color:gray;"> {}</span><br>
                            <span style="font-size:12px; color:black;">{}</span>
                            <span style="font-size:12px; color:gray;"> ({})</span><br>
                            <span></span>
                            """.format(name_CN,sub_name_CN,name_EN,sub_name_EN), info)
                        
                    button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                    button.setFixedHeight(66)
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
                    button.clicked.connect(lambda checked, btn=btn_number: self.afterButtonClick(btn))
                    button_layout.insertWidget(0, button)
                    
                    
                    menu = QVBoxLayout()
                    up_down_layout = QHBoxLayout()
                    
                    if servel_num != max(num_route_list):
                        up = QPushButton()
                        up.setText("+")
                        up.setFont(QFont("黑体", 16))
                        up.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                        up.setStyleSheet("""
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
                        up.clicked.connect(lambda checked, num=servel_num: self.upStation(num))
                        up_down_layout.addWidget(up)
                    
                    down = QPushButton()
                    if servel_num != min(num_route_list):
                        down.setText("-")
                        down.setFont(QFont("黑体", 16))
                        down.setIconSize(QSize(20, 20))
                        down.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                        down.setStyleSheet("""
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
                        down.clicked.connect(lambda checked, num=servel_num: self.downStation(num))
                        up_down_layout.addWidget(down)
                    
                    menu.insertLayout(0, up_down_layout)
                    
                    delete = QPushButton()
                    delete.setText("删除")
                    delete.setFont(QFont("黑体", 12))
                    delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                    delete.setStyleSheet("""
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
                    delete.clicked.connect(lambda checked, num=servel_num: self.sureDelete(num))
                    menu.insertWidget(1, delete)
                    
                    button_layout.insertLayout(1, menu)
                    button_layout.setStretch(0, 518)
                    button_layout.setStretch(1, 100)
                    
                    self.p_layout.addLayout(button_layout)
                    
                    horizontal_line = QFrame()
                    horizontal_line.setFrameShape(QFrame.HLine)
                    horizontal_line.setFrameShadow(QFrame.Plain)
                    horizontal_line.setLineWidth(2)
                    horizontal_line.setStyleSheet("color: gray;")
                    horizontal_line.setObjectName(station[1])
                    self.p_layout.addWidget(horizontal_line)
                    
                    self.names.append([btn_number, station[1]]) # 这里是数据汇总表
                    
                    btn_number += 1
                   
        create = QPushButton()
        create.setFont(QFont("黑体", 12))
        create.setText("新增站点")
        create.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        create.setFixedHeight(30)
        create.setStyleSheet("""
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
        create.clicked.connect(self.createNewStation)
        
        self.p_layout.addWidget(create)
        
        
    def createNewStation(self):
        
        global ROUTE
        LOOP = False

        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
        
        if 'lines' in data:
            process_list = [[key, (value[0])] for key, value in data['lines'][f'Line_{ROUTE}'].items()]
            need_dict = {}
            need_list = []
            for item in process_list:
                if len(item[1]) == 2 and ROUTE not in [i[0] for i in data['direct_lines']]:
                    need_list.append([min(item[1]), item[0]])
                    LOOP = True
                    
                else:
                    for servel in item[1]:
                        if servel == 0:
                            continue
                        need_dict[servel] = item[0]
                        
            if need_dict != {}:
                number = 1
                for _ in range(len(self.all_EN_list)):
                    for item in self.all_EN_list:
                        if f"New1o1Station1o1{number}" in item:
                            number += 1
                            
                if ROUTE in [i[0] for i in data['direct_lines']]:
                    need_dict[max([key for key in need_dict.keys()]) + 1] = need_dict[max([key for key in need_dict.keys()])]
                    need_dict[max([key for key in need_dict.keys()]) - 1] = f"New1o1Station1o1{number}"
                else:
                    need_dict[max([key for key in need_dict.keys()]) + 1] = f"New1o1Station1o1{number}"
                
            if need_list != []:
                number = 1
                for _ in range(len(need_list)):
                    for item in need_list:
                        if f"New1o1Station1o1{number}" == item[1]:
                            number += 1
                need_list.append([max([item[0] for item in need_list]) + 1, f"New1o1Station1o1{number}"])
                    
            if ROUTE in [i[0] for i in data['direct_lines']]:
                for servel in need_dict.items():
                    if servel[0] == min([item[0] for item in need_dict.items()]):
                        min_station = servel[1]
                        
                    if servel[0] == max([item[0] for item in need_dict.items()]):
                        max_station = servel[1]
                    
                if min_station != max_station:
                    num = 1
                    for _ in range(len(self.all_EN_list)):
                        for servel in self.all_EN_list:
                            if servel == f'Empty1o1Station1o1{num}':
                                num += 1
                            
                    need_dict[0] = f'Empty1o1Station1o1{num}'
                    need_dict[max([item[0] for item in need_dict.items()]) + 1] =  f'Empty1o1Station1o1{num}'
                    
            if LOOP == True:
                need_dict = {}
                new_list = []
                new_key = 1
                for item in sorted(need_list):
                    new_list.append([new_key, item[1]])
                    new_key += 1
                
                need_list = new_list
                
                max_num = max([item[0] for item in need_list])
                middle = max_num // 2
                
                all_loop = []
                mid_plus_num = 1
                while True:
                    for item in need_list:
                        if item[0] == middle + mid_plus_num:
                            all_loop.append([(item[0], max_num + mid_plus_num), item[1]])
                    for item in need_list:
                        if item[0] == middle + mid_plus_num - max_num:
                            all_loop.append([(item[0], max_num + mid_plus_num), item[1]])
                    if max_num + mid_plus_num == 2 * max_num:
                        break
                    mid_plus_num += 1
                    
                for servel in all_loop:
                    for item in servel[0]:
                        if item == 0:
                            continue
                        need_dict[item] = servel[1]
                    
            # 重新排列键，使键连续
            final_dict = {}
            new_key = 1
            for key in sorted(need_dict.keys()):
                final_dict[new_key] = need_dict[key]
                new_key += 1
            
            result = {}
            for key, value in final_dict.items():
                if value not in result:
                    result[value] = [key]
                else:
                    result[value].append(key)
            
            for item in data['lines'][f'Line_{ROUTE}'].items():
                if item[0] in result.keys():
                    result[item[0]] = [result[item[0]]] + item[1][1:]
                    
            for item in result.items():
                if len(item[1]) != 3:
                    number = 1
                    for _ in range(len(self.all_CN_list)):
                        for servel in self.all_CN_list:
                            if servel == f'新增站点{number}-{item[0][-1]}':
                                number += 1
                    result[item[0]] = [result[item[0]]] + [f'新增站点{number}-{item[0][-1]}', '暂无']
                    
            if ROUTE in [i[0] for i in data['direct_lines']]:
                for key,value in result.items():
                    if len(value[0]) == 1:
                        result[key][0].append(0)
                        
        data['lines'][f'Line_{ROUTE}'] = result
       
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
        
        self.add_stations()
        
        self.all_CN_list = Producer.route.last(Producer.route.flatten([[x[1][1] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
        self.all_EN_list = Producer.route.last(Producer.route.flatten([[x[0] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))

            
    def afterButtonClick(self, button_number):
        
        global ROUTE
        
        for name in self.names:
            if name[0] == button_number:
                station_name = name[1]
                
        window = Make_Station_Dialog.make_dialog(station_name, ROUTE)
        window.exec_()
                
        self.add_stations()
        
        
    def upStation(self, station_num):
        
        global ROUTE

        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
        
        if 'lines' in data:
            
            if len(list(data['lines'][f'Line_{ROUTE}'].values())[0][0]) == 2: # 单行线
                
                if ROUTE in [i[0] for i in data['direct_lines']]:

                    num_list = []
                    for item in data['lines'][f'Line_{ROUTE}'].values():
                        num_list += item[0]
                    
                    num_list = sorted([item for item in num_list if item != 0])
                    
                    station_dict = {}
                    for num in num_list:
                        for item in data['lines'][f'Line_{ROUTE}'].items():
                            if num in item[1][0]:
                                station_dict[num] = item[0]
                                
                    now_station = station_dict[station_num]
                    rep_station = station_dict[station_num + 1]
                    
                    station_dict[station_num + 1] = now_station
                    station_dict[station_num] = rep_station
                    
                    station_dict = self.collapse_dict(station_dict)
                    
                    result = {}
                    for key, value in station_dict.items():
                        if value not in result:
                            result[value] = [key]
                        else:
                            result[value].append(key)
                    
                    for item in data['lines'][f'Line_{ROUTE}'].items():
                        
                        if item[0] in result.keys():
                            result[item[0]] = [result[item[0]]] + item[1][1:]
                    
                    for item in result.items():
                        
                        if len(item[1]) != 3:
                            number = 1
                            for _ in range(len(self.all_CN_list)):
                                for servel in self.all_CN_list:
                                    if servel == f'头端站点{number}-{item[0][-1]}':
                                        number += 1
                            result[item[0]] = [result[item[0]]] + [f'头端站点{number}-{item[0][-1]}', '暂无']
                         
                    for key,value in result.items():
                        if len(value[0]) == 1:
                            result[key][0].append(0)
                            
                    data['lines'][f'Line_{ROUTE}'] = result
                            
                else: # 环线
                    for item in data['lines'][f'Line_{ROUTE}'].items():
                        if item[1][0][0] == station_num:
                            new_station = [item[0], item[1][0]]
                        if item[1][0][0] == station_num + 1:
                            replace_station = [item[0], item[1][0]]
                    
                    for item in data['lines'][f'Line_{ROUTE}'].items():
                        if item[0] == new_station[0]:
                            data['lines'][f'Line_{ROUTE}'][new_station[0]][0] = replace_station[1]
                        if item[0] == replace_station[0]:
                            data['lines'][f'Line_{ROUTE}'][replace_station[0]][0] = new_station[1]
                
            else: # 普通线
                for item in data['lines'][f'Line_{ROUTE}'].items():
                    if item[1][0][0] == station_num:
                        new_station = [item[0], item[1][0]]
                    if item[1][0][0] == station_num + 1:
                        replace_station = [item[0], item[1][0]]
                
                for item in data['lines'][f'Line_{ROUTE}'].items():
                    if item[0] == new_station[0]:
                        data['lines'][f'Line_{ROUTE}'][new_station[0]][0] = replace_station[1]
                    if item[0] == replace_station[0]:
                        data['lines'][f'Line_{ROUTE}'][replace_station[0]][0] = new_station[1]
       
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
        
        self.add_stations()
        
        self.all_CN_list = Producer.route.last(Producer.route.flatten([[x[1][1] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
        self.all_EN_list = Producer.route.last(Producer.route.flatten([[x[0] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
        
        
    def downStation(self, station_num):
        
        global ROUTE

        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
        
        if 'lines' in data:
            
            if len(list(data['lines'][f'Line_{ROUTE}'].values())[0][0]) == 2: # 单行线
                
                if ROUTE in [i[0] for i in data['direct_lines']]:

                    num_list = []
                    for item in data['lines'][f'Line_{ROUTE}'].values():
                        num_list += item[0]
                    
                    num_list = sorted([item for item in num_list if item != 0])
                    
                    station_dict = {}
                    for num in num_list:
                        for item in data['lines'][f'Line_{ROUTE}'].items():
                            if num in item[1][0]:
                                station_dict[num] = item[0]
                                
                    now_station = station_dict[station_num]
                    rep_station = station_dict[station_num - 1]
                    
                    station_dict[station_num - 1] = now_station
                    station_dict[station_num] = rep_station
                    
                    station_dict = self.collapse_dict(station_dict)
                    
                    result = {}
                    for key, value in station_dict.items():
                        if value not in result:
                            result[value] = [key]
                        else:
                            result[value].append(key)
                    
                    for item in data['lines'][f'Line_{ROUTE}'].items():
                        
                        if item[0] in result.keys():
                            result[item[0]] = [result[item[0]]] + item[1][1:]
                    
                    for item in result.items():
                        
                        if len(item[1]) != 3:
                            number = 1
                            for _ in range(len(self.all_CN_list)):
                                for servel in self.all_CN_list:
                                    if servel == f'头端站点{number}-{item[0][-1]}':
                                        number += 1
                            result[item[0]] = [result[item[0]]] + [f'头端站点{number}-{item[0][-1]}', '暂无']
                         
                    for key,value in result.items():
                        if len(value[0]) == 1:
                            result[key][0].append(0)
                            
                    data['lines'][f'Line_{ROUTE}'] = result
                               
                else: # 环线
                    for item in data['lines'][f'Line_{ROUTE}'].items():
                        if item[1][0][0] == station_num:
                            new_station = [item[0], item[1][0]]
                        if item[1][0][0] == station_num - 1:
                            replace_station = [item[0], item[1][0]]
                    
                    for item in data['lines'][f'Line_{ROUTE}'].items():
                        if item[0] == new_station[0]:
                            data['lines'][f'Line_{ROUTE}'][new_station[0]][0] = replace_station[1]
                        if item[0] == replace_station[0]:
                            data['lines'][f'Line_{ROUTE}'][replace_station[0]][0] = new_station[1]
                
            else: # 普通线
                for item in data['lines'][f'Line_{ROUTE}'].items():
                    if item[1][0][0] == station_num:
                        new_station = [item[0], item[1][0]]
                    if item[1][0][0] == station_num - 1:
                        replace_station = [item[0], item[1][0]]
                
                for item in data['lines'][f'Line_{ROUTE}'].items():
                    if item[0] == new_station[0]:
                        data['lines'][f'Line_{ROUTE}'][new_station[0]][0] = replace_station[1]
                    if item[0] == replace_station[0]:
                        data['lines'][f'Line_{ROUTE}'][replace_station[0]][0] = new_station[1]
       
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
        
        self.add_stations()
        
        self.all_CN_list = Producer.route.last(Producer.route.flatten([[x[1][1] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
        self.all_EN_list = Producer.route.last(Producer.route.flatten([[x[0] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
        
        
    def sureDelete(self, num):
        
        sure_dialog = sureDelete()
        
        result = sure_dialog.exec_()  # 显示对话框并获取返回值

        if result == QDialog.Accepted:
            self.deleteStation(num)


    def deleteStation(self, num):
        
        global ROUTE
        LOOP = False
        
        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
        
        if 'lines' in data:
            process_list = [[key, (value[0])] for key, value in data['lines'][f'Line_{ROUTE}'].items() if num not in value[0]]
            need_dict = {}
            need_list = []
            for item in process_list:
                if len(item[1]) == 2 and ROUTE not in [i[0] for i in data['direct_lines']]:
                    need_list.append([min(item[1]), item[0]])
                    LOOP = True
                    
                else:
                    for servel in item[1]:
                        if servel == 0:
                            continue
                        need_dict[servel] = item[0]
                    
            if ROUTE in [i[0] for i in data['direct_lines']]:
                for servel in need_dict.items():
                    if servel[0] == min([item[0] for item in need_dict.items()]):
                        min_station = servel[1]
                        
                    if servel[0] == max([item[0] for item in need_dict.items()]):
                        max_station = servel[1]
                    
                if min_station != max_station:
                    num = 1
                    for _ in range(len(self.all_EN_list)):
                        for servel in self.all_EN_list:
                            if servel == f'Empty1o1Station1o1{num}':
                                num += 1
                            
                    need_dict[0] = f'Empty1o1Station1o1{num}'
                    need_dict[max([item[0] for item in need_dict.items()]) + 1] =  f'Empty1o1Station1o1{num}'
                    
            if LOOP == True:
                new_list = []
                new_key = 1
                for item in sorted(need_list):
                    new_list.append([new_key, item[1]])
                    new_key += 1
                
                need_list = new_list
                
                max_num = max([item[0] for item in need_list])
                middle = max_num // 2
                
                all_loop = []
                mid_plus_num = 1
                while True:
                    for item in need_list:
                        if item[0] == middle + mid_plus_num:
                            all_loop.append([(item[0], max_num + mid_plus_num), item[1]])
                    for item in need_list:
                        if item[0] == middle + mid_plus_num - max_num:
                            all_loop.append([(item[0], max_num + mid_plus_num), item[1]])
                    if max_num + mid_plus_num == 2 * max_num:
                        break
                    mid_plus_num += 1
                    
                for servel in all_loop:
                    for item in servel[0]:
                        if item == 0:
                            continue
                        need_dict[item] = servel[1]
                    
            # 重新排列键，使键连续
            final_dict = {}
            new_key = 1
            for key in sorted(need_dict.keys()):
                final_dict[new_key] = need_dict[key]
                new_key += 1
            
            result = {}
            for key, value in final_dict.items():
                if value not in result:
                    result[value] = [key]
                else:
                    result[value].append(key)
            
            for item in data['lines'][f'Line_{ROUTE}'].items():
                if item[0] in result.keys():
                    result[item[0]] = [result[item[0]]] + item[1][1:]
                    
            for item in result.items():
                if len(item[1]) != 3:
                    number = 1
                    for _ in range(len(self.all_CN_list)):
                        for servel in self.all_CN_list:
                            if servel == f'头端站点{number}-{item[0][-1]}':
                                number += 1
                    result[item[0]] = [result[item[0]]] + [f'头端站点{number}-{item[0][-1]}', '暂无']
                    
            if ROUTE in [i[0] for i in data['direct_lines']]:
                for key,value in result.items():
                    if len(value[0]) == 1:
                        result[key][0].append(0)
                        
        data['lines'][f'Line_{ROUTE}'] = result
       
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
        
        self.add_stations()
        LOOP = False
        
        self.all_CN_list = Producer.route.last(Producer.route.flatten([[x[1][1] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
        self.all_EN_list = Producer.route.last(Producer.route.flatten([[x[0] for x in servel.items()] for servel in [item[1] for item in self.getAim(resourcePath("mader/folder/data.json"), "lines").items()]]))
    
    
    def getAim(self, file_path, aim):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return(data.get(aim))
        
        
    def sortDict(self, dct, keyOrValue):
        if keyOrValue == "key":
            sorted_dict = dict(sorted(dct.items(), key=lambda item: item[0]))
            return sorted_dict
        
        elif keyOrValue == "value":
            sorted_dict = dict(sorted(dct.items(), key=lambda item: item[0]))
            return sorted_dict
        
        else:
            return
        
    
    def station_get(self, dct):
        
        RGB = self.getAim(resourcePath("mader/folder/data.json"), "color")
        LIS = self.getAim(resourcePath("mader/folder/data.json"), "lines")
        station_name = []
        
        for item in dct.items():
            
            name = item[1][1]
            value = item[0]
            
            result_dct = {line: stations for line, stations in LIS.items() if value in stations}
            result_lst = [item.replace("Line_","") for item in result_dct.keys()]
            
            color = [[result, RGB_line[1]] for result, RGB_line in itertools.product(result_lst, RGB.items()) if result == RGB_line[0]]
    
            name_list = [name, value, [item[1][0], color]]
                    
            if "1tc1" in name or "1te1" in value:
                
                if "1tc1" in name:
                    list_EN = name.split("1tc1")
                    name_list.insert(3, list_EN)
                else:
                    name_list.insert(3, None)
                    
                if "1te1" in value:
                    list_CN = value.split("1te1")
                    name_list.insert(4, list_CN)
                else:
                    name_list.insert(4, None)
            
            station_name.append(name_list)
                  
        return station_name
    
    
    def collapse_dict(self, input_dict):

        sorted_items = sorted(input_dict.items())
        
        result = []
        
        # 初始化当前键值对
        current_key = None
        current_value = None
        
        for key, value in sorted_items:
            if current_key is None:
                # 如果是第一个键值对，直接初始化
                current_key = key
                current_value = value
                
                if isinstance(current_key, tuple):
                    current_key = min(current_key)
                
            elif value == current_value:
                # 保留第一个键的值
                current_key = (current_key, key)
                
                if isinstance(current_key, tuple):
                    current_key = min(current_key)
                
            else:
                result.append((current_key, current_value))
                current_key = key
                current_value = value
                
                if isinstance(current_key, tuple):
                    current_key = min(current_key)
                
        result.append((current_key, current_value))
        
        for servel in result:
            
            if servel[0] == min([item[0] for item in result]):
                min_station = servel[1]
                
            if servel[0] == max([item[0] for item in result]):
                max_station = servel[1]
                
        if min_station != max_station:
            
            num = 1
            for _ in range(len(self.all_EN_list)):
                for servel in self.all_EN_list:
                    if servel == f'Empty1o1Station1o1{num}':
                        num += 1
                    
            result.append((0, f'Empty1o1Station1o1{num}'))
            result.append((max([item[0] for item in result]) + 1, f'Empty1o1Station1o1{num}'))
        
        collapsed_dict = {key: value for key, value in result}
        
        # 重新排列键，使键连续
        final_dict = {}
        new_key = 1
        for key in sorted(collapsed_dict.keys()):
            final_dict[new_key] = collapsed_dict[key]
            new_key += 1

        return final_dict
    
    
    def clearLayout(self, layout):
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() 
            if widget:
                widget.deleteLater()  
            else:
                self.clearLayout(item.layout())  
        
        
    def closeEvent(self, event):
        event.ignore()
        self.searchOldWindow()
        self.deleteLater()
        


class error(QtWidgets.QDialog):
    
    def __init__(self):

        super().__init__()
        self.errorDialog = uic.loadUi(Producer.route.resourcePath("window/ui/error.ui"), self)
        
        ctypes.windll.user32.MessageBeep(0x00000010)
        self.errorDialog.error.setText("输入无效")
        
        
        
class sureDelete(QtWidgets.QDialog):
    
    def __init__(self):

        ctypes.windll.user32.MessageBeep(0x00000010)
        
        super().__init__()
        self.sureDialog = uic.loadUi(Producer.route.resourcePath("window/ui/sure.ui"), self)
        
        self.sureDialog.que.setText("您确定要删除吗？\n同线路中具有相同识别码的站点也将被删除!")
        self.sureDialog.que.setAlignment(Qt.AlignCenter)
        
        self.sureDialog.yes.clicked.connect(self.accept)
        self.sureDialog.cancel.clicked.connect(self.reject)
    
    def closeEvent(self, event):
        event.ignore()
        self.sureDialog.deleteLater()
        
        
        
class RichTextButton(QPushButton):
    def __init__(self, text, info, parent=None):
        
        global ROUTE
        
        self.info = info
        super().__init__(parent)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.label.setStyleSheet("""
        QLabel {
            font-family: 微软雅黑;
            background-color: transparent;
            border: 0px solid transparent;
            padding: 6px;
        }
        """)
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        branch_lines = self.getAim(resourcePath("mader/folder/data.json"), "branch_lines")
        
        branch = [item[1] for item in branch_lines if item[0] != "False"]
        main = [item[0] for item in branch_lines if item[1] == ROUTE and item[0] != "False"]
        num = info[0]
        
        self.num = QLabel(self)
        self.num.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.num.setFont(QFont("黑体", 20))
        
        if ROUTE in branch:
            if set([name[0] for name in info[2]]) & set(main):
                num = f"{info[0]}"
            else:
                num = f"Y{info[0]}"
                self.num.setFont(QFont("黑体", 16))
        
        self.num.setText(f" {num}")
        self.num.setStyleSheet(f"color: {info[1]}")
        self.num.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.num.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.layout = QHBoxLayout(self)
        self.layout.insertWidget(0, self.num)
        self.layout.insertWidget(1, self.label)
        
        self.setLayout(self.layout)
        
        self.colorRoute()

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
        
    def colorRoute(self):
        layouts = {}
        num = 1
        layout_num = 1
        
        layouts[f"{layout_num}"] = QVBoxLayout()
        
        for color in self.info[2]:
            num += 1
            if num %2 == 0:
                layout_num += 1
                layouts[f"{layout_num}"] = QVBoxLayout()
                
            label = QLabel()
            label.setText(color[0])
            label.setFont(QFont("微软雅黑", 9))
            label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            label.setFixedWidth(60)
            label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            label.setStyleSheet("""
            QLabel {{
                color: rgb(255,255,255);
                border: 2px solid {}; 
                background-color: {}; 
                border-radius: 10px; 
            }}
            """.format(color[1], New_Producer.darkerColor(color[1])))
            layouts[f"{layout_num}"].addWidget(label)
        
        for layout_num_servel in range(layout_num + 1, 0, -1):
            for layout in layouts.items():
                if layout[0] == str(layout_num_servel):
                    self.layout.addLayout(layout[1])
                    
    def getAim(self, file_path, aim):
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return(data.get(aim))