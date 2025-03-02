import importlib.util
import itertools
import os
import sys
import importlib
import re


def resourcePath(relative_path):
        """获取资源的绝对路径，适用于Dev和PyInstaller"""
        
        try:
            # PyInstaller 会创建一个临时文件夹并将路径存储在 _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

Data = load("Data",resourcePath("data/Data.py"))

station = []
# 遍历Station类的所有属性
for attribute in dir(Data.Station):
    # 检查属性是否是类变量（不是方法也不是私有属性）
    if not attribute.startswith('__') and not callable(
        getattr(
        Data.Station,
        attribute
        )) and not attribute.startswith('_'):
        # 将属性值添加到列表中
        station.append(
        getattr(
        Data.Station,
        attribute
        ))

station_name = []

for stations in station:
    station_name.append(stations[-1])
    
    
class ruleText:
    """字符规则"""
    
    def colorRoute(RouteText):
        "根据线路编号返回RGB值"
        
        for Route in Data.RGB_DICT.keys():
            
            if Route == RouteText:
                return(Data.RGB_DICT[Route])
        
        
    def describeRoute(RouteText):
        "根据线路编号返回线路描述"
        
        for Route in Data.TIME_DICT.keys():
            
            if Route == RouteText:
                return(Data.TIME_DICT[Route])
        
        
    def darkerColor(rgb_str):
        """将RGB值全部减小"""
        
        # 使用正则表达式找到所有数字
        numbers = re.findall(r'\d+', rgb_str)
        
        # 将找到的数字转换为整数，并减去50
        reduced_numbers = [str(max(0, int(num) - 20)) for num in numbers]
        
        # 将原字符串中的数字替换为减小后的数字
        for i, num in enumerate(numbers):
            rgb_str = rgb_str.replace(num, reduced_numbers[i], 1)  # 只替换第一次出现的数字
            
        return rgb_str
        
    
    def betterEnglish(t):
        """对英文名称进行适当的修改"""
        
        result = ""
        for i in range(len(t)):
            
            # 将当前字符添加到结果字符串中
            result += t[i]
            # 如果当前字符是小写字母，并且下一个字符是大写字母
            # 则在它们之间加上空格
            if i < len(t) - 1 and t[i].islower() and t[i + 1].isupper():
                result += " "
                
        result = result.split("1te1")[0]
        result = result.replace("1o1", " ").replace("_", " / ").replace("1te1", "").replace("1d1",".").replace("1h1","-").replace("1c1",",").replace("1n1","").replace("1q1","'").replace("1a1","&")
        return result   
    
    
    def betterChinese(t):
        """对中文名称进行适当的修改"""
        
        result = ""
        for i in range(len(t)):
            
            # 将当前字符添加到结果字符串中
            result += t[i]
            # 如果当前字符是小写字母，并且下一个字符是大写字母
            # 则在它们之间加上空格
            if i < len(t) - 1 and t[i].islower() and t[i + 1].isupper():
                result += " "
        
        result = result.split("1tc1")[0]
        result = result.replace("1o1", " ").replace("_", "/").replace("1tc1", "").replace("1h1","-").replace("1d1","·").replace("1q1","'")
        return result   
    
    
    def better(t):
        """专用改动"""

        result = t.replace("1tc1"," ")
        return result
    
    
    def planName(n):
        """将数字转换为汉字"""
        
        if not isinstance(n, int) or n < 1:
            return "请输入一个自然数"

        chinese_numerals = "零一二三四五六七八九"
        units = ["", "十", "百", "千", "万", "亿"]
        result = ""
        zero = False  # 用于处理连续的零

        # 将数字转换为汉字
        unit_index = 0
        while n > 0:
            digit = n % 10
            if digit == 0:
                if not zero:
                    zero = True
                    result = "零" + result
            else:
                zero = False
                result = chinese_numerals[digit] + units[unit_index] + result
            n //= 10
            unit_index += 1

        # 处理“一十”的情况
        if result.startswith("一十"):
            result = result[1:]

        return result        
        
    
    def formatLineList(Lines):
        """将多条线路转换为其它格式"""
        
        lines = []
        for Line in Lines:
            
            line = "".join(Line)
            
            for key in {value: key for key, value in Data.ALL_LINE_DICT.items()}.keys():
                
                if line == key:
                    lines.append({value: key for key, value in Data.ALL_LINE_DICT.items()}[key])
        
        return (lines)



    def connectWith(List):
        
        """将多个站点用"或"连接"""
        return "或".join(List)



