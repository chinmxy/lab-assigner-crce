import mysql.connector
from itertools import combinations

queries = __import__("queries")

time_slots = {'T845_945': '8:45 - 9:45', 'T945_1045': '9:45 - 10:45', 'T11_12': '11:00 - 12:00', 'T12_1': '12:00 - 13:00',
              'T130_230': '13:30 - 14:30', 'T230_330': '14:30 - 15:30', 'T330_430': '15:30 - 16:30', 'T430_530': '16:30 - 17:30'}


def execute_query(cursor, str_q):
    cursor.execute(str_q)



def check_reschedulable(cursor, day, time, acc, labno, software, combn, reschedule_dict, pracs):

    execute_query(cursor, "Select labno from software where sw = '" +
                  software + "' intersect " + queries.get_freelabs_query(time, day))
    x = cursor.fetchall()

    reschedulable = []
    for i in x:
        if i[0] not in combn:
            reschedulable.append(i[0])

    if len(reschedulable) == 0:
        t = str(labno + "||"+time[0])
        reschedule_dict['r_dict'][t] = "X"
        reschedule_dict['ans_str'] += labno + " cannot be rescheduled for " + \
            pracs + " at " + time_slots[time[0]] + ". "
    else:
        flag = 0
        for i in reschedulable:
            if i not in list(reschedule_dict['rescheduled'].values()):
                reschedule_dict['rescheduled'][labno +
                                               "||"+time_slots[time[0]]+"||"+pracs] = i
                reschedule_dict['ans_str'] += labno + " can be rescheduled for " + \
                    pracs + " at " + time_slots[time[0]] + " in " + i+". "
            flag = 1
            break

        new_dict = {}
        new_dict['rescheduled'] = {}
        for j, k in reschedule_dict['rescheduled'].items():
            if labno == j.split("||")[0] and pracs == j.split("||")[2] and time_slots[time[0]] != j.split("||")[1]:
                new_dict['rescheduled'][labno+"||" +
                                        time_slots[time[0]]+"||"+pracs] = k
        for n, p in new_dict['rescheduled'].items():
            reschedule_dict['rescheduled'][n] = p
            reschedule_dict['ans_str'] += labno + " can be rescheduled for " + \
                pracs + " at " + time_slots[time[0]] + " in " + p+". "

        if flag == 0:
            t = str(labno + "||"+time[0])
            reschedule_dict['r_dict'][t] = "X"
            reschedule_dict['ans_str'] += labno + " cannot be rescheduled for " + \
                pracs + " at " + time_slots[time[0]] + ".\n"
        # print(reschedule_dict['r_dict'],labno)

    return reschedule_dict


def reschedule_time(sw, sw_dict):
    time = []
    for key, value in sw_dict.items():
        if sw == value:
            time.append(key)
    return time


def genKey(comb):
    key = ''
    for i in comb:

        key += i
        if(i != comb[-1]):
            key += " | "

    return key


# genKey(['802', '803', '804', '805'])


def reschedule_labs(ip):
    day = ip['day']
    time = ip['time_slots']
    acc = ip['acc']
    all_combs = ip['av_labs']
    rd_list = []

    for combs in all_combs:

        combKey = genKey(combs)

        conn = mysql.connector.connect(
            host='localhost', user='root', passwd='', db='it_dept')
        cursor = conn.cursor()

        reschedule_dict = {}
        reschedule_dict['ans_str'] = ''
        reschedule_dict['r_dict'] = {}
        reschedule_dict['rescheduled'] = {}
        for i in combs:
            execute_query(cursor, queries.gen_timeslot_query(
                time) + day + " where labno = '"+i+"'")
            sw1 = cursor.fetchall()
            sw_dict = {}
            for x, y in zip(time, sw1[0]):
                sw_dict[x] = y
            for k, l in list(sw_dict.items()):
                if l != '-':
                    s = l.split(" / ")
                    t = []
                    t.append(k)
                    reschedule_dict = check_reschedulable(
                        cursor, day, t, acc, i, s[1], combs, reschedule_dict, s[0])
        if reschedule_dict['ans_str'] == '':
            reschedule_dict['ans_str'] = "The selected labs are free to use"

        someDict = {combKey: reschedule_dict}
        rd_list.append(someDict)
    # print()
    return rd_list


# for i in reschedule_labs(ip):
#     print(i)


def bestOption(mainList):
    leastCancellations = 999
    leastReschedules = 999
    bestCombination = []
    bestCombinationwRS = []
    for i in mainList:
        if(leastCancellations == 999):
            leastCancellations = len(i['r_dict'])
            bestCombination.append(i)
        else:
            if(len(i['r_dict']) < leastCancellations):
                leastCancellations = len(i['r_dict'])
                bestCombination.clear()
                bestCombination.append(i)

            if(len(i['r_dict']) == leastCancellations):
                # leastCancellations = len(i['r_dict'])
                # bestCombination.clear()
                bestCombination.append(i)
    # print(bestCombination)
    if (len(bestCombination) > 1):
        for i in bestCombination:
            if (leastReschedules == 999):
                leastReschedules = len(i['rescheduled'])
                bestCombinationwRS.append(i)
            else:
                if(len(i['rescheduled']) < leastReschedules):
                    leastReschedules = len(i['rescheduled'])
                    bestCombinationwRS.clear()
                    bestCombinationwRS.append(i)

                if(len(i['rescheduled']) == leastReschedules):
                    # leastCancellations = len(i['r_dict'])
                    # bestCombination.clear()
                    bestCombinationwRS.append(i)
        return bestCombinationwRS

    else:
        return bestCombination


def sortRdict(val):
    list1 = list(val.values())
    return(len(list1[0]['r_dict']))
    # return(len(val['r_dict']))


def sortRescheduled(val):
    list1 = list(val.values())
    return(len(list1[0]['rescheduled']))

    # return(len(val['rescheduled']))


def bestOption2(mainList):

    mainList.sort(key=sortRdict)
    bestCanOptions = []
    remainingOptions = []
    leastCancellations = len(list(mainList[0].values())[0]['r_dict'])

    # print(leastCancellations)
    for i in range(0, len(mainList)):
        if(len(list(mainList[i].values())[0]['r_dict']) == leastCancellations):
            bestCanOptions.append(mainList[i])
        else:
            remainingOptions.append(mainList[i])

    bestCanOptions.sort(key=sortRescheduled)
    remainingOptions.sort(key=sortRescheduled)
    
    sortedOptionList = bestCanOptions + remainingOptions


    return sortedOptionList


