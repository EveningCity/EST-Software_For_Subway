import ctypes
import itertools
import json
import os
import sys
import uuid
import zipfile
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import New_Producer
import Producer
import Station_Search
from window import Main, Make_Dialog, Make_Route_Dialog


ERROR = None
NAME = None

def resourcePath(relative_path):
    """获取资源的绝对路径，适用于Dev和PyInstaller"""
    
    try:
        # PyInstaller 会创建一个临时文件夹并将路径存储在 _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class pack_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        global NAME
        self.num = 0
        NAME = Make_Dialog.NAME
        
        super().__init__()
        self.packDialog = uic.loadUi(Producer.route.resourcePath("window/ui/make_pack_dialog.ui"), self)
        
        self.packDialog.change_pack_name.clicked.connect(self.packName)
        self.packDialog.save.clicked.connect(self.sureSave)
        self.packDialog.uuid.clicked.connect(self.changeUUID)
        self.packDialog.get.clicked.connect(self.addRoute)
        self.packDialog.add.clicked.connect(self.newRoute)
                
        self.packDialog.now_pack_name.setText("当前的资源包名称是：{}".format(self.getPackName(Producer.resourcePath("mader/folder/data.json"))))
        self.packDialog.uuidText.setText("资源包的UUID是：{}".format(self.getUUID(Producer.resourcePath("mader/folder/data.json"))))
        
        self.addRoute()
        
            
    def packName(self):
        
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
        
        self.packDialog.pack_name.setStyleSheet(passCode)
        self.packDialog.pack_name.setFont(QFont("黑体", 12))
        
        name = r"{}".format(self.packDialog.pack_name.text())
                
        # 检查输入
        if "\\" in name or len(name)>= 10 or name == "":
            # 创建一个错误消息框
            global ERROR
            ERROR = "含有无效字符、输入长度超过10个字符或输入为空"
            errorWindow = error()
            errorWindow.show()
            
            self.packDialog.pack_name.setStyleSheet(errorCode)
            self.packDialog.pack_name.setFont(QFont("黑体", 12))
            
        else:
            file_path = Producer.resourcePath("mader/folder/data.json")
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if "pack_name" in data:
                data["pack_name"] = name

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4, ensure_ascii=False)
            self.packDialog.now_pack_name.setText("当前的资源包名称是：{}".format(self.getPackName(file_path)))


    def changeUUID(self):
        
        file_path = Producer.resourcePath("mader/folder/data.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if "uuid" in data:
            data["uuid"] = f"{uuid.uuid4()}"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        self.packDialog.uuidText.setText("资源包的UUID是：{}".format(self.getUUID(file_path)))
    
    
    def getPackName(self, file_path):
        
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return(data.get("pack_name"))
            
            
    def getUUID(self, file_path):
        
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return(data.get("uuid"))
            
            
    def sureSave(self):
        
        sureDialog = sure()
        sureDialog.exec_()
        
        
    def addRoute(self):
        
        num = 0
        self.routes = []
        
        color = self.getAim(resourcePath("mader/folder/data.json"), "color")
        routes_CN = self.getAim(resourcePath("mader/folder/data.json"), "routes_CN")
        
        query = self.packDialog.searchText.text()
        result = Station_Search.fuzzy_search(query, New_Producer.formatLineList(self.getAim(resourcePath("mader/folder/data.json"), "routes_EN"), routes_CN))
        
        if self.num != 0:
            self.clearLayout(self.pack_layout)
            
        self.num += 1
        
        if isinstance(result, list):
            self.pack_layout.setAlignment(Qt.AlignTop)
            
            result_formal = [routes_CN[key] for key in result]
        
            for servel_route in result_formal:
                
                every_layout = QHBoxLayout()
                self.pack_layout.addLayout(every_layout)
                
                button = QPushButton(f"Route{num}")
                button.setText(f" {New_Producer.formatLine(servel_route, routes_CN)} ")  
                button.setFont(QFont("黑体", 12))
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                button.setFixedHeight(30)
                button.setStyleSheet("""
                QPushButton {{
                    color: rgb(255,255,255);
                    border: 2px solid gray; 
                    background-color: {}; 
                    border-radius: 10px; 
                }}
                QPushButton:hover {{
                    background-color: {}; 
                }}
                QPushButton:pressed {{
                    border: 2px solid #33373E; 
                    background-color: {}; 
                }}
                """.format(New_Producer.colorRoute(servel_route, color),
                        New_Producer.darkerColor(New_Producer.colorRoute(servel_route, color)),
                        New_Producer.darkerColor(New_Producer.colorRoute(servel_route, color))))
                button.clicked.connect(lambda checked, btn=num: self.afterClick(btn))
                every_layout.addWidget(button)  
                self.routes.append([num, servel_route])
                
                copy = QPushButton(f"Copy{num}")
                copy.setText("复制")
                copy.setFont(QFont("黑体", 12))
                copy.setMinimumSize(60, 30)  
                copy.setStyleSheet("""
                QPushButton {
                    border: 2px solid gray; 
                    background-color: white; 
                    border-radius: 10px; 
                    color: black;
                }
                QPushButton:hover {
                    background-color: rgb(209, 209, 209); 
                }
                QPushButton:pressed {
                    background-color: rgb(190, 190, 190); 
                    border: 2px solid #33373E; 
                }
                """)
                every_layout.addWidget(copy)  
                copy.clicked.connect(lambda checked, btn=num: self.afterCopyClick(btn))
                
                delete = QPushButton(f"Button{num}")
                delete.setText("删除")
                delete.setFont(QFont("黑体", 12))
                delete.setMinimumSize(60, 30)  
                delete.setStyleSheet("""
                QPushButton {
                    border: 2px solid red; 
                    background-color: white; 
                    border-radius: 10px; 
                    color: red;
                }
                QPushButton:hover {
                    background-color: rgb(209, 209, 209); 
                }
                QPushButton:pressed {
                    background-color: rgb(190, 190, 190); 
                    border: 2px solid rgb(139, 0, 0); 
                }
                """)
                every_layout.addWidget(delete)  
                delete.clicked.connect(lambda checked, btn=num: self.afterDeleteClick(btn))
                
                every_layout.setStretch(0,518)
                every_layout.setStretch(1,100)
                every_layout.setStretch(2,100)
                
                num += 1
                
        else:
            self.pack_layout.setAlignment(Qt.AlignCenter)
            
            text = QLabel()
            text.setText("未找到匹配项，请检查输入或尝试其他查询")  
            text.setFont(QFont("黑体", 12))
            text.setAlignment(Qt.AlignCenter) 
            text.setMinimumSize(60, 30)  
            self.pack_layout.addWidget(text)
            
            
    def newRoute(self):
        
        num = 0
        
        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
        
        while f'Empty{num}' in data['routes_EN']:
            num += 1
            
        if 'routes_EN' in data:
            data['routes_EN'].append(f'Empty{num}')
            data['routes_EN'] = sorted(data['routes_EN'])
            
        if 'routes_CN' in data:
            data['routes_CN'][f'未知线路{num}'] = f'Empty{num}'
            data['routes_CN'] = self.sortDict(data['routes_CN'], "value")
            
        if 'above' in data:
            data['above'][f'Empty{num}'] = 'None'
            data['above'] = self.sortDict(data['above'], "key")
            
        if 'below' in data:
            data['below'][f'Empty{num}'] = 'None'
            data['below'] = self.sortDict(data['below'], "key")
            
        if 'color' in data:
            data['color'][f'Empty{num}'] = 'rgb(100,100,100)'
            data['color'] = self.sortDict(data['color'], "key")
            
        if 'time' in data:
            data['time'][f'Empty{num}'] = 'None'
            data['time'] = self.sortDict(data['time'], "key")
            
        if 'lines' in data:
            data['lines'][f'Line_Empty{num}'] = {"None": [[1],"未知站点","暂无"]}
            data['lines'] = self.sortDict(data['lines'], "key")
            
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
            
        self.addRoute()
        
        
    def afterClick(self, button_number):
        
        for servel in self.routes:
            if button_number == servel[0]:
                NAME = servel[1]
        Make_Route_Dialog.make_dialog(self.addRoute, NAME).exec_()
            
    
    def afterDeleteClick(self, button_number):
        
        global ERROR
        self.addRoute()
        if len(self.routes) == 1:
            ERROR = "资源包必须存在至少一条线路"
            error().exec_()
            return
        if len(self.routes) != 0:
            for name in self.routes:
                if name[0] == button_number:
                    NAME = name
            TEXT = "您确定要删除该线路？"
            sureWindow = delete(self.addRoute, NAME, TEXT)
            sureWindow.exec_()
        else:
            ERROR = "搜索结果为空"
            error().exec_()
    
    
    def getAim(self, file_path, aim):
        
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            return(data.get(aim))
        
        
    def afterCopyClick(self, button_number):
        
        def numsOfCopy(num):
            text = []
            for _ in range(num):
                text.append("复制")
                
            return "的".join(text)
            
        num = 1
        
        for servel in self.routes:
            if button_number == servel[0]:
                NAME = servel[1]
        
        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典
        
        while f'{NAME.split("_copied")[0]}_copied{num}' in data['routes_EN']:
            num += 1
            
        if 'routes_EN' in data:
            data['routes_EN'].append(f'{NAME.split("_copied")[0]}_copied{num}')
            data['routes_EN'] = sorted(data['routes_EN'])
            
        if 'routes_CN' in data:
            data['routes_CN'][f'{New_Producer.formatLine(NAME.split("_copied")[0], data['routes_CN'])}（{numsOfCopy(num)}）'] = f'{NAME.split("_copied")[0]}_copied{num}'
            data['routes_CN'] = self.sortDict(data['routes_CN'], "value")
            
        if 'above' in data:
            data['above'][f'{NAME.split("_copied")[0]}_copied{num}'] = data['above'][NAME]
            data['above'] = self.sortDict(data['above'], "key")
            
        if 'below' in data:
            data['below'][f'{NAME.split("_copied")[0]}_copied{num}'] = data['below'][NAME]
            data['below'] = self.sortDict(data['below'], "key")
            
        if 'color' in data:
            data['color'][f'{NAME.split("_copied")[0]}_copied{num}'] = data['color'][NAME]
            data['color'] = self.sortDict(data['color'], "key")
            
        if 'time' in data:
            data['time'][f'{NAME.split("_copied")[0]}_copied{num}'] = data['time'][NAME]
            data['time'] = self.sortDict(data['time'], "key")
            
        if 'branch_lines' in data:
            name_list = []
            for servel in data['branch_lines']:
                if NAME in servel:
                    name_list.append(servel)
                    
            for servel in name_list:
                every_list = []
                for element in servel:
                    if element == NAME:
                        every_list.append(f'{NAME.split("_copied")[0]}_copied{num}')
                    else:
                        every_list.append(element)
                data['branch_lines'].append(every_list)

            data['branch_lines'].sort()
            
        if 'direct_lines' in data:
            name_list = []
            for servel in data['direct_lines']:
                if NAME in servel:
                    name_list.append(servel)
                    
            for servel in name_list:
                every_list = []
                if servel[0] == NAME:
                    every_list.insert(0, f'{NAME.split("_copied")[0]}_copied{num}')
                    every_list.insert(1, servel[1])
                data['direct_lines'].append(every_list)

            data['direct_lines'].sort()
            
        if 'lines' in data:
            data['lines'][f'Line_{NAME.split("_copied")[0]}_copied{num}'] = data['lines'][f'Line_{NAME}']
            data['lines'] = self.sortDict(data['lines'], "key")
            
        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
            
        self.addRoute()
    
    
    def clearLayout(self, layout):
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() 
            if widget:
                widget.deleteLater()  
            else:
                self.clearLayout(item.layout())  
                
                
    def sortDict(self, dct, keyOrValue):
        
        if keyOrValue == "key":
            sorted_dict = dict(sorted(dct.items(), key=lambda item: item[0]))
            return sorted_dict
        
        elif keyOrValue == "value":
            sorted_dict = dict(sorted(dct.items(), key=lambda item: item[0]))
            return sorted_dict
        
        else:
            return
        
        
    def closeEvent(self, event):
        
        event.ignore()
        sureDialog = sure()
        sureDialog.exec_()
                


class sure(QtWidgets.QDialog):
    
    def __init__(self):

        ctypes.windll.user32.MessageBeep(0x00000010)
        
        super().__init__()
        self.sureDialog = uic.loadUi(Producer.route.resourcePath("window/ui/save.ui"), self)
        
        self.sureDialog.que.setText("您确定要保存修改后的资源包？")
        
        self.sureDialog.yes.clicked.connect(self.ifYes)
        self.sureDialog.no.clicked.connect(self.ifNo)
        self.sureDialog.cancel.clicked.connect(self.ifCancel)
        
    def ifYes(self):
        
        global NAME

        def addToZip(zip_path, file_or_folder_path):
            
            if not os.path.exists(file_or_folder_path):
                return

            with zipfile.ZipFile(zip_path, "a", zipfile.ZIP_DEFLATED) as zipf:
                
                if os.path.isfile(file_or_folder_path):
                    # 如果是文件
                    arcname = os.path.basename(file_or_folder_path)
                    zipf.write(file_or_folder_path, arcname=arcname)
                    
                elif os.path.isdir(file_or_folder_path):
                    # 如果是文件夹
                    for root, dirs, files in os.walk(file_or_folder_path):
                        
                        for file in files:
                            
                            file_path = os.path.join(root, file)
                            # 计算文件在 ZIP 文件中的相对路径
                            arcname = os.path.relpath(file_path, start=os.path.dirname(file_or_folder_path))
                            zipf.write(file_path, arcname=arcname)
       
        os.remove(Producer.route.resourcePath(f"mader/zips/{Make_Dialog.NAME}"))
        
        path_list = [Producer.resourcePath("mader/folder/data.json"),
                     Producer.resourcePath("mader/folder/stations"),
                     Producer.resourcePath("mader/folder/map")]
        
        zip_path = Producer.resourcePath(f"mader/zips/{NAME}")

        for path in path_list:
            addToZip(zip_path,path)
            
        Main.JUDGE = False  
        for window in QApplication.topLevelWidgets():
            if window.objectName() != "Main":
                window.deleteLater()
        Make_Dialog.make_dialog().show()
        
    def ifNo(self):
        Main.JUDGE = False  
        for window in QApplication.topLevelWidgets():
            if window.objectName() != "Main":
                window.deleteLater()
        Make_Dialog.make_dialog().show()
        
    def ifCancel(self):
        self.deleteLater()
        
    def closeEvent(self, event):
        event.ignore()
        self.deleteLater()
        
    

class error(QtWidgets.QDialog):
    
    def __init__(self):
        
        global ERROR

        super().__init__()
        self.errorDialog = uic.loadUi(Producer.route.resourcePath("window/ui/error.ui"), self)
        
        ctypes.windll.user32.MessageBeep(0x00000010)
        self.errorDialog.error.setText(ERROR)
        
        
        
class delete(QtWidgets.QDialog):
    
    def __init__(self, callback_function, name, text):

        ctypes.windll.user32.MessageBeep(0x00000010)
        
        super().__init__()
        self.sureDialog = uic.loadUi(Producer.route.resourcePath("window/ui/sure.ui"), self)
        
        self.sureDialog.que.setText(text)
        
        self.sureDialog.yes.clicked.connect(self.ifYes)
        self.sureDialog.cancel.clicked.connect(self.ifCancel)
        
        self.callback_function = callback_function
        self.name = name
        
        
    def ifYes(self):
        
        NAME = self.name
        
        file_path = Producer.route.resourcePath("mader/folder/data.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)  # 将 JSON 文件内容加载为 Python 字典

        if 'routes_EN' in data and NAME[1] in data['routes_EN']:
            data['routes_EN'] = sorted(list(filter(lambda line: line != NAME[1], data['routes_EN'])))
            
        if 'routes_CN' in data and NAME[1] in data['routes_CN'].values():
            data['routes_CN'] = self.sortDict(dict(filter(lambda item: item[1] != NAME[1], data['routes_CN'].items())), "value")
            
        if 'above' in data and NAME[1] in data['above'].keys():
            data['above'] = self.sortDict(dict(filter(lambda item: item[0] != NAME[1], data['above'].items())), "key")
            
        if 'below' in data and NAME[1] in data['below'].keys():
            data['below'] = self.sortDict(dict(filter(lambda item: item[0] != NAME[1], data['below'].items())), "key")
            
        if 'color' in data and NAME[1] in data['color'].keys():
            data['color'] = self.sortDict(dict(filter(lambda item: item[0] != NAME[1], data['color'].items())), "key")
            
        if 'time' in data and NAME[1] in data['time'].keys():
            data['time'] = self.sortDict(dict(filter(lambda item: item[0] != NAME[1], data['time'].items())), "key")
           
        if 'branch_lines' in data:
            pos_list = []
            for servel in data['branch_lines']:
                if NAME[1] in servel:
                    pos_list.append(data['branch_lines'].index(servel))
                    
            pos_list = list(set(pos_list))
            
            for pos in pos_list:
                del data['branch_lines'][pos]
                data['branch_lines'].sort()
                
            pos_list = []
            
        if 'direct_lines' in data:
            direct_pos_list = []
            for servel in data['direct_lines']:
                if NAME[1] in servel:
                    direct_pos_list.append(data['direct_lines'].index(servel))
            
            for direct_pos in direct_pos_list:
                del data['direct_lines'][direct_pos]
                data['direct_lines'].sort()
                
            direct_pos_list = []
            
            if len(data['direct_lines']) == 0:
                data['direct_lines'] = [["None","开往 None 方向"]]
            
        if 'lines' in data and f'Line_{NAME[1]}' in data['lines']:
            del data['lines'][f'Line_{NAME[1]}']
            data['lines'] = self.sortDict(data['lines'], "key")

        # 将修改后的数据写回 JSON 文件
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)  # 使用 indent 参数美化输出格式
        
        self.callback_function()
        self.deleteLater()
        
        
    def ifCancel(self):
        
        self.deleteLater()
        
        
    def sortDict(self, dct, keyOrValue):
        
        if keyOrValue == "key":
            sorted_dict = dict(sorted(dct.items(), key=lambda item: item[0]))
            return sorted_dict
        elif keyOrValue == "value":
            sorted_dict = dict(sorted(dct.items(), key=lambda item: item[0]))
            return sorted_dict
        else:
            return
        
        
    def closeEvent(self, event):
        
        event.ignore()
        self.deleteLater()