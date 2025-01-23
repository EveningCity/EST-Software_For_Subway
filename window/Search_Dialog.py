import itertools
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

import Producer
import window.Searched_of_Search_Dialog as Searched_of_Search_Dialog, Station_Search, window.Main as Main


NAME = None

class search_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        self.num = 0
        
        super().__init__()
        self.searchDialog = uic.loadUi(Producer.route.resourcePath("window/ui/search_dialog.ui"), self)
        
        self.searchDialog.pushButton.clicked.connect(self.afterClick)
        
        self.p_layout = QVBoxLayout()  
        self.searchDialog.scrollArea.widget().setLayout(self.p_layout)  
        
        #首先执行的命令
        self.afterClick()
            
        
    def afterClick(self):
        
        query = self.searchDialog.searchText.text()
        result = Station_Search.fuzzy_search(query, [item[2] for item in Station_Search.station_name])
        res_lst = []
        
        for res,lst in itertools.product(result, Station_Search.station_name):
            
            if res in lst:
                res_lst.append(lst)
        
        if self.num != 0:
            self.clearLayout(self.p_layout)
            
        self.num = self.num + 1
        
        if isinstance(result, list):
            
            btn_number = 0
            self.buttons = {}
            self.names = []
            
            self.p_layout.setAlignment(Qt.AlignTop)
            
            for station_name in res_lst:
                
                button = QPushButton(f"Button{btn_number}")
                button.setText(station_name[2])  
                button.setFont(QFont("等线", 12))
                button.setMinimumSize(60, 30)  
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
                self.p_layout.addWidget(button)  
                
                button.clicked.connect(lambda checked, btn=btn_number: self.afterButtonClick(btn))
                self.buttons[btn_number] = button
                self.names.append([btn_number, station_name])
                
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
        
        self.searchedDialog = Searched_of_Search_Dialog.searched_dialog()
        self.searchedDialog.show()
        
            
    def clearLayout(self, layout):
        
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget() 
            if widget:
                widget.deleteLater()  
            else:
                self.clearLayout(item.layout())  
           
                
    def closeEvent(self, event):
        Main.JUDGE = False  
        for window in QApplication.topLevelWidgets():
            if window.objectName() != "Main":
                window.deleteLater()
        event.accept()