class errorCode:
    """错误代码"""
    
    ERROR001 = "未查询到起点站和终点站"
    ERROR002 = "未查询到终点站"
    ERROR003 = "未查询到起点站"
    ERROR004 = "起点站和终点站相同"
    
    
    
class passCode:
    """正确代码"""
    
    PASS001 = "输入正确"
    PASS002 = "肯定输出"
    PASS003 = "否定输出"



class route:
    """基础模块"""
    
    def begin(Start,End):
        """数据获取模块"""
        
        while True:
            
            if End not in station_name:
                
                if Start not in station_name:
                    return(errorCode.ERROR001)
                else:
                    return(errorCode.ERROR002)
            elif Start not in station_name:
                
                if End not in station_name:
                    return(errorCode.ERROR001)
                else:
                    return(errorCode.ERROR003)
                    
            elif Start in station_name:
                if End == Start:
                    return(errorCode.ERROR004)
                    
                elif End != Start:
                    return(passCode.PASS001)
        
        
        
    def stationRoute(Start,End):
        """整合站点的线路编号"""
        
        start_line_list = []
        end_line_list = []
        
        for start in station:
            
            if start[-1] == Start:
                start_line_and_number = start[:-1]
                      
                for start_line in start_line_and_number:
                
                    start_line_list.append(start_line[0])
                
        for end in station:
            
            if end[-1] == End:
                end_line_and_number = end[:-1]
                    
                for end_line in end_line_and_number:
                    
                    end_line_list.append(end_line[0])
                    
        return([start_line_list,end_line_list,start_line_and_number,end_line_and_number])
    
    
    def stationRouteServel(StationName):
        """获取站点所在的线路列表"""
        
        line_list = []
        
        for station_name in station:
            
            if station_name[-1] == StationName:
                line_and_number = station_name[:-1]
                
                for line in line_and_number:
                    
                    line_list.append(line[0])
                
        return(route.remain(line_list))
    
    
    def stationRouteAndNumberServel(StationName):
        """获取站点的线路编号列表"""
        
        for station_name in station:
            
            if station_name[-1] == StationName:
                line_and_number = station_name[:-1]
                
        return(line_and_number)
        
        
    def getMaxNumber(Route):
        """获取一条线路中存在最大编号的编号组"""
        
        lst = []
        max_lst = []
        for servel in station:
            
            for eo in servel[:-1]:
                
                if eo[0] == Route:
                    lst.append(eo[1:])
        
        for servel_lst in lst:
            
            max_lst.append(max(servel_lst))
            
        for servel_lst in lst:
            
            if max(max_lst) in servel_lst:
                return(servel_lst)
                    
        
    def resourcePath(relative_path):
        """获取资源的绝对路径，适用于Dev和PyInstaller"""
        
        try:
            # PyInstaller 会创建一个临时文件夹并将路径存储在 _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
        
                
    def judgeLine(start_line_list,end_line_list):
        """判断是否位于同一线路上"""
        
        if set(start_line_list) & set(end_line_list):
            
            return([passCode.PASS002,"位于同一线路上"])
        
        else:
            
            return([passCode.PASS003,"不在同一线路上"])
        
        
        
    def filterStationByRoute(station_line_list):
        """寻找列表中所有线路的所有站点"""
        
        station_list = []
        
        for single, servel in itertools.product(
            station_line_list, [item[:-1] for item in station]
            ):
            if any(single == inner_item[0] for inner_item in servel):
                station_list.append(servel)
                
        return station_list
    
    
    
    def flatten(nested_list):
        """铺平嵌套列表"""
        
        flat_list = []
        stack = [nested_list]  # 使用栈来处理嵌套列表

        while stack:
            current = stack.pop()
            if isinstance(current, list):
                stack.extend(current[::-1])  # 将列表元素逆序压入栈中
            else:
                flat_list.append(current)

        return flat_list
    
    
    
    def flattenOnce(nested_list):
        """只铺平一层嵌套列表"""
        
        return([item for sublist in nested_list for item in sublist])
    
    
    
    def remain(need_list):
        """对已铺平的列表进行唯一元素求舍"""
        
        seen = set()
        result = []
        
        for item in need_list:
            
            if item not in seen:
                seen.add(item)
                result.append(item)
                
        return result
    
    
    
    def filterStr(input_list):
        """只保留列表中的字符串"""
        
        return [item for item in input_list if isinstance(item, str)]
    
    
    
    def last(list):
        """去除列表中相同的元素"""
        
        new_list = []
        
        for element in list:
            
            if element not in new_list:
                
                new_list.append(element)
                
        return(new_list)
    
    
    
    def findStationInTwoRoutes(line1_list,line2_list):
        """根据两条线路找相交的站点"""
        line1_station_list = route.filterStationByRoute(line1_list)
        line2_station_list = route.filterStationByRoute(line2_list)
        
        station_list = [item for sublist in [line1_station_list, line2_station_list] for item in sublist]
        
        # 使用字典来存储已经见过的嵌套列表
        seen = {}
        duplicates = []

        # 定义一个函数来将嵌套列表转换为可哈希的元组
        def make_hashable(lst):
            return tuple(tuple(item) for item in lst)

        # 遍历顶层列表
        for sublist in station_list:
            # 将嵌套列表转换为可哈希的元组
            key = make_hashable(sublist)
            
            # 检查是否已经见过这个嵌套列表
            if key in seen:
                duplicates.append(sublist)
            else:
                seen[key] = True
                
        return(duplicates)

    
    
    def lastOnly(nested_list):
        """去除嵌套列表中重复的嵌套列表"""
        
        # 将每个子列表转换为元组，以便可以添加到集合中
        tuple_set = set(tuple(map(tuple, sublist)) for sublist in nested_list)

        # 将集合中的元组转换回列表
        unique_nested_list = [list(map(list, tup)) for tup in tuple_set]
        return(unique_nested_list)
    
    
    
    def last(list):
        """去掉列表中重复的元素"""
        
        List = []
        for item in list:
            
            if item not in List:
                
                List.append(item)
                
        return(List)
    
    
    
    def lastDifferentListHead(list):
        """如果嵌套列表中的首项和其它嵌套列表相同，只保留一个"""
        
        List = []
        Head = []
        
        for item in list:
            
            if item not in List:
                if item[0] not in Head:
                    List.append(item)
                    Head.append(item[0])
                
        return(List)
        
        
        
    def dictDifferentFeet(list):
        """如果嵌套列表中的末项和其它嵌套列表相同，组合在一个字典中"""
        
        # 创建一个字典来存储末项相同的子列表
        grouped_dict = {}

        # 遍历嵌套列表
        for sublist in list:
            key = sublist[1]  # 末项作为键
            value = sublist[0]  # 去掉末项后的值
            if key in grouped_dict:
                grouped_dict[key].append(value)
            else:
                grouped_dict[key] = [value]
                
        return(grouped_dict)
        
        
        
    def findRouteByRouteAndnumber(A,B):
        """根据线路和编号中相同的线路找出相同的线路"""
        # 提取A和B中所有嵌套列表的首项
        first_items_A = [sublist[0] for sublist in A]
        first_items_B = [sublist[0] for sublist in B]

        # 找出共有的首项
        common_first_items = list(set(first_items_A) & set(first_items_B))

        # 将结果转换为嵌套列表的形式
        result = [[item] for item in common_first_items]
        
        return(result)
            
            
           
    def resultGet(station_line_list,station_line_and_number):
        """根据线路找编号"""
        
        return([sublist[1:] for sublist in station_line_and_number if sublist[0] in station_line_list])
    
    
    
    def findPositions(list, element):
        """寻找元素在列表中的位置，返回所有位置的列表"""
        
        return [i for i, x in enumerate(list) if x == element]
    
    
    
    def getElementsByPositions(list, positions):
        """根据提供的位置列表找元素"""
        
        return [list[pos] for pos in positions]
         
        
        
    def findStationByRouteAndnumberList(station_line_and_number):
        """通过线路和编号的嵌套列表找到站点名称"""
        
        for sublist in station:
            
            if all(item in sublist for item in station_line_and_number):
                
                return sublist[-1]
        
    
    
    def removeOuterLayerList(nested_list):
        """如果一个嵌套列表内只有一个元素且该元素是列表，删去最外层嵌套"""
        
        # 检查列表是否只有一个元素且该元素是列表
        if len(nested_list) == 1 and isinstance(nested_list[0], list):
            return nested_list[0]
        
        else:
            return nested_list  # 如果不符合条件，返回原列表
    
    
    
    def resultPossible(Dict):
        """将字典内每个键对应的列表按键配对，得到一个包含所有可能结果的字典"""
        
        # 获取字典中的键并按顺序排序
        keys = sorted(Dict.keys())

        # 初始化结果列表
        result_list = [()]

        # 逐步构建配对结果
        for key in keys:
            current_list = Dict[key]
            # 使用 itertools.product 生成当前结果列表与当前列表的所有可能配对
            result_list = [pair + (item,) for pair in result_list for item in current_list]

        # 创建结果字典，每个配对对应一个唯一的键
        result_dict = {i: list(pair) for i, pair in enumerate(result_list, start=1)}      
              
        return(result_dict)
    
    
    
    def yesOrNotIntersectionLine(line_list_1,line_list_2):
        """判断两条线是否相交"""
        
        TRUE = 0
        
        for every_line in route.flatten(
            route.filterStr(
            route.remain(
            route.flatten(
            route.filterStationByRoute(line_list_1)
            )))):
            
            if every_line in line_list_2:
                TRUE = 1

        if TRUE == 1:
            return(1)
        
        else:
            return(0)
    
    
    
    def pairElements(list1, list2):
        """对两个列表进行两两配对"""
        
        # 创建一个空的嵌套列表来存储结果
        result = []
        
        # 使用for循环遍历list1中的每个元素
        for item1 in list1:
            # 对于list1中的每个元素，再遍历list2中的每个元素
            for item2 in list2:
                # 将配对 (item1, item2) 添加到结果列表中
                result.append([item1, item2])
        
        return(result)
    
    
    
    def fromValueToKey(dictionary, value):
        """根据字典中的值查找对应的键，并返回键的列表。
        
        param dictionary: 要搜索的字典
        param value: 要查找的值
        return: 包含所有对应键的列表
        """
        
        keys = []
        for key, values in dictionary.items():
            if value in values:
                keys.append(key)
        
        return keys
    
    
    
    def remainKeys(dictionary, keys_to_keep):
        """只保留字典里指定的键"""
        
        return {key: dictionary[key] for key in keys_to_keep if key in dictionary}
    
    
    
    def deleteSameDictValue(Dict):
        """删除一个字典内具有同值的键"""
        
        # 使用一个集合来存储已经存在的列表（转换为元组）
        seen = set()

        # 新的字典，用于存储去重后的结果
        new_dict = {}

        for key, value in Dict.items():
            # 将列表转换为元组
            value_tuple = tuple(value)
            if value_tuple not in seen:
                # 如果这个元组不在集合中，说明这个列表是唯一的
                new_dict[key] = value
                # 将元组添加到集合中
                seen.add(value_tuple)
                
        return(new_dict)
    
    
    
    def findPaths(layers):
        """专用函数，将嵌套列表中首尾相同的列表连接起来，包含所有可能性"""
        
        def dfs(layer_idx, path):
            
            if layer_idx == len(layers):
                result.append(path[:])
                return
            
            for node in layers[layer_idx]:
                path.append(node[1])
                dfs(layer_idx + 1, path)
                path.pop()
        
        result = []
        
        for start_node in layers[0]:
            
            dfs(1, [start_node[0], start_node[1]])
        
        return result
    
    
    
    def intersectionStationList(station_line_list_1,station_line_list_2):
        """两线路列表相交得出站点属性（名称除外）"""
        
        intersection_station_line_and_number = []
        
        for station_list_line_and_number_element_1,station_list_line_and_number_element_2 in itertools.product(
            route.filterStationByRoute(station_line_list_1),
            route.filterStationByRoute(station_line_list_2)):
            
            if station_list_line_and_number_element_1 == station_list_line_and_number_element_2:
                intersection_station_line_and_number.append(station_list_line_and_number_element_1)
        
        return(intersection_station_line_and_number)
    
    
    def direction(route_number, pair, distance):
                
        first_name = pair[0]
        second_name = pair[1]
        
        first_number = route.flatten(route.resultGet([route_number],route.stationRouteAndNumberServel(first_name)))
        second_number = route.flatten(route.resultGet([route_number],route.stationRouteAndNumberServel(second_name)))
            
        if len(second_number) == 1:
            # 直线
            for a, b in zip(first_number, second_number):
                    
                if a - b < 0:
                    return(Data.BELOW_ZERO_DIRECTION[route_number])
                        
                else:
                    return(Data.ABOVE_ZERO_DIRECTION[route_number])
            
        else:
            # 环线
            for a, b in zip(first_number, second_number):
                
                if abs(a - b) == distance:
                    
                    if a - b < 0:
                        return(Data.BELOW_ZERO_DIRECTION[route_number])
                        
                    else:
                        return(Data.ABOVE_ZERO_DIRECTION[route_number])