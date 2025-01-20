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
        station_name.append(f"{value[-1]} | {Producer.ruleText.betterEnglish(name)}")

def fuzzy_search(query, choices):
    
    results = [choice for choice in choices if query.lower() in choice.lower()]
    
    if not results:
        return("未找到匹配项，请检查输入或尝试其他查询")
                
    return results