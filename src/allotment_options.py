import mysql.connector

from . import queries as query
from . import misc_funcs as func
from . import select_best

# query = __import__("queries")
# func = __import__("misc_funcs")
# select_best = __import__("select_best")


def execute_query(cursor, str_q):
    cursor.execute(str_q)


conn = mysql.connector.connect(
    host='localhost', user='root', passwd='', db='it_dept')
cursor = conn.cursor()


def get_appr_comb(acc, lists):
    execute_query(cursor, "select * from accom")
    all_labs = cursor.fetchall()
    all_labs_wo_swlabs = []
    final_comb_list = []
    if len(lists) == 1:
        for i in all_labs:
            if i not in lists[0]:
                all_labs_wo_swlabs.append(i)
        cap_comb_list = func.get_combinations(acc, all_labs_wo_swlabs)
        for i in cap_comb_list:
            final_comb_list.append([lists[0], list(i)])
    else:
        for i in all_labs:
            if i not in lists[0] and i not in lists[1]:
                all_labs_wo_swlabs.append(i)
        cap_comb_list = func.get_combinations(acc, all_labs_wo_swlabs)
        for i in cap_comb_list:
            final_comb_list.append([lists[0], lists[1]+list(i)])

    return final_comb_list


def make_comb_list(possible_combs, labs_with_sw):
    final_comb_list = []
    if len(possible_combs) == 1:
        final_comb = []
        final_comb.append(labs_with_sw)
        final_comb.append(possible_combs)
        final_comb_list.append(final_comb)
    else:
        for i in possible_combs:
            final_comb = []
            final_comb.append(labs_with_sw)
            final_comb.append(list(i))
            final_comb_list.append(final_comb)

    return final_comb_list


