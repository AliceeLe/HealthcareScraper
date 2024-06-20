import math

def approach_1(n:int)->list[int]:
    # 1st elem: number of times to press button 11
    # 2nd elemn: last button pressed
    res = []
    if n <=11:
        res.append(0)
        res.append(n)
    else:
        x = n-5
        button_11_times = math.floor(x/5)
        last_button = (x%5)+5
        if (x % 5 == 0) and n!= 930:
            button_11_times-=1
            last_button+=5
        res.append(button_11_times)
        res.append(last_button)
    return res

def approach_2(n:int)->list[int]:
    # 1st elem: number of times to press button 1
    # 2nd elemn: last button pressed
    res = []
    if n >= 920:
        res.append(0)
        res.append(n+1-920)
    else: 
        x = 930 - n - 5
        button_1_times = math.floor(x/5)
        last_button = (x % 5)
        res.append(button_1_times)
        res.append(dict_button.get(last_button))
    return res
    
dict_button = {0:1, 1:5, 2:4, 3:3, 4:2}
def compute_button(num:int)->int:
    approach1 = approach_1(num)
    approach2 = approach_2(num)
    if approach1[0] <= approach2[0]: 
        approach1.append(1)
        return approach1
    else: 
        approach2.append(2)
        return approach2


