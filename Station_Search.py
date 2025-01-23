import importlib
import Producer

import inspect


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

Data = load("Data",Producer.route.resourcePath("data/Data.py"))

station_name = []

for name, value in inspect.getmembers(Data.Station, lambda a: not(inspect.isroutine(a))):
    
    if not name.startswith('__'):
        name_list = [value[-1],name]
        
        if "1tc1" in name or "1tc1" in value[-1]:
            
            if "1te1" in name:
                list_EN = name.split("1te1")
                name_list.insert(3, list_EN[-1])
            else:
                name_list.insert(3, " ")
                
            if "1tc1" in value[-1]:
                list_CN = value[-1].split("1tc1")
                name_list.insert(2, list_CN[-1])
            else:
                name_list.insert(2, " ")
        
        station_name.append(name_list)


for servel in station_name:
    if len(servel) == 2:
        servel.insert(2, f"{Producer.ruleText.betterChinese(servel[0])} | {Producer.ruleText.betterEnglish(servel[1])}")
    else: 
        servel.insert(2, f"{Producer.ruleText.betterChinese(servel[0].split('1tc1')[0])} {Producer.ruleText.betterChinese(servel[2])} | {Producer.ruleText.betterEnglish(servel[1].split('1te1')[0])} ({Producer.ruleText.betterEnglish(servel[3])})")


def fuzzy_search(query, choices):
    
    results = [choice for choice in choices if query.lower() in choice.lower()]
    
    if not results:
        return("未找到匹配项，请检查输入或尝试其他查询")
                
    return results