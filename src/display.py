import mysql.connector

time_slots = {'T845_945': '8:45 - 9:45' , 'T945_1045' : '9:45 - 10:45' , 'T11_12' : '11:00 - 12:00' , 'T12_1' : '12:00 - 13:00' , 'T130_230' : '13:30 - 14:30' , 'T230_330' : '14:30 - 15:30' , 'T330_430' : '15:30 - 16:30'}

times = ['T845_945','T945_1045','T11_12','T12_1','T130_230','T230_330','T330_430']
labs = ['802','803','804','808','809','810','711', '902']

def displaytt(day,date):

    final_op = []
    
    conn = mysql.connector.connect(
        host='localhost', user='root', passwd='', db='it_dept')
    cursor = conn.cursor()
    cursor.execute('select * from output_table where date_input = "'+date+'"')
    op = cursor.fetchall()
    cname = ''
    rlist = []

    if (op != []):
        slots = op[0][4].split(" | ")
        cursor.execute('select * from lab_allocations where id = "'+str(op[0][0])+'"')
        resc_op = cursor.fetchall()
        lab = op[0][5].split(" | ")
        cname = op[0][2]

        mk_query = "select * from "
        mk_query += day
        cursor.execute(mk_query)
        data = cursor.fetchall()

        ndata = []
        for i in data:
            line = []
            for j in i:
                line.append(j)
            ndata.append(line)

        cancellations = []

        for i in slots:
            for k in resc_op:
                if k[3] == i:
                    if k[2] != 'X':
                        ndata[labs.index(k[2])][times.index(k[3])+1] = ndata[labs.index(k[1])][times.index(k[3])+1].split("/")[0]
                        rlist.append(ndata[labs.index(k[1])][times.index(k[3])+1].split("/")[0])
                    else:
                        cancellations.append("The practical needs to be cancelled at "+time_slots[i]+" for "+ndata[labs.index(k[1])][times.index(k[3])+1].split("/")[0]+" for "+k[1])
        
        
        for i in lab:
            for j in slots:
                ndata[labs.index(i)][times.index(j)+1] = op[0][2]

        
        if len(cancellations) == 0:
            cancellations = ['None']

    else:
        cursor.execute("Select * from "+day)
        ndata = cursor.fetchall()
        cancellations = ['None']

    final_op.append(ndata)
    final_op.append(cancellations)
    final_op.append(cname)
    final_op.append(rlist)

    return final_op
