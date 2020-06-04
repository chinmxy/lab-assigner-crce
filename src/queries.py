import mysql.connector


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


def sum_t(t):
    sum = 0
    for i in t:
        sum += int(i[1])
    return sum


def get_fl_cap(time, day):
    str1 = "select a.labno,a.capacity from accom as a join "
    str2 = 'select labno from '+day+' where '
    for i in range(len(time)):
        if i < len(time)-1:
            str2 += time[i]
            str2 += " = '-' "
            str2 += ' and '
        else:
            str2 += time[i]
            str2 += " = '-' "
    str1 += "("
    str1 += str2
    str1 += ") as temp on a.labno = temp.labno"
    return str1


def get_sw_cap(sw):
    str1 = "select a.labno,a.capacity from accom as a join "
    str2 = 'select labno from Software where sw = '
    for i in range(len(sw)):
        if i < len(sw)-1:
            str2 += "'"
            str2 += sw[i]
            str2 += "'"
            str2 += ' intersect select labno from Software where sw = '
        else:
            str2 += "'"
            str2 += sw[i]
            str2 += "'"
    str1 += "("
    str1 += str2
    str1 += ") as temp on a.labno = temp.labno"
    return str1


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


def db_update(current_option, full_data):

    c_name = full_data['c_name']
    date_input = full_data['date_input']
    # print(type(date_input))
    acc = str(full_data['acc'])
    time = full_data['time_slots']
    comb_str = current_option[0]
    # print(type(comb_str))

    # creating time string
    time_str = ''
    for i in range(len(time)):
        if i < len(time)-1:
            time_str += str(time[i]) + " | "
        else:
            time_str += str(time[i])

    # print(time_str)

    op_msg = "Some error occurred, could not update successfully!"

    conn = mysql.connector.connect(
        host='localhost', user='root', passwd='', db='it_dept')
    cursor = conn.cursor()
    # selects max ID from table
    cursor.execute('select max(id) from output_table')
    last_id_no = str(cursor.fetchall()[0][0])
    # print(eg)
    if (last_id_no == 'None'):
        cursor.execute('insert into output_table (id, date_input, c_name, accomo,combn,time_slots) values (1,"' +
                       date_input+'","'+c_name+'","'+acc+'","'+comb_str+'","'+time_str+'")')
        conn.commit()
        for i, j in current_option[1]['r_dict'].items():
            lnt = i.split("|")
            cursor.execute(
                'insert into lab_allocations values ("1","'+lnt[0]+'","'+j+'","'+lnt[2]+'")')
            conn.commit()
        for i, j in current_option[1]['rescheduled'].items():
            lnt = i.split("|")
            cursor.execute(
                'insert into lab_allocations values ("1","'+lnt[0]+'","'+j+'","'+lnt[2]+'")')
            conn.commit()
            # return ("Updated successfully!")
        op_msg = "Updated successfully!"
    else:
        current_id_no = int(last_id_no) + 1
        cursor.execute('insert into output_table (id, date_input, c_name, accomo,combn,time_slots) values ("'+str(current_id_no)+'","' +
                       date_input+'","'+c_name+'","'+acc+'","'+comb_str+'","'+time_str+'")')
        conn.commit()
        for i, j in current_option[1]['r_dict'].items():
            lnt = i.split("|")
            cursor.execute('insert into lab_allocations values ("' +
                           str(current_id_no)+'","'+lnt[0]+'","'+j+'","'+lnt[2]+'")')
            conn.commit()
        for i, j in current_option[1]['rescheduled'].items():
            lnt = i.split("|")
            cursor.execute('insert into lab_allocations values ("' +
                           str(current_id_no)+'","'+lnt[0]+'","'+j+'","'+lnt[2]+'")')
            conn.commit()
        op_msg = "Updated successfully!"
    return op_msg


# Queries to test
# TRUNCATE TABLE output_table;
# TRUNCATE TABLE lab_allocations;