def schedule_labs(data):
    title_msg = []
    if data['sw'] != []:
        execute_query(cursor, query.get_sw_cap(data['sw']))
        labs_with_sw = cursor.fetchall()
        if labs_with_sw != []:
            if func.get_total_cap(labs_with_sw) >= data['acc']:
                print("LABS HAVE SOFTWARE SHOULD BE USED:")
                title_msg.append("LABS HAVE SOFTWARE SHOULD BE USED:")

                ''' I've made changes starting here'''
                comb_list = func.get_combinations(data['acc'], labs_with_sw)
                final_comb_list = []
                for i in comb_list:
                    final_comb_list.append([list(i), []])
                ''' Uptill here '''

            else:
                execute_query(cursor, query.get_fl_cap(
                    data['time_slots'], data['day']))
                flabs = cursor.fetchall()
                if flabs != []:
                    flabs_wo_sw = []
                    for i in flabs:
                        if i not in labs_with_sw:
                            flabs_wo_sw.append(i)
                    possible_combs = func.get_combinations(
                        data['acc'] - func.get_total_cap(labs_with_sw), flabs_wo_sw)
                    if possible_combs != []:
                        final_comb_list = make_comb_list(
                            possible_combs, labs_with_sw)
                        print("LIST1 W SW  LIST2 W/O SW", "FREE LABS")
                        # title_msg.append("LIST1 W SW  LIST2 W/O SW", "FREE LABS")
                    else:
                        final_comb_list = get_appr_comb(data['acc'] - func.get_total_cap(
                            labs_with_sw) - func.get_total_cap(flabs_wo_sw), [labs_with_sw, flabs_wo_sw])
                        print("LIST1 W SW  LIST2 W/O SW",
                              "FREE LABS & UNFREE LABS")
                        # title_msg.append("LIST1 W SW  LIST2 W/O SW",
                        #       "FREE LABS & UNFREE LABS")
                else:
                    final_comb_list = get_appr_comb(
                        data['acc'] - func.get_total_cap(labs_with_sw), [labs_with_sw])
                    print("LABS W SW  LIST2 LABS W/O SW", "UNFREE LABS")

        else:
            execute_query(cursor, query.get_fl_cap(
                data['time_slots'], data['day']))
            flabs = cursor.fetchall()
            if flabs != []:
                if func.get_total_cap(flabs) >= data['acc']:
                    # final_comb_list = func.get_combinations(data['acc'], flabs)
                    comb_list = func.get_combinations(data['acc'], flabs)
                    final_comb_list = []
                    for i in comb_list:
                        final_comb_list.append([list(i), []])

                    print(
                        "NO LABS HAVE REQUIRED SOFTWARE, The following are combinations of free labs that can used:", "FREE LABS")
                    title_msg.append(
                        "NO LABS HAVE REQUIRED SOFTWARE, The following are combinations of free labs that can used:")
                else:
                    final_comb_list = get_appr_comb(
                        data['acc'] - func.get_total_cap(flabs), [flabs])
                    print("NO LABS HAVE REQUIRED SOFTWARE, The following are combinations of free labs that can used:",
                          "FREE LABS & UNFREE LABS")
                    title_msg.append(
                        "NO LABS HAVE REQUIRED SOFTWARE, The following are combinations of free labs that can used:")
            else:
                execute_query(cursor, "select * from accom")
                # final_comb_list = func.get_combinations(
                #     data['acc'], cursor.fetchall())
                comb_list = func.get_combinations(
                    data['acc'], cursor.fetchall())
                final_comb_list = []
                for i in comb_list:
                    final_comb_list.append([list(i), []])
                print(
                    "NO LABS HAVE SW , Neither are any labs free , you can use the following combintaions:")
                title_msg.append(
                    "NO LABS HAVE SW , Neither are any labs free , you can use the following combintaions:")
    else:
        execute_query(cursor, query.get_fl_cap(
            data['time_slots'], data['day']))
        flabs = cursor.fetchall()
        if flabs != []:
            if func.get_total_cap(flabs) >= data['acc']:
                # final_comb_list = func.get_combinations(data['acc'], flabs)
                comb_list = func.get_combinations(data['acc'], flabs)
                final_comb_list = []
                for i in comb_list:
                    final_comb_list.append([list(i), []])

                print("THE LABS ARE FREE AND CAN BE USED:")
                title_msg.append("THE LABS ARE FREE AND CAN BE USED:")

            else:
                final_comb_list = get_appr_comb(
                    data['acc'] - func.get_total_cap(flabs), [flabs])
                print("THERE ARE FREE AND UNFREE LABS:")
                title_msg.append("THERE ARE FREE AND UNFREE LABS:")
        else:
            execute_query(cursor, "select * from accom")
            # final_comb_list = func.get_combinations(
            #     data['acc'], cursor.fetchall())
            comb_list = func.get_combinations(data['acc'], cursor.fetchall())
            final_comb_list = []
            for i in comb_list:
                final_comb_list.append([list(i), []])
            print("NO LABS ARE FREE, THE FOLLOWING LABS CAN BE USED")
            title_msg.append(
                "NO LABS ARE FREE, THE FOLLOWING LABS CAN BE USED")

    # print(final_comb_list)
    # for i in final_comb_list:
    #     print(i, "\n")
    final_app_list = []
    for i in final_comb_list:
        app_list = []
        for j in i[0]:
            app_list.append(j[0])
        if (i[1]):
            for j in i[1]:
                app_list.append(j[0])

        final_app_list.append(app_list)

    return (final_app_list, title_msg)
    # print(final_app_list)


ip = {'c_name': 'ABC', 'date_input': '2020-03-10', 'day': 'Tuesday', 'time_slots': [
    'T11_12', 'T12_1'], 'acc': 40, 'av_labs': {}, 'best_opt': {}, 'sw': ['SQL'], 'error_message': ''}

sl_op = schedule_labs(ip)
print(sl_op)
# ip['av_labs'] = sl_op
# print(ip)

# select_best.reschedule_labs(ip)


def getFinalOp(input):
    sl_op = schedule_labs(input)
    input['av_labs'], title_message = sl_op
    list_of_all_combs = select_best.reschedule_labs(input)
    # print('list of all combs', list_of_all_combs)
    op = select_best.bestOption2(list_of_all_combs)
    input['displaylabs'] = op
    input['title_msg'] = title_message

    return input
