from itertools import combinations

def sum_t(t):
    sum=0
    for i in t:
        sum+=int(i[1])
    return sum

def get_combinations(acc,sw):
    final=[]
    flag = 0
    for j in range(1,len(sw)+1):
        sub_c = combinations(sw,j)
        for i in list(sub_c):
            if(sum_t(i) >= acc):
                final.append(i)
                flag = 1
        if (flag != 0):
            break
    return final

def reschedule_time(sw, sw_dict):
    time = []
    for key, value in sw_dict.items():
        if sw == value:
            time.append(key)
    return time

def get_total_cap(sw_lab_list):
    cap = 0
    for i in sw_lab_list:
        cap += i[1]
    return cap