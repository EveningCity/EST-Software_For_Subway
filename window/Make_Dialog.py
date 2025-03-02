import ctypes
import importlib
import json
import os
import shutil
from tkinter import filedialog
import tkinter
import uuid
import zipfile
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QApplication, QHBoxLayout, QFrame, QSizePolicy, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import Producer,Station_Search
from window import Main, Make_Pack_Dialog


NAME = None
ERROR = None

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module



class make_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        self.num = 1
        
        super().__init__()
        self.packDialog = uic.loadUi(Producer.route.resourcePath("window/ui/make_dialog.ui"), self)
        
        self.packDialog.get.clicked.connect(self.afterClick)
        self.packDialog.old_add.clicked.connect(self.afterAdd)
        self.packDialog.new_add.clicked.connect(self.afterNew)
        
        for window in QApplication.topLevelWidgets():
            if window.objectName() != "Main" and window != self:
                window.deleteLater()
        
        self.afterClick()
        
    def afterClick(self):

        self.clearLayout(self.pack_layout)
        self.pack_layout.setAlignment(Qt.AlignTop)
        
        files_name_list = []
        for filename in os.listdir(Producer.route.resourcePath("mader/zips/")):
            file_path = os.path.join(Producer.route.resourcePath("mader/zips/"), filename)
            if os.path.isfile(file_path) and filename.endswith(".zip"):
                files_name_list.append([filename, self.getPackName(Producer.route.resourcePath(file_path))])
                
        query = self.packDialog.searchText.text()
        answer = Station_Search.fuzzy_search(query, [item[1] for item in files_name_list])
        result = [item[0] for item in files_name_list if item[1] in answer]
        
        if isinstance(answer, list):
            
            btn_number = 0
            self.buttons = []
            self.exports = []
            self.names = []
                                
            for pack_name in result:
                                
                every_layout = QHBoxLayout()
                self.pack_layout.addLayout(every_layout)
                
                pack = QPushButton(f"Pack{btn_number}")
                pack.setText(self.getPackName(Producer.route.resourcePath(f"mader/zips/{pack_name}")))  
                pack.setFont(QFont("黑体", 12))
                pack.setMinimumSize(60, 30)  
                pack.setStyleSheet("""
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
                every_layout.addWidget(pack)  
                
                pack.clicked.connect(lambda checked, btn=btn_number: self.afterButtonClick(btn))
                self.names.append([btn_number, pack_name])
                
                
                export = QPushButton(f"Export{btn_number}")
                export.setText("导出")
                export.setFont(QFont("黑体", 12))
                export.setMinimumSize(60, 30)  
                export.setStyleSheet("""
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
                every_layout.addWidget(export)  
                
                export.clicked.connect(lambda checked, btn=btn_number: self.afterExport(btn))
                self.exports.append([btn_number, export])
                
                
                button = QPushButton(f"Button{btn_number}")
                button.setText("删除")
                button.setFont(QFont("黑体", 12))
                button.setMinimumSize(60, 30)  
                button.setStyleSheet("""
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
                every_layout.addWidget(button)  
                
                button.clicked.connect(lambda checked, btn=btn_number: self.afterDeleteClick(btn))
                self.buttons.append([btn_number, button])
                
                
                every_layout.setStretch(0,518)
                every_layout.setStretch(1,100)
                every_layout.setStretch(2,100)
                
                btn_number = btn_number + 1
                
        else:
            
            self.pack_layout.setAlignment(Qt.AlignCenter)
            
            p_text = QLabel()
            p_text.setText("未找到资源包，请检查输入或尝试其他查询")  
            p_text.setFont(QFont("黑体", 12))
            p_text.setAlignment(Qt.AlignCenter) 
            p_text.setMinimumSize(60, 30)  
            self.pack_layout.addWidget(p_text)  
            
            
    def afterButtonClick(self, button_number):
        
        folder_path = Producer.route.resourcePath("mader/folder/")
        file_name_list = ["data.json","stations","map"]

        for file_name in file_name_list:
            
            file_path = os.path.join(folder_path, file_name)
            # 检查文件是否存在
            if os.path.exists(file_path) and os.path.isdir(file_path):
                shutil.rmtree(file_path)
                continue
            if os.path.exists(file_path):
                os.remove(file_path)
                
        for name in self.names:
            if name[0] == button_number:
                file = Producer.route.resourcePath(f"mader/zips/{name[1]}")
                
        with zipfile.ZipFile(file, 'r') as zip_ref:
            zip_ref.extractall(Producer.route.resourcePath("mader/folder/"))
            
        self.afterClick()
        
        Make_Pack_Dialog.pack_dialog().exec_()
                
    
    def afterDeleteClick(self, button_number):
        
        self.afterClick()
        BTN = button_number
        if len(self.names) != 0:
            for name in self.names:
                if name[0] == BTN:
                    NAME = name[1]
                    
            sure_dialog = sure()
            result = sure_dialog.exec_()  # 显示对话框并获取返回值

            if result == QDialog.Accepted:
                os.remove(Producer.route.resourcePath(f"mader/zips/{NAME}"))
                self.afterClick()
        
        else:
            global ERROR
            ERROR = "搜索结果为空"
            error().exec_()
        
            
    def clearLayout(self, layout):
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() 
            if widget:
                widget.deleteLater()  
            else:
                self.clearLayout(item.layout()) 
                
    
    def getPackName(self, file_path):
        
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(Producer.route.resourcePath(file_path),"r") as zip:
                with zip.open("data.json") as file:
                    data = json.load(file)
                    return(data.get("pack_name"))
                
        elif file_path.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                return(data.get("pack_name"))
                
        
    def afterAdd(self):
        
        def addFiletoFolder():
            
            file_path = filedialog.askopenfilename(
                title="选择文件",
                filetypes=[("Zip Files", "*.zip")])
            
            if not file_path:
                return
            
            target_folder = Producer.route.resourcePath("mader/zips/")
            
            file_name = os.path.basename(file_path)
            
            target_file_path = os.path.join(target_folder, file_name)
            
            shutil.copy(file_path, target_file_path)

        root = tkinter.Tk()
        root.withdraw()

        addFiletoFolder()
        self.afterClick()
        
    
    def afterExport(self, button_number):
        
        global ERROR
        for name in self.names:
            if name[0] == button_number:
                file = Producer.route.resourcePath(f"mader/zips/{name[1]}")
                
        # 指定的zip文件路径
        source_zip_file = file

        # 打开文件对话框，让用户选择目标文件夹
        target_folder = filedialog.askdirectory(title="选择文件夹")
        if not target_folder:
            return

        # 构造目标文件路径
        target_file_path = os.path.join(target_folder, os.path.basename(source_zip_file))

        # 检查目标路径是否已经存在同名文件
        if os.path.exists(target_file_path):
            ERROR = f"目标文件夹已存在同名文件"
            error().exec_()
            return
        
        # 复制文件
        try:
            shutil.copy(source_zip_file, target_file_path)
            
        except Exception as e:
            ERROR = f"导出文件时出错：{e}"
            error().exec_()
            
        
    def afterNew(self):

        # 创建一个临时目录，用于存放文件
        temp_dir = Producer.resourcePath("temp")
        os.makedirs(temp_dir, exist_ok=True)

        # 创建 stations 文件夹
        stations_dir = os.path.join(temp_dir, "stations")
        os.makedirs(stations_dir, exist_ok=True)

        # 创建 dont_delete.txt 文件
        dont_delete_file = os.path.join(stations_dir, "dont_delete.txt")
        with open(dont_delete_file, "w") as f:
            pass  # 创建一个空白文件
        
        # 创建 map 文件夹
        map = os.path.join(temp_dir, "map")
        os.makedirs(map, exist_ok=True)
        
        # 创建 dont_delete.txt 文件
        dont_delete_file = os.path.join(map, "dont_delete.txt")
        with open(dont_delete_file, "w") as f:
            pass  # 创建一个空白文件

        # 创建 data.json 文件并写入内容
        data_json_file = os.path.join(temp_dir, "data.json")
        
        while True:
            if os.path.exists("mader/zips/Data{}.zip".format(self.num)):
                self.num += 1
            else:
                data = {
                    "pack_name": f"新建资源包{self.num}",
                    "uuid": f"{uuid.uuid4()}",
                    "routes_EN": ["Empty0"],
                    "routes_CN": {"未知线路0":"Empty0"},
                    "above": {"Empty0": "开往 None 方向"},
                    "below": {"Empty0": "开往 None 方向"},
                    "time": {"Empty0": "None"},
                    "color": {"Empty0": "rgb(100,100,100)"},
                    "branch_lines": [],
                    "direct_lines":[
                        ["None", "开往 None 方向"]
                        ],
                    "lines":{
                        "Line_Empty0": {
                            "None": [[0],"未知站点","暂无"]
                            }
                        }
                    }
                break
        
        with open(data_json_file, "w") as f:
            json.dump(data, f, indent=4)

        # 创建压缩包
        zip_file_name = Producer.resourcePath("mader/zips/Data{}.zip".format(self.num))
        
        with zipfile.ZipFile(zip_file_name, "w") as zipf:
            # 将 data.json 文件添加到压缩包
            zipf.write(data_json_file, arcname="data.json")
            # 将 stations 文件夹及其内容添加到压缩包
            for root, dirs, files in os.walk(stations_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname=arcname)
            # 将 map 文件夹及其内容添加到压缩包
            for root, dirs, files in os.walk(map):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname=arcname)

        # 清理临时目录
        shutil.rmtree(temp_dir)
        
        self.afterClick()
        
        
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
        
        

class sure(QtWidgets.QDialog):
    
    def __init__(self):

        ctypes.windll.user32.MessageBeep(0x00000010)
        
        super().__init__()
        self.sureDialog = uic.loadUi(Producer.route.resourcePath("window/ui/sure.ui"), self)
        
        self.sureDialog.que.setText("您确定要删除资源包？删除后的资源包将永久丢失")
        
        self.sureDialog.yes.clicked.connect(self.accept)
        self.sureDialog.cancel.clicked.connect(self.reject)
        
    def closeEvent(self, event):
        event.ignore()
        self.sureDialog.deleteLater()