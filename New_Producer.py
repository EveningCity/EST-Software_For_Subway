

import re


def formatLineList(Lines, routes_CN):
    """将多条线路转换为汉字格式"""
    
    lines = []
    for Line in Lines:
        for item in routes_CN.items():
            if Line == item[1]:
                lines.append(item[0])
    return (lines)


def formatLine(Line, routes_CN):
    """将线路转换为汉字格式"""
        
    for item in routes_CN.items():
        if Line == item[1]:
            return item[0]
    

def colorRoute(RouteText, color):
    "根据线路编号返回RGB值"
        
    for Route in color.keys():
        
        if Route == RouteText:
            return(color[Route])
        
        
def describeRoute(RouteText, time):
    "根据线路编号返回线路描述"
    
    for Route in time.keys():
        
        if Route == RouteText:
            return(time[Route])
    
    
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