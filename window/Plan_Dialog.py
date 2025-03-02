import ctypes
import itertools
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from window import Searched_of_Search_Dialog
import Plan, Producer, window.Searched_of_Start_Dialog as Searched_of_Start_Dialog, window.Searched_of_End_Dialog as Searched_of_End_Dialog, window.Search_Plan_Dialog as Search_Plan_Dialog
from window import Searched_of_Route_Dialog,Plan_View_Dialog,Main


DIRECTION = None
ERROR = None
RESULT = None

class plan_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.planDialog = uic.loadUi(Producer.route.resourcePath("window/ui/plan_dialog.ui"), self)
        
        self.planDialog.search.clicked.connect(self.afterClick)
        self.planDialog.searchStart.clicked.connect(self.searchStartStation)
        self.planDialog.searchEnd.clicked.connect(self.searchEndStation)
        self.planDialog.mode.clicked.connect(self.changeMode)
        self.setObjectName("Plan")
        
        for window in QApplication.topLevelWidgets():
            if window.objectName() not in ["Main", "Plan"]:
                window.deleteLater()
        
            
    def fillAir(self, data):
        
        if data[1] == "Start":
            self.planDialog.startText.setText(data[0])
            
        elif data[1] == "End":
            self.planDialog.endText.setText(data[0])
            
            
    def afterClick(self):
        
        global RESULT
        
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
        
        self.planDialog.startText.setStyleSheet(passCode)
        self.planDialog.startText.setFont(QFont("黑体", 12))
        self.planDialog.endText.setStyleSheet(passCode)
        self.planDialog.endText.setFont(QFont("黑体", 12))
        
        Start = self.planDialog.startText.text()
        End = self.planDialog.endText.text()
        
        if Producer.route.begin(Start,End) != Producer.passCode.PASS001:
            if Producer.route.begin(Start.replace(" ","1tc1"),End) == Producer.passCode.PASS001:
                Start = Start.replace(" ","1tc1")
            if Producer.route.begin(Start,End.replace(" ","1tc1")) == Producer.passCode.PASS001:
                End = End.replace(" ","1tc1")
            if Producer.route.begin(Start.replace(" ","1tc1"),End.replace(" ","1tc1")) == Producer.passCode.PASS001:
                Start = Start.replace(" ","1tc1")
                End = End.replace(" ","1tc1")
                
        # 检查输入
        if Producer.route.begin(Start,End) != Producer.passCode.PASS001:
            # 创建一个错误消息框
            global ERROR
            ERROR = Producer.route.begin(Start,End)
            errorWindow = error()
            errorWindow.exec_()
            ctypes.windll.user32.MessageBeep(0x00000010)
            
            if Producer.route.begin(Start,End) == Producer.errorCode.ERROR001:
                self.planDialog.startText.setStyleSheet(errorCode)
                self.planDialog.startText.setFont(QFont("黑体", 12))
                self.planDialog.endText.setStyleSheet(errorCode)
                self.planDialog.endText.setFont(QFont("黑体", 12))
                
            elif Producer.route.begin(Start,End) == Producer.errorCode.ERROR002:
                self.planDialog.endText.setStyleSheet(errorCode)
                self.planDialog.endText.setFont(QFont("黑体", 12))
                
            elif Producer.route.begin(Start,End) == Producer.errorCode.ERROR003:
                self.planDialog.startText.setStyleSheet(errorCode)
                self.planDialog.startText.setFont(QFont("黑体", 12))
                
            elif Producer.route.begin(Start,End) == Producer.errorCode.ERROR004:
                self.planDialog.startText.setStyleSheet(errorCode)
                self.planDialog.startText.setFont(QFont("黑体", 12))
                self.planDialog.endText.setStyleSheet(errorCode)
                self.planDialog.endText.setFont(QFont("黑体", 12))
                         
        else:
            # 查询起点和终点的所在线路
            start_line_list = Producer.route.stationRoute(Start,End)[0]
            end_line_list = Producer.route.stationRoute(Start,End)[1]
            start_line_and_nummber = Producer.route.stationRoute(Start,End)[2]
            end_line_and_nummber = Producer.route.stationRoute(Start,End)[3]

            # 位于同一线路上
            if Producer.route.judgeLine(start_line_list,end_line_list)[0] == Producer.passCode.PASS002:
                result_list = Plan.plan.resultSameRoute(start_line_list,end_line_list,start_line_and_nummber,end_line_and_nummber)               
                RESULT = result_list
                Plan_View_Dialog.planView().exec_()

            # 位于不同线路上
            elif Producer.route.judgeLine(start_line_list,end_line_list)[0] == Producer.passCode.PASS003:
                result_list = Plan.plan.resultDifferentRoute(start_line_list,end_line_list,start_line_and_nummber,end_line_and_nummber)
                RESULT = result_list
                Plan_View_Dialog.planView().exec_()
                
    def searchStartStation(self):
        
        global DIRECTION
        DIRECTION = "Start"
        searchStart = Search_Plan_Dialog.search_plan_dialog(function=self.judge)
        searchStart.exec_()
        
        
    def searchEndStation(self):
        
        global DIRECTION
        DIRECTION = "End"
        searchEnd = Search_Plan_Dialog.search_plan_dialog(function=self.judge)
        searchEnd.exec_()
        
        
    def changeMode(self):
        
        global ERROR
        ERROR = "请注意在切换模式时，已输入的所有内容将会消失！"
        
        if self.planDialog.mode.text() == "选择模式":
            errorWindow = error()
            errorWindow.exec_()
            ctypes.windll.user32.MessageBeep(0x00000010)
            self.planDialog.mode.setText("手写模式")
            self.planDialog.searchStart.setDisabled(True)
            self.planDialog.searchEnd.setDisabled(True)
            self.planDialog.startText.setReadOnly(False)
            self.planDialog.endText.setReadOnly(False)
            self.planDialog.startText.setText("")
            self.planDialog.endText.setText("")
        
        elif self.planDialog.mode.text() == "手写模式":
            errorWindow = error()
            errorWindow.exec_()
            ctypes.windll.user32.MessageBeep(0x00000010)
            self.planDialog.mode.setText("选择模式")
            self.planDialog.searchStart.setDisabled(False)
            self.planDialog.searchEnd.setDisabled(False)
            self.planDialog.startText.setReadOnly(True)
            self.planDialog.endText.setReadOnly(True)
            self.planDialog.startText.setText("")
            self.planDialog.endText.setText("")
            
            
    def judge(self, NAME, mode):
        
        if mode == "Start":
            searchedDialog = Searched_of_Start_Dialog.searched_start_dialog(NAME)
            searchedDialog.signal.connect(self.startSignal)
            searchedDialog.exec_()
        
        elif mode == "End":
            searchedDialog = Searched_of_End_Dialog.searched_end_dialog(NAME)
            searchedDialog.signal.connect(self.endSignal)
            searchedDialog.exec_()
            
    
    def startSignal(self, data):
        
        self.planDialog.startText.setText(data)
        
        
    def endSignal(self, data):
        
        self.planDialog.endText.setText(data)
            
            
    def closeEvent(self, event):
        event.accept()
        
        
        
class error(QtWidgets.QDialog):
    
    def __init__(self):
        
        global ERROR

        super().__init__()
        self.errorDialog = uic.loadUi(Producer.route.resourcePath("window/ui/error.ui"), self)
        
        self.errorDialog.error.setText(ERROR)