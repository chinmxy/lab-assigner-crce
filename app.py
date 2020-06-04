import calendar
from datetime import date
from flask import Flask, request, render_template, jsonify, json

# allotment_options = __import__("allotment_options")
# select_best = __import__("select_best")
# queries = __import__("queries")
# misc_funcs = __import__("misc_funcs")

# display_ob = __import__("display")
# demo = __import__("demo")

from src import queries
from src import allotment_options
from src import demo
from src import display as display_ob
from src import misc_funcs
from src import select_best

app = Flask(__name__)


@app.route('/')
def my_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def my_form_post():
    i_acc = request.form['occupancy']
    # print(type(i_acc))
    company_name = request.form['company-name']
    date_input = request.form['date-input']

    d1 = request.form['date-input'].split("-")
    dayname = calendar.day_name[date(int(d1[0]),
                                     int(d1[1]), int(d1[2])).weekday()]
    i_day = dayname
    i_time = request.form.getlist('cb')
    i_sw = request.form.getlist('sw')
    # av_labs = schedule_labs(i_day, i_time, int(i_acc), i_sw)
    data_pass = {}
    data_pass['c_name'] = company_name
    data_pass['date_input'] = date_input
    data_pass['day'] = i_day
    data_pass['time_slots'] = i_time
    data_pass['acc'] = int(i_acc)
    data_pass['sw'] = i_sw
    data_pass['av_labs'] = []
    data_pass['error_message'] = ''

    # print(data_pass)
    data_pass = allotment_options.getFinalOp(data_pass)
    # print(data_pass)
# opdata1 = jsonify(list(opdata))
    return render_template('result.html', data=data_pass)


@app.route('/update_db/', methods=['POST'])
def update_db():
    rf = request.form
    for key in rf.keys():
        data = key
    option_data = json.loads(data)
    # print(option_data)
    current_option = option_data[0]
    full_data = option_data[1]
    op_msg = queries.db_update(current_option, full_data)

    # return jsonify("Return successfully")
    return jsonify(op_msg)


@app.route('/timetable')
def viewtt():
    return render_template("tt.html", value=[[], []])


@app.route('/timetable', methods=['POST'])
def displaytt():
    date_input = request.form['date-input']
    d1 = request.form['date-input'].split("-")
    dayname = calendar.day_name[date(int(d1[0]),
                                     int(d1[1]), int(d1[2])).weekday()]
    data = display_ob.displaytt(dayname, date_input)
    return render_template("tt.html", value=data)


@app.route('/history')
def history():
    data = demo.displayhis()
    print(data)
    return render_template("history.html", value=data)


@app.route('/fetchlabs', methods=['POST'])
def fetchlabs():
    rf = request.form
    for key in rf.keys():
        data = key
    data_r = json.loads(data)
    # print(type(data_r))

    data = demo.displaytest(data_r)
    return jsonify(data)


@app.route('/deletedb', methods=['POST'])
def deletedb():
    rf = request.form
    for key in rf.keys():
        data = key
    data_r = json.loads(data)
    # print("here", data_r)
    demo.deletefromdb(data_r)
    return "hello"


@app.route('/changedate', methods=['POST'])
def changedate():
    rf = request.form
    for key in rf.keys():
        data = key
    data_r = json.loads(data)
    # print("here", data_r)
    dataa = reschedule_ob.fetchrow(data_r)
    # print(dataa)
    return jsonify("yes")


app.jinja_env.add_extension('jinja2.ext.do')
app.run(debug=True)
