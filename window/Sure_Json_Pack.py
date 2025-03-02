import ast
import ctypes
import json
import os
import shutil
import subprocess
import sys
import zipfile
from PyQt5 import QtWidgets, uic

import Producer
from window import Main, Pack_Dialog

TEXT = None
BTN = None

class sure(QtWidgets.QDialog):
    
    def __init__(self):

        ctypes.windll.user32.MessageBeep(0x00000010)
        
        super().__init__()
        self.sureDialog = uic.loadUi(Producer.route.resourcePath("window/ui/sure.ui"), self)
        
        self.sureDialog.que.setText(TEXT)
        
        self.sureDialog.yes.clicked.connect(self.ifYes)
        self.sureDialog.cancel.clicked.connect(self.ifCancel)
        
    def ifYes(self):
        global BTN
        
        for filename in os.listdir(Producer.route.resourcePath("data/stations/")):
            file_path = os.path.join(Producer.route.resourcePath("data/stations/"), filename)
            
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # 删除文件或链接
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # 删除子文件夹
                    
        for name in Pack_Dialog.pack_dialog().names:
            if name[0] == BTN:
                
                with zipfile.ZipFile(Producer.route.resourcePath(f"pack/{name[1]}"),"r") as zip:
                    
                    with zip.open("data.json") as file:
                        data = json.load(file)
                        
                    target_json_path = os.path.join(Producer.route.resourcePath("data/"), "content.json")
                    with open(target_json_path, "w", encoding="utf-8") as output_file:
                        json.dump(data, output_file, indent=4, ensure_ascii=False)
                    
                    all_files = zip.infolist()
                    for fi in all_files:
                        fi_name = fi.filename
                        if fi_name.startswith("stations/") and fi_name.lower().endswith((".png",".jpg",".jpeg",".txt")):
                            temp_path = zip.extract(fi, path=Producer.route.resourcePath("data/stations/"))
                            shutil.move(temp_path, os.path.join(Producer.route.resourcePath("data/stations/"), os.path.basename(fi.filename)))
                            shutil.rmtree(Producer.route.resourcePath("data/stations/stations/"))
                        
                first_file = Producer.route.resourcePath(self.changeFirst(Producer.route.resourcePath("data/content.json")))
                src_file = Producer.route.resourcePath(self.changeFile(Producer.route.resourcePath(first_file)))
                dst_folder = Producer.route.resourcePath("")
                dst_file = os.path.join(dst_folder, Producer.route.resourcePath("data/Data.py"))

                shutil.copy(src_file, dst_file)
                os.remove(first_file)
                os.remove(src_file)
                                
                Main.JUDGE = False  
                python = sys.executable
                subprocess.Popen([python] + sys.argv)
                sys.exit(0)
        
    def ifCancel(self):
        self.sureDialog.deleteLater()
    
    def changeFirst(self, file_path):
                
        with open(file_path, 'rb') as file:
            dict = json.load(file)
            self.lines = dict.get("lines")
            station = {}
    
            for dict_name, inner_dict in self.lines.items():
                for key, value in inner_dict.items():
                    # 提取描述字符串
                    name = value[1]
                    description = value[2]
                    
                    # 如果键已经存在于station中
                    if key in station:
                        # 将当前字典名称添加到列表中（避免重复）
                        if dict_name not in station[key][0]:
                            station[key][0].append(dict_name.replace("Line_",""))
                    else:
                        # 如果键不存在于station中，创建新的条目
                        station[key] = [[dict_name.replace("Line_","")], name, description]
                        
            with open(os.path.join(Producer.route.resourcePath("data/"),os.path.basename(file_path)), "r", encoding="utf-8") as file_next:
                existing_data = json.load(file_next)

            existing_data["stations"] = station

            with open(os.path.join(Producer.route.resourcePath("data/"),os.path.basename(file_path)), "w", encoding="utf-8") as file_then:
                json.dump(existing_data, file_then, ensure_ascii=False, indent=4)
        
            path = os.path.join(Producer.route.resourcePath("data/"), os.path.basename(file_path))
            
        return(path)

    
    def changeFile(self, file_path):
        
        with open(file_path, 'rb') as file:
            dict = json.load(file)
            self.lines = dict.get("lines")
            
            code = """
NAME = "{}"
UUID = "{}"
ALL_LINE_LIST = {}
ALL_LINE_DICT = {}
ABOVE_ZERO_DIRECTION = {}
BELOW_ZERO_DIRECTION = {}
TIME_DICT = {}
RGB_DICT = {}
BRANCH_LINE_LIST = {}
DIRECT_LINE_LIST = {}
            """.format(
                dict.get("pack_name"),
                dict.get("uuid"),
                dict.get("routes_EN"),
                dict.get("routes_CN"),
                dict.get("above"),
                dict.get("below"),
                dict.get("time"),
                dict.get("color"),
                dict.get("branch_lines"),
                dict.get("direct_lines"))
            
            for every_class,line_station in dict.get("lines").items():
                line_code = """
class {}:
                """.format(every_class)
                code += line_code
                
                for station_name, class_station in line_station.items():
                    station_code = """
    {} = {}
                    """.format(
                        station_name.replace('"',""),
                        Producer.route.flatten([every_class.replace("Line_",""), self.convertToNumbers(str(class_station[0]).replace("[","").replace("]",""))]))
                    code += station_code
                
            code += """
class Station:
            """
            
            description_list = []
            for stations, data in dict.get("stations").items():
                code_list = []
                first_code = f"{stations}"
                for servel_data in data[0]:
                    every_data = str(self.fromRouteAndNameToData(f"Line_{servel_data}", stations))
                    code_list.append(every_data)
                code_list.append(data[1])
                description_list.append([first_code ,data[-1]])
                second_code = """
    {} = {}
                """.format(first_code,self.listToString(code_list))
                code += second_code
                
            third_code = """
DESCRIPTION = {}
            """.format(description_list)
            
            code += third_code
            
            path = os.path.join(Producer.route.resourcePath("data/"), os.path.basename(file_path).replace(".json", ".py"))
            with open(path, 'w', encoding='utf-8') as file:
                file.write(code)
        
        return(path)
                        
    def fromRouteAndNameToData(self, dict_name, key):

        if dict_name in self.lines:
            target_dict = self.lines[dict_name]
            # 检查键是否存在于目标字典中
            if key in target_dict:
                return f"{dict_name}.{key}"
                         
    def stringToList(self, stringified_list):

        result = ast.literal_eval(stringified_list)
        if isinstance(result, list):
            return result

    def convertToNumbers(self, num_str):
        try:
            # 尝试直接转换为整数（如果字符串是单个数字）
            return [int(num_str)]
        except ValueError:
            # 如果包含逗号，分割并转换为整数列表
            return [int(num) for num in num_str.split(",")]
        
    def listToString(self, lst):
         # 将列表转换为字符串，去掉所有引号，唯独最后一个元素的引号保留
        result = []
        for i, item in enumerate(lst):
            if i == len(lst) - 1:
                result.append(f'"{item}"')
            else:
                result.append(str(item).strip('"'))
        
        string = '[' + ",".join(result) + ']'
        return string

    def closeEvent(self, event):
        self.sureDialog.deleteLater()
        event.accept()