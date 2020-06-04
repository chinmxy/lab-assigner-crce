import mysql.connector
from itertools import combinations

time_slots = {'T845_945': '8:45 - 9:45', 'T945_1045': '9:45 - 10:45', 'T11_12': '11:00 - 12:00', 'T12_1': '12:00 - 13:00',
              'T130_230': '13:30 - 14:30', 'T230_330': '14:30 - 15:30', 'T330_430': '15:30 - 16:30', 'T430_530': '16:30 - 17:30'}


def execute_query(cursor, str_q):
    cursor.execute(str_q)


def gen_timeslot_query(time):
    str2 = "select "
    for i in range(len(time)):
        if i < len(time)-1:
            str2 += time[i]
            str2 += ", "
        else:
            str2 += time[i]
            str2 += " from "
    return str2


def get_freelabs_query(time, day):
    str2 = "select labno from "
    str2 += day
    str2 += " where "
    for i in range(len(time)):
        if i < len(time)-1:
            str2 += time[i]
            str2 += " = '-' and "
        else:
            str2 += time[i]
            str2 += " = '-' "
    return str2


def check_reschedulable(cursor, day, time, acc, labno, software, combn, reschedule_dict):

    execute_query(cursor, "Select labno from software where sw = '" +
                  software + "' intersect " + get_freelabs_query(time, day))
    x = cursor.fetchall()

    reschedulable = []

    for i in x:
        if i[0] not in combn:
            reschedulable.append(i)

    if len(reschedulable) == 0:
        t = str(labno + "|"+time[0])
        reschedule_dict['r_dict'][t] = "X"
        reschedule_dict['ans_str'] += labno + " <span class='text-danger'><b>cannot</b></span> be rescheduled for " + \
            software + " at " + time_slots[time[0]] + "."
    else:
        reschedulable1 = []
        for i in reschedulable:
            reschedulable1.append(i[0])

        finalrbstring = ''
        for j in reschedulable1:
            radiobuttonstring = '<input type="radio" id="male" name="unique" value="male"><label for="male">male</label><br>'
            value = j
            uniqueID = ''
            uniqueID += str(labno)
            uniqueID += '|'
            uniqueID += str(time[0])

            uniqueID.replace(" ", "")

            finalrbstring += radiobuttonstring.replace("male", str(value))
            finalrbstring = finalrbstring.replace("unique", uniqueID)
        reschedule_dict['ans_str'] += "<span class='text-success'><b>"+labno+"</b></span> can be rescheduled for " + \
            software + " at " + time_slots[time[0]
                                           ] + " in : <br>" + finalrbstring

    return reschedule_dict


def reschedule_time(sw, sw_dict):
    time = []
    for key, value in sw_dict.items():
        if sw == value:
            time.append(key)
    return time


def reschedule_labs(day, time, acc, combs):
    conn = mysql.connector.connect(
        host='localhost', user='root', passwd='', db='it_dept')
    cursor = conn.cursor()
    reschedule_dict = {}
    reschedule_dict['ans_str'] = ''
    reschedule_dict['r_dict'] = {}
    r_count = {}
    for i in combs:
        execute_query(cursor, gen_timeslot_query(
            time) + day + " where labno = '"+i+"'")
        sw1 = cursor.fetchall()
        sw_dict = {}
        r_count[i] = 0
        for x, y in zip(time, sw1[0]):
            sw_dict[x] = y
        for k, l in list(sw_dict.items()):
            if l != '-':
                s = l.split("/")
                t = []
                t.append(k)
                r_count[i] += 1
                reschedule_dict = check_reschedulable(
                    cursor, day, t, acc, i, s[1], combs, reschedule_dict)
                if len(reschedule_dict['ans_str']) != 0:
                    reschedule_dict['ans_str'] += "<br>"
        if len(reschedule_dict['ans_str']) != 0:
            reschedule_dict['ans_str'] += "<br>"

    d_count = 0
    for i, j in r_count.items():
        d_count += j
    r_count = {}
    r_count[str(combs)] = d_count
    # print(r_count,len(reschedule_dict['r_dict']))
    reschedule_dict['r_count'] = r_count[str(combs)]

    return reschedule_dict


def displayhis():
    conn = mysql.connector.connect(
        host='localhost', user='root', passwd='', db='it_dept')
    cursor = conn.cursor()
    sql = "select * from output_table"
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


def displaytest(data):
    conn = mysql.connector.connect(
        host='localhost', user='root', passwd='', db='it_dept')
    cursor = conn.cursor()
    sql = "select * from lab_allocations where id = "
    sql += str(data)
    cursor.execute(sql)
    data = cursor.fetchall()
    print("data: ", data)
    '''
    retstring = "<table><tr><th>Lab No.</th><th>Assigned Lab</th><th>Time Slot</th></tr>"
    sample = "<tr><td>d1</td><td>d2</td><td>d3</td></tr>"

    for i in data:
        print(i[1], i[2], i[3])
        sample = sample.replace("d1", i[1])
        sample = sample.replace("d2", i[2])
        sample = sample.replace("d3", i[3])
        retstring += sample
        sample = "<tr><td>d1</td><td>d2</td><td>d3</td></tr>"
    retstring += "</table>"
    '''
    string_list = []

    if data == []:
        retstring = "The labs were already free, so no labs were rescheduled."
        string_list.append(retstring)
    else:
        for i in data:
            if i[2] != 'X':
                retstring = "Lab "+i[1] + \
                    " was rescheduled to "+i[2]+" at "+i[3]+"."
                string_list.append(retstring)
            elif i[2] == 'X':
                retstring = "Lab "+i[1] + \
                    " was cancelled at "+time_slots[i[3]]+"."
                string_list.append(retstring)

    # print(string_list)
    return string_list


def select_best(av_labs, day, time, acc):
    best_list = []
    for i in av_labs:
        temp_list = []
        for j in i:
            temp_list.append(j[0])
        best_list.append(temp_list)
    best_opt = []
    min = 100
    m_cancels = 100
    for i in best_list:
        r_dict = reschedule_labs(day, time, acc, i)
        if r_dict['r_count'] < min:
            min = r_dict['r_count']
            if len(r_dict['r_dict']) < m_cancels:
                m_cancels = len(r_dict['r_dict'])
                if len(best_opt) != 0:
                    best_opt.pop()
                    print(best_opt, "POPPED")
            best_opt.append(i)
            print(best_opt, "APPENDED")
    # print(min,m_cancels)
            # if len(best_opt) != 0 and r_dict['r_count'] != min:
            #     best_opt.pop()
            #     min = r_dict['r_count']
            #     m_cancels = len(r_dict['r_dict'])
            #     best_opt.append(i)
            # elif len(best_opt) != 0 and r_dict['r_count'] == min and len(r_dict['r_dict']) < m_cancels:
            #     best_opt.append(i)
            #     m_cancels = len(r_dict['r_dict'])
            # elif len(best_opt) == 0:
            #     best_opt.append(i)
    return best_opt


def deletefromdb(id):
    conn = mysql.connector.connect(
        host='localhost', user='root', passwd='', db='it_dept')
    cursor = conn.cursor()
    sql = "delete from output_table where id = '"
    sql += str(id)
    sql += "'"
    # print(sql)
    cursor.execute(sql)
    conn.commit()
    sql1 = "delete from lab_allocations where id = '"
    sql1 += str(id)
    sql1 += "'"
    # print(sql1)
    cursor.execute(sql1)
    conn.commit()

    cursor.close()
    conn.close()


def fetchrow(id):
    conn = mysql.connector.connect(
        host='localhost', user='root', passwd='', db='it_dept')
    cursor = conn.cursor()
    sql = "select * from output_table where id = '"
    sql += str(id)
    sql += "'"
    # print(sql)
    cursor.execute(sql)
    row = cursor.fetchall()
    # print(row)
    # conn.commit()
    # cursor.close()
    # conn.close()
    return row
