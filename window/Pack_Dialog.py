import hashlib
import importlib
import json
import os
import shutil
from tkinter import filedialog
import tkinter
import zipfile
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QApplication, QHBoxLayout, QFrame, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import Producer
import Station_Search
from window import Pack_Error, Sure_Json_Pack
import window.Main as Main
import window.Sure_Delete_Pack as Sure_Delete_Pack


KEYED = ""
NAME = None
ERROR = None

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class pack_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.packDialog = uic.loadUi(Producer.route.resourcePath("window/ui/pack_dialog.ui"), self)
        
        self.packDialog.get.clicked.connect(self.afterClick)
        self.packDialog.add.clicked.connect(self.afterAdd)
        
        #首先执行的命令
        if Sure_Delete_Pack.KEYED != None:
            self.packDialog.searchText.setText(Sure_Delete_Pack.KEYED)
        
        self.afterClick()
        
    def afterClick(self):

        self.clearLayout(self.pack_layout)
        
        files_name_list = []
        for filename in os.listdir(Producer.route.resourcePath("pack/")):
            file_path = os.path.join(Producer.route.resourcePath("pack/"), filename)
            if os.path.isfile(file_path):
                files_name_list.append(filename)
                
        query = self.packDialog.searchText.text()
        result = Station_Search.fuzzy_search(query, files_name_list)
        
        if isinstance(result, list):
            
            btn_number = 0
            self.buttons = {}
            self.packs = {}
            self.names = []
            
            self.pack_layout.setAlignment(Qt.AlignTop)
            head_layout = QVBoxLayout()
            self.pack_layout.addLayout(head_layout)
            
            pack = QLabel(f"Pack{btn_number}")
            pack.setFont(QFont("黑体", 12))
            pack.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
            pack.setAlignment(Qt.AlignCenter)
            pack.setStyleSheet("""
            QLabel {
                color: red;
            }
            """)
            head_layout.addWidget(pack, 0)
            
            horizontal_line = QFrame()
            horizontal_line.setFrameShape(QFrame.HLine)
            horizontal_line.setFrameShadow(QFrame.Plain)
            horizontal_line.setLineWidth(2)
            horizontal_line.setStyleSheet("color: gray;")
            horizontal_line.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed))
            head_layout.addWidget(horizontal_line, 1)
            
            for pack_name in files_name_list:
                
                if self.getUUID(Producer.route.resourcePath(f"pack/{pack_name}")) == self.getUUID(Producer.route.resourcePath("data/Data.py")):
                    pack.setText(f"当前使用的资源包是 {self.getPackName(Producer.route.resourcePath(f"pack/{pack_name}"))}")  
                    break
                else:
                    pack.setText("未使用任何资源包")
                    
            for pack_name in result:
                
                if self.getUUID(Producer.route.resourcePath(f"pack/{pack_name}")) != self.getUUID(Producer.route.resourcePath("data/Data.py")):
                        
                    every_layout = QHBoxLayout()
                    self.pack_layout.addLayout(every_layout, 2)
                    
                    pack = QPushButton(f"Pack{btn_number}")
                    pack.setText(self.getPackName(Producer.route.resourcePath(f"pack/{pack_name}")))  
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
                    self.packs[btn_number] = pack
                    self.names.append([btn_number, pack_name])
                    
                    button = QPushButton(f"Button{btn_number}")
                    button.setText("删除")
                    button.setFont(QFont("黑体", 12))
                    button.setMinimumSize(60, 30)  
                    button.setStyleSheet("""
                    QPushButton {
                        border: 2px solid gray; 
                        background-color: white; 
                        border-radius: 10px; 
                        color: red;
                    }
                    QPushButton:hover {
                        background-color: rgb(209, 209, 209); 
                    }
                    QPushButton:pressed {
                        background-color: rgb(190, 190, 190); 
                        border: 2px solid #33373E; 
                    }
                    """)
                    every_layout.addWidget(button)  
                    
                    button.clicked.connect(lambda checked, btn=btn_number: self.afterDeleteClick(btn))
                    self.buttons[btn_number] = button
                    self.names.append([btn_number, pack_name])
                    
                    every_layout.setStretch(0,618)
                    every_layout.setStretch(1,100)
                    
                    btn_number = btn_number + 1
                
        else:
            
            self.names = []
            
            self.pack_layout.setAlignment(Qt.AlignCenter)
            
            p_text = QLabel()
            p_text.setText("未找到资源包，请检查输入或尝试其他查询")  
            p_text.setFont(QFont("黑体", 12))
            p_text.setAlignment(Qt.AlignCenter) 
            p_text.setMinimumSize(60, 30)  
            self.pack_layout.addWidget(p_text)  
    
    
    def getFileMd5(self, file_path):
        
        with open(file_path, 'rb') as f:
            md5 = hashlib.md5()
            while True:
                data = f.read(4096)
                if not data:
                    break
                md5.update(data)
                
        return md5.hexdigest()
    
        
    def afterButtonClick(self, button_number):
        
        for name in self.names:
            if name[0] == button_number:
                file = Producer.route.resourcePath(f"pack/{name[1]}")
                
        if file.endswith(".zip"):
            Sure_Json_Pack.TEXT = "您确定要更换资源包？如确定窗口将会重启"
            Sure_Json_Pack.BTN = button_number
            Sure_Json_Pack.sure().show()
                
    
    def afterDeleteClick(self, button_number):
        
        self.afterClick()
        if len(self.names) != 0:
            Sure_Delete_Pack.KEYED = None
            global KEYED
            KEYED = self.packDialog.searchText.text()
            
            Sure_Delete_Pack.TEXT = "您确定要删除资源包？删除后的资源包将永久丢失"
            Sure_Delete_Pack.BTN = button_number
            Sure_Delete_Pack.sure().show()
        
        else:
            global ERROR
            ERROR = "搜索结果为空"
            Pack_Error.error().show()
        
            
    def clearLayout(self, layout):
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() 
            if widget:
                widget.deleteLater()  
            else:
                self.clearLayout(item.layout()) 
                
    
    def getUUID(self, file_path):
        
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(Producer.route.resourcePath(file_path),"r") as zip:
                with zip.open("data.json") as file:
                    data = json.load(file)
                    return(data.get("uuid"))
        elif file_path.endswith(".py"):
            file = load(os.path.basename(file_path), file_path)
            return(file.UUID)
        
    def getPackName(self, file_path):
        
        if file_path.endswith(".zip"):
            with zipfile.ZipFile(Producer.route.resourcePath(file_path),"r") as zip:
                with zip.open("data.json") as file:
                    data = json.load(file)
                    return(data.get("pack_name"))
        elif file_path.endswith(".py"):
            file = load(os.path.basename(file_path), file_path)
            return(file.NAME)
                
    def closeEvent(self, event):
        Main.JUDGE = False  
        for window in QApplication.topLevelWidgets():
            if window.objectName() != "Main":
                window.deleteLater()
        event.accept()
        
    def afterAdd(self):

        def addFiletoFolder():
            
            file_path = filedialog.askopenfilename(
                title="选择文件",
                filetypes=[("Zip Files", "*.zip")])
            
            if not file_path:
                return
            
            target_folder = Producer.route.resourcePath(Producer.route.resourcePath("pack/"))
            
            file_name = os.path.basename(file_path)
            
            target_file_path = os.path.join(target_folder, file_name)
            
            shutil.copy(file_path, target_file_path)

        root = tkinter.Tk()
        root.withdraw() 

        addFiletoFolder()
        self.afterClick()
