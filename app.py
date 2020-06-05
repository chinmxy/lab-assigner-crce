import calendar
from datetime import date
from flask import Flask, request, render_template, jsonify, json

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
    data_pass = {}
    data_pass['c_name'] = request.form['company-name']
    data_pass['date_input'] = request.form['date-input']
    data_pass['day'] = calendar.day_name[date(int(data_pass['date_input'].split('-')[0]),
                                     int(data_pass['date_input'].split('-')[1]), int(data_pass['date_input'].split('-')[2])).weekday()]
    data_pass['time_slots'] = request.form.getlist('cb')
    data_pass['acc'] = int(request.form['occupancy'])
    data_pass['sw'] = request.form.getlist('sw')
    data_pass['av_labs'] = []
    data_pass['error_message'] = ''

    data_pass = allotment_options.getFinalOp(data_pass)
    return render_template('result.html', data=data_pass)


@app.route('/update_db/', methods=['POST'])
def update_db():
    rf = request.form
    for key in rf.keys():
        data = key
    option_data = json.loads(data)
    current_option = option_data[0]
    full_data = option_data[1]
    op_msg = queries.db_update(current_option, full_data)

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
    return render_template("history.html", value=data)


@app.route('/fetchlabs', methods=['POST'])
def fetchlabs():
    rf = request.form
    for key in rf.keys():
        data = key
    data_r = json.loads(data)

    data = demo.displaytest(data_r)
    return jsonify(data)


@app.route('/deletedb', methods=['POST'])
def deletedb():
    rf = request.form
    for key in rf.keys():
        data = key
    data_r = json.loads(data)
    demo.deletefromdb(data_r)
    return "hello"


@app.route('/changedate', methods=['POST'])
def changedate():
    rf = request.form
    for key in rf.keys():
        data = key
    data_r = json.loads(data)
    dataa = reschedule_ob.fetchrow(data_r)
    return jsonify("yes")


app.jinja_env.add_extension('jinja2.ext.do')
app.run(debug=True)
