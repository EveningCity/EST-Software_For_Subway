import copy
import importlib
import itertools
import os
import sys
import Producer


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

class plan:
    """查找线路"""
    
    def resultSameRoute(start_line_list,end_line_list,start_line_and_number,end_line_and_number):
        """同线路结果"""
        
        result = {}
        direction = []
        difference_list_abs = []
        NUM = 0
        
        same_line_list = list(set(start_line_list) & set(end_line_list))
        
        for same_line in same_line_list:
            
            NUM = NUM + 1
            
            for direct_line in Data.DIRECT_LINE_LIST:
            
                if same_line in direct_line[0]:
                    
                    start_result_direct = [sublist_1[1:] for sublist_1 in start_line_and_number if sublist_1[0] in [same_line]][0]
                    end_result_direct = [sublist_2[1:] for sublist_2 in end_line_and_number if sublist_2[0] in [same_line]][0]
                    
                    direct_servel = []
                    for direct_servel_start, direct_servel_end in itertools.product(start_result_direct, end_result_direct):
                        if direct_servel_start != 0 and direct_servel_end != 0:
                            if direct_servel_start - direct_servel_end < 0:
                                direct_servel.append([direct_servel_start,direct_servel_end])
                    
                    if len(direct_servel) != 0:
                        diffs = [abs(a-b) for a,b in direct_servel]
                        min_diff = min(diffs)
                        index = diffs.index(min_diff)
                        number = abs(direct_servel[index][0] - direct_servel[index][1])
                        difference_list_abs.append(number)
                        
                    else:
                        number = abs(max(start_result_direct) - max(Producer.route.getMaxNumber(same_line))) + [x for x in end_result_direct if x != 0][0] - 1
                        difference_list_abs.append(number)
                
                else:
                    
                    start_result = [sublist_1[1:] for sublist_1 in start_line_and_number if sublist_1[0] in [same_line]]
                    end_result = [sublist_2[1:] for sublist_2 in end_line_and_number if sublist_2[0] in [same_line]]
                
                    for START,END in itertools.product(start_result,end_result):
                        difference_list = [num for num in [a - b for a,b in zip(START,END)]] # 对两个列表中的对应元素进行减法
                        difference_list_abs.append([abs(num) for num in difference_list][0])
            
            min_number = min(difference_list_abs)
            
            Start = Producer.route.findStationByRouteAndnumberList(start_line_and_number)
            End = Producer.route.findStationByRouteAndnumberList(end_line_and_number)
            
            for direct_line in Data.DIRECT_LINE_LIST:
                if same_line == direct_line[0]:
                    direction.append(direct_line[-1])
                else:
                    direction.append(Producer.route.direction(same_line, [Start, End], min_number))
            direction.append(0)
            
            line_list = [same_line, same_line]
            
            min_number_list = [min_number, 0]

            result["方案" + Producer.ruleText.planName(NUM)] = [0, min_number_list, [Start, End], line_list, [min_number], direction]
            
        return(result)
        
        
        
    def resultDifferentRoute(start_line_list,end_line_list,start_line_and_number,end_line_and_number):
        """异线路结果"""

        route_of_station_start = Producer.route.filterStr(
            Producer.route.remain(
            Producer.route.flatten(
            Producer.route.filterStationByRoute(start_line_list)
            ))) # 得到起始线路相关联的线路
        
        if set(route_of_station_start) & set(Producer.route.remain(end_line_list)):
            
            start_intersection_list = []
            end_intersection_list = []
            
            for start_line_list_element,end_line_list_element in itertools.product(
                Producer.route.filterStationByRoute(start_line_list),
                Producer.route.filterStationByRoute(end_line_list)
                ):
                
                if start_line_list_element == end_line_list_element:
                    
                    for station_line_and_number in start_line_list_element:
                        
                        if station_line_and_number[0] in Producer.route.remain(start_line_list):
                            start_intersection_list.append(station_line_and_number[0])
                            
                        if station_line_and_number[0] in Producer.route.remain(end_line_list):
                            end_intersection_list.append(station_line_and_number[0])
                            
            intersection_route_dict = {0:start_intersection_list, 1:end_intersection_list}
               
        else:  
            NUM = 0
            route_from_station_start_informal = route_of_station_start
            route_from_station_start = [[item, NUM] for item in route_of_station_start]
            
            while True:
                NUM = NUM +1
                
                #设定允许换乘的最大次数+1值：
                if NUM == 30:
                    return(None)
                
                for item in Producer.route.flatten(
                    Producer.route.filterStr(
                    Producer.route.remain(
                    Producer.route.flatten(
                    Producer.route.filterStationByRoute(route_from_station_start_informal)
                    )))):

                    route_from_station_start.append([item, NUM])
                    route_from_station_start_informal.append(item)
                
                route_from_station_start = Producer.route.lastDifferentListHead(route_from_station_start)
                route_from_station_start_informal = Producer.route.remain(route_from_station_start_informal)
                
                if set(route_from_station_start_informal) & set(end_line_list):
                    route_from_station_start_dict = Producer.route.dictDifferentFeet(route_from_station_start)
                    route_from_station_start_dict[NUM] = Producer.route.remain(end_line_list)
                    
                    route_from_station_start_dict = dict(sorted(route_from_station_start_dict.items(), key=lambda item: item[0], reverse=True))
                    # 倒序字典
                    
                    head_deled_route_from_station_start_dict = {key: value for key, value in route_from_station_start_dict.items() if key != NUM}
                    feet_deled_route_from_station_start_dict = {key: value for key, value in route_from_station_start_dict.items() if key != 0}
                    
                    break
                
                
            # 获取换乘线路
            intersection_route_dict = {}
            last_route_dict = {}
            last_route_dict[NUM] = Producer.route.remain(end_line_list)
            
            for no_head, KEY in zip(
                head_deled_route_from_station_start_dict.values(),
                feet_deled_route_from_station_start_dict.keys()
                ):
                    
                NEXT_KEY = KEY - 1
                
                for Item in no_head:
                    
                    element_list = Producer.route.flatten(
                    Producer.route.filterStr(
                    Producer.route.remain(
                    Producer.route.flatten(
                    Producer.route.filterStationByRoute([Item])
                    ))))
                    
                    element_list = [item for item in element_list if item != Item]
                
                    if set(element_list) & set(last_route_dict[KEY]):
                        
                        if KEY in intersection_route_dict:
                            intersection_route_dict[KEY].append(Item)
                            
                        elif KEY not in intersection_route_dict:
                            intersection_route_dict[KEY] = [Item]
                            
                        if NEXT_KEY in last_route_dict:
                            last_route_dict[NEXT_KEY].append(Item)
                            
                        elif NEXT_KEY not in last_route_dict:
                            last_route_dict[NEXT_KEY] = [Item]
            
            
            FINAL_KEY = NUM + 1
            
            for start_line in Producer.route.remain(start_line_list):
                
                for element in intersection_route_dict[1]:
                    
                    if element in Producer.route.flatten(
                        Producer.route.filterStr(
                        Producer.route.remain(
                        Producer.route.flatten(
                        Producer.route.filterStationByRoute([start_line])
                    )))):
                        
                        if 0 in intersection_route_dict:
                            intersection_route_dict[0].append(start_line)
                            
                        elif 0 not in intersection_route_dict:
                            intersection_route_dict[0] = Producer.route.remain([start_line])
                            
                            
            # 得出最优换乘路线，得出换乘步骤
            for end_line in Producer.route.remain(end_line_list):
                            
                for element in intersection_route_dict[NUM]:
                            
                    if element in Producer.route.flatten(
                        Producer.route.filterStr(
                        Producer.route.remain(
                        Producer.route.flatten(
                        Producer.route.filterStationByRoute([end_line])
                    )))):
                        
                        if FINAL_KEY in intersection_route_dict:
                            intersection_route_dict[FINAL_KEY].append(end_line)
                            
                        elif FINAL_KEY not in intersection_route_dict:
                            intersection_route_dict[FINAL_KEY] = Producer.route.remain([end_line])
                            
            intersection_route_dict[FINAL_KEY] = Producer.route.remain(intersection_route_dict[FINAL_KEY])
            intersection_route_dict[0] = Producer.route.remain(intersection_route_dict[0])
            
            intersection_route_dict = dict(sorted(intersection_route_dict.items(), key=lambda item: item[0], reverse=False))
        
        
        # 获取方案胚
        DICT = 0
        all_plans = {}
        
        for NUM_KEY in intersection_route_dict.keys():
            
            NUM_KEY_NEXT = NUM_KEY + 1
            
            if NUM_KEY == 1:
                break
            
            for every_list in Producer.route.pairElements(
                intersection_route_dict[NUM_KEY],
                intersection_route_dict[NUM_KEY_NEXT]
            ):
                
                if Producer.route.yesOrNotIntersectionLine([every_list[0]],[every_list[1]]) == 1:
                    all_plans[DICT] = [every_list[0],every_list[1]]
                    
                    DICT = DICT + 1
                    
                    
        # 得出线路换乘方案
        for ROUTE_DICT_KEY in range(2, max(list(intersection_route_dict.keys())) + 1):
            
            all_plans = Producer.route.deleteSameDictValue(all_plans)
            
            now_plans = copy.deepcopy(all_plans)
            
            for every_plan in Producer.route.pairElements(
                [servel_plan[-1] for servel_plan in all_plans.values()],
                intersection_route_dict[ROUTE_DICT_KEY]
                ):
                
                if Producer.route.yesOrNotIntersectionLine([every_plan[0]],[every_plan[1]]) == 1:
                    
                    if set(Producer.route.fromValueToKey(now_plans, every_plan[0])) & set(list(now_plans.keys())):
                        
                        for NEW_PLAN_KEY in Producer.route.fromValueToKey(now_plans, every_plan[0]):
                            
                            changed_plans = copy.deepcopy(all_plans)
                            
                            if len(changed_plans[NEW_PLAN_KEY]) == ROUTE_DICT_KEY:
                                all_plans[NEW_PLAN_KEY].append(every_plan[1])
                                
                            elif len(changed_plans[NEW_PLAN_KEY]) != ROUTE_DICT_KEY:
                                NEW_PLAN_KEY_ADD = max(list(all_plans.keys())) + 1
                            
                                for list_element in now_plans[NEW_PLAN_KEY]:
                                    
                                    if NEW_PLAN_KEY_ADD not in changed_plans:
                                        all_plans[NEW_PLAN_KEY_ADD] = [list_element]
                                        changed_plans[NEW_PLAN_KEY_ADD] = [list_element]
                                        
                                    elif NEW_PLAN_KEY_ADD in changed_plans:
                                        all_plans[NEW_PLAN_KEY_ADD].append(list_element)
                                        changed_plans[NEW_PLAN_KEY_ADD].append(list_element)
                                        
                                all_plans[NEW_PLAN_KEY_ADD].append(every_plan[1]) 
                                changed_plans[NEW_PLAN_KEY_ADD].append(every_plan[1])
            
        all_plans = Producer.route.deleteSameDictValue(all_plans)
        
        all_plans = {key: Producer.route.remain(value) for key, value in all_plans.items()}
        
        # 用从小到大（从0开始）的数字重命名各个键
        all_plans = {index: value for index, (key, value) in enumerate(all_plans.items())}
        
        
        compute_dict = {} 
        
        for final_plan,FINAL_PLAN_KEY in zip(all_plans.values(),all_plans.keys()):
        
            final = [[final_plan[i], final_plan[i+1]] for i in range(len(final_plan) - 1)]
            
            for final_pair in final:
                
                intersections = Producer.route.findStationInTwoRoutes([final_pair[0]],[final_pair[1]])
            
                if FINAL_PLAN_KEY in compute_dict:
                    compute_dict[FINAL_PLAN_KEY].append(intersections)
                
                else:
                    compute_dict[FINAL_PLAN_KEY] = [intersections]
        
        compute_dict = {key: [[start_line_and_number]] + value + [[end_line_and_number]] for key, value in compute_dict.items()}


        intersection_name_dict = {}
        
        for compute_dict_element,COMPUTE_KEY in zip(compute_dict.values(),compute_dict.keys()):
            
            for intersection_route_number_list in compute_dict_element:
                
                name_list = []
                
                for intersection_route_number in intersection_route_number_list:
                
                    intersection_name = Producer.route.findStationByRouteAndnumberList(intersection_route_number)
                    
                    name_list.append(intersection_name)
                    
                if COMPUTE_KEY in intersection_name_dict:
                    intersection_name_dict[COMPUTE_KEY].append(name_list)
                    
                else:
                    intersection_name_dict[COMPUTE_KEY] = [name_list]
                    
        
        name_dict = {}
                
        for intersection_name_list,DICT_KEY in zip(
            intersection_name_dict.values(),
            intersection_name_dict.keys()
            ):
            
            for LIST_POS in range(0, len(intersection_name_list)):
                
                if LIST_POS + 1 >= len(intersection_name_list):
                    break

                names = []
                
                servel_list = Producer.route.pairElements(
                    intersection_name_list[LIST_POS],
                    intersection_name_list[LIST_POS + 1]
                    )
                
                for servel in servel_list:
                    
                    names.append(servel)
                    
                if DICT_KEY not in name_dict:
                    name_dict[DICT_KEY] = [names]
                
                elif DICT_KEY in name_dict:
                    name_dict[DICT_KEY].append(names)
            
            
        plan_name_dict = {}
        
        for plan_name_list_informal,PLAN_NAME_KEY in zip(
            name_dict.values(),
            name_dict.keys()
            ):
            
            plan_name_lists = Producer.route.findPaths(plan_name_list_informal)
            
            for plan_name_list in plan_name_lists:
            
                if PLAN_NAME_KEY not in plan_name_dict:
                    plan_name_dict[PLAN_NAME_KEY] = [plan_name_list]
                    
                else:
                    plan_name_dict[PLAN_NAME_KEY].append(plan_name_list)
                    
            plan_name_dict[PLAN_NAME_KEY] = Producer.route.last(plan_name_dict[PLAN_NAME_KEY])
        
        
        all_numbers = {}
        all_numbers_clear = {}
        
        for plan_name_dict_element,same_route_list,PLAN_number_KEY in zip(
            plan_name_dict.values(),
            all_plans.values(),
            plan_name_dict.keys()
            ):
            
            for dict_element_list in plan_name_dict_element:
                
                number_list = []
                
                for element_pair,same_route in zip(
                    [[dict_element_list[i], dict_element_list[i+1]] for i in range(len(dict_element_list)-1)],
                    same_route_list
                    ):
                    
                    need_list = Producer.route.stationRoute(
                        element_pair[0],
                        element_pair[1]
                        )
                    
                    forward_line_and_number = need_list[2]
                    backward_line_and_number = need_list[3]
                    
                    for direct_line in Data.DIRECT_LINE_LIST:
        
                        if same_route == direct_line[0]:
                    
                            start_result_direct = [sublist_1[1:] for sublist_1 in forward_line_and_number if sublist_1[0] in [same_route]][0]
                            end_result_direct = [sublist_2[1:] for sublist_2 in backward_line_and_number if sublist_2[0] in [same_route]][0]
                            
                            direct_servel = []
                            for direct_servel_start, direct_servel_end in itertools.product(start_result_direct, end_result_direct):
                                if direct_servel_start != 0 and direct_servel_end != 0:
                                    if direct_servel_start - direct_servel_end < 0:
                                        direct_servel.append([direct_servel_start,direct_servel_end])
                            
                            if len(direct_servel) != 0:
                                diffs = [abs(a-b) for a,b in direct_servel]
                                min_diff = min(diffs)
                                index = diffs.index(min_diff)
                                number = abs(direct_servel[index][0] - direct_servel[index][1])
                                number_list.append(number)
                                
                                
                            else:
                                number = abs(max(start_result_direct) - max(Producer.route.getMaxNumber(same_route))) + [x for x in end_result_direct if x != 0][0] - 1
                                number_list.append(number)
                            
                        else:

                            forward_result = [sublist_1[1:] for sublist_1 in forward_line_and_number if sublist_1[0] in [same_route]]
                            backward_result = [sublist_2[1:] for sublist_2 in backward_line_and_number if sublist_2[0] in [same_route]]
                            
                            for FORWARD,BACKWARD in itertools.product(forward_result,backward_result):
                                difference_list = [abs(num) for num in [a - b for a,b in zip(FORWARD,BACKWARD)]] # 对两个列表中的对应元素进行减法和绝对值化操作
                                min_number = min(difference_list)
                                
                                number_list.append(min_number)
                        
                if PLAN_number_KEY not in all_numbers_clear:
                    all_numbers_clear[PLAN_number_KEY] = [number_list]
                    
                elif PLAN_number_KEY in all_numbers_clear:
                    all_numbers_clear[PLAN_number_KEY].append(number_list)
                    
                number_list = sum(number_list)
                    
                if PLAN_number_KEY not in all_numbers:
                    all_numbers[PLAN_number_KEY] = [number_list]
                    
                elif PLAN_number_KEY in all_numbers:
                    all_numbers[PLAN_number_KEY].append(number_list)

        
        final_numbers = {}
        clear_numbers = {}
        final_names = {}
        
        for all_number_element_list,all_number_clear_element_list,all_name_element_list,ALL_NUM_KEY in zip(
            all_numbers.values(),
            all_numbers_clear.values(),
            plan_name_dict.values(),
            all_numbers.keys()
            ):
            
            pos_list = Producer.route.findPositions(all_number_element_list,min(all_number_element_list))
            
            all_number_elements = min(all_number_element_list)
        
            final_numbers[ALL_NUM_KEY] = [all_number_elements]
            
            all_number_clear_elements = Producer.route.getElementsByPositions(all_number_clear_element_list, pos_list)
            
            if ALL_NUM_KEY not in clear_numbers:
                clear_numbers[ALL_NUM_KEY] = [all_number_clear_elements]
            
            elif ALL_NUM_KEY in clear_numbers:
                clear_numbers[ALL_NUM_KEY].append(all_number_clear_elements)
                
            all_name_elements = Producer.route.getElementsByPositions(all_name_element_list, pos_list)
            
            if ALL_NUM_KEY not in final_names:
                final_names[ALL_NUM_KEY] = [all_name_elements]
            
            elif ALL_NUM_KEY in final_names:
                final_names[ALL_NUM_KEY].append(all_name_elements)
            
            
        compare_number_list = []

        for servel_number_list in final_numbers.values():
            
            for numbers in servel_number_list:
                
                compare_number_list.append(numbers)
        
        final_min_number = min(compare_number_list)
        
        ALL_KEY = Producer.route.fromValueToKey(final_numbers, final_min_number)
        
        last_numbers = Producer.route.remainKeys(clear_numbers , ALL_KEY)
        
        last_number = Producer.route.remainKeys(final_numbers , ALL_KEY)
        
        last_names = Producer.route.remainKeys(final_names , ALL_KEY)
        
        last_routes = Producer.route.remainKeys(all_plans , ALL_KEY)
        
        
        result = {}
        LAST_KEY = 0
        
        for names_plan,numbers_plan,routes_plan,number_plan in zip(
            last_names.values(),
            last_numbers.values(),
            last_routes.values(),
            last_number.values()
            ):
            
            for servel_numbers_plan,servel_names_plan in zip(
                Producer.route.flattenOnce(numbers_plan),
                Producer.route.flattenOnce(names_plan)
                ):
                
                LAST_KEY = LAST_KEY + 1
                direction = []
                
                routes_plan.append(routes_plan[-1])
                
                pair = [servel_names_plan[i:i + 2] for i in range(len(servel_names_plan) - 1)]
                
                for servel_number,pair_element,servel_route in zip(servel_numbers_plan, pair, routes_plan):
                    
                    for direct_line in Data.DIRECT_LINE_LIST:
                        if servel_route == direct_line[0]:
                            direction.append(direct_line[-1])
                        else:
                            direction.append(Producer.route.direction(servel_route, pair_element, servel_number))
                    
                direction.append(0)
                servel_numbers_plan.append(0)
                
                result["方案" + Producer.ruleText.planName(LAST_KEY)] = [1, servel_numbers_plan, servel_names_plan, routes_plan, number_plan, direction]
        
        return(result)