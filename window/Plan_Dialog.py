import ctypes
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from window import Searched_of_Search_Dialog
import Plan, Producer, window.Plan_Error as Plan_Error, window.Searched_of_Start_Dialog as Searched_of_Start_Dialog, window.Searched_of_End_Dialog as Searched_of_End_Dialog, window.Search_Plan_Dialog as Search_Plan_Dialog
from window import Searched_of_Route_Dialog,Plan_View_Dialog,Main


DIRECTION = None
NAME = None
ERROR = None
START_DATA = None
END_DATA = None
RESULT = None

class plan_dialog(QtWidgets.QDialog):
    
    def __init__(self):
        
        super().__init__()
        self.planDialog = uic.loadUi(Producer.route.resourcePath("window/ui/plan_dialog.ui"), self)
        
        self.planDialog.search.clicked.connect(self.afterClick)
        self.planDialog.searchStart.clicked.connect(self.searchStartStation)
        self.planDialog.searchEnd.clicked.connect(self.searchEndStation)
        self.planDialog.mode.clicked.connect(self.changeMode)
        global END_DATA, START_DATA
        
        if Searched_of_Start_Dialog.STATION != None:
            self.planDialog.startText.setText(Searched_of_Start_Dialog.STATION)
            Searched_of_Start_Dialog.STATION = None
        elif Searched_of_End_Dialog.START_DATA != None:
            self.planDialog.startText.setText(Searched_of_End_Dialog.START_DATA)
            Searched_of_End_Dialog.START_DATA = None
            START_DATA = None
        elif Searched_of_Search_Dialog.STATION_START != None:
            self.planDialog.startText.setText(Searched_of_Search_Dialog.STATION_START)
            Searched_of_Search_Dialog.STATION_START = None
        elif Searched_of_Route_Dialog.STATION_START != None:
            self.planDialog.startText.setText(Searched_of_Route_Dialog.STATION_START)
            Searched_of_Route_Dialog.STATION_START = None
        
        if Searched_of_End_Dialog.STATION != None:
            self.planDialog.endText.setText(Searched_of_End_Dialog.STATION)
            Searched_of_End_Dialog.STATION = None
        elif Searched_of_Start_Dialog.END_DATA != None:
            self.planDialog.endText.setText(Searched_of_Start_Dialog.END_DATA)
            Searched_of_Start_Dialog.END_DATA = None
            END_DATA = None
        elif Searched_of_Search_Dialog.STATION_END != None:
            self.planDialog.endText.setText(Searched_of_Search_Dialog.STATION_END)
            Searched_of_Search_Dialog.STATION_END = None
        elif Searched_of_Route_Dialog.STATION_END != None:
            self.planDialog.endText.setText(Searched_of_Route_Dialog.STATION_END)
            Searched_of_Route_Dialog.STATION_END = None
        
            
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
        
        # 检查输入
        if Producer.route.begin(Start,End) != Producer.passCode.PASS001:
            # 创建一个错误消息框
            global ERROR
            ERROR = Producer.route.begin(Start,End)
            errorWindow = Plan_Error.error()
            errorWindow.show()
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
                Plan_View_Dialog.planView().show()

            # 位于不同线路上
            elif Producer.route.judgeLine(start_line_list,end_line_list)[0] == Producer.passCode.PASS003:
                result_list = Plan.plan.resultDifferentRoute(start_line_list,end_line_list,start_line_and_nummber,end_line_and_nummber)
                RESULT = result_list
                Plan_View_Dialog.planView().show()
                
    def searchStartStation(self):
        
        global DIRECTION, END_DATA
        DIRECTION = "Start"
        END_DATA = self.planDialog.endText.text()
        searchStart = Search_Plan_Dialog.search_plan_dialog()
        searchStart.show()
        
        
    def searchEndStation(self):
        
        global DIRECTION, START_DATA
        DIRECTION = "End"
        START_DATA = self.planDialog.startText.text()
        searchEnd = Search_Plan_Dialog.search_plan_dialog()
        searchEnd.show()
        
        
    def changeMode(self):
        
        global ERROR, END_DATA, START_DATA
        ERROR = "请注意在切换模式时，已输入的所有内容将会消失！"
        START_DATA = None
        END_DATA = None
        
        if self.planDialog.mode.text() == "选择模式":
            errorWindow = Plan_Error.error()
            errorWindow.show()
            ctypes.windll.user32.MessageBeep(0x00000010)
            self.planDialog.mode.setText("手写模式")
            self.planDialog.searchStart.setDisabled(True)
            self.planDialog.searchEnd.setDisabled(True)
            self.planDialog.startText.setReadOnly(False)
            self.planDialog.endText.setReadOnly(False)
            self.planDialog.startText.setText("")
            self.planDialog.endText.setText("")
        
        elif self.planDialog.mode.text() == "手写模式":
            errorWindow = Plan_Error.error()
            errorWindow.show()
            ctypes.windll.user32.MessageBeep(0x00000010)
            self.planDialog.mode.setText("选择模式")
            self.planDialog.searchStart.setDisabled(False)
            self.planDialog.searchEnd.setDisabled(False)
            self.planDialog.startText.setReadOnly(True)
            self.planDialog.endText.setReadOnly(True)
            self.planDialog.startText.setText("")
            self.planDialog.endText.setText("")
            
            
    def closeEvent(self, event):
        Main.JUDGE = False  
        for window in QApplication.topLevelWidgets():
            if window.objectName() != "Main":
                window.deleteLater()
        event.accept()