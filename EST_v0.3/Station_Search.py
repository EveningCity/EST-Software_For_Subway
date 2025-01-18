import Data
import Producer

import inspect

station_name = []

for name, value in inspect.getmembers(Data.Station, lambda a: not(inspect.isroutine(a))):
    
    if not name.startswith('__'):
        station_name.append(f"{value[-1]} | {Producer.ruleText.betterEnglish(name)}")

def fuzzy_search(query, choices):
    
    results = [choice for choice in choices if query.lower() in choice.lower()]
    
    if not results:
        return("未找到匹配项，请检查输入或尝试其他查询")
                
    return results