import math

def locate_button(n:int)->list[int]:
    # 1st elem: number of times to press button 11
    # 2nd elemn: last button pressed
    res = []
    if n <=11:
        res.append(0)
        res.append(n)
    else:
        x = n-5
        button_11_times = math.floor(x/5)
        if n <= 926:
            last_button = (x%5)+5
        elif n == 930:
            last_button = 11
        else:
            last_button = (x%5)+6
        if (x % 5 == 0) and n!= 930:
            button_11_times-=1
            last_button+=5
        res.append(button_11_times)
        res.append(last_button)
    print(res)
    return res

locate_button(4) # [0, 4]
locate_button(6) # [0, 6]
locate_button(12) # [1, 7]
locate_button(15) # [1, 10]
locate_button(16) # [2, 6]
locate_button(20) # [2, 10]
locate_button(21) # [3, 6]
locate_button(23) # [3, 8]
locate_button(25) # [3, 10]
locate_button(925) # [183, 10]
locate_button(926) # [184, 6]
locate_button(927) # [184, 8]
locate_button(928) # [184, 9]
locate_button(929) # [184, 10]
locate_button(930) # [184, 11]
