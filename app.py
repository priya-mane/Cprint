from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_wtf.csrf import CSRFProtect
from forms import SignUpForm, LoginForm, DataForm
from datetime import datetime
import sqlite3
import numpy as np
import json
import plotly
import plotly.graph_objs as go
import pandas as pd

app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)

app.config['SECRET_KEY'] = "athenahacks2022"

@ app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_email = form.email.data
        user_password = form.password.data
        
        if user_email=='abc@gmail.com' and user_password=='abc@123':
            session['email'] = user_email
            flash('You have been logged in!', 'success')
            return redirect(url_for('dataform'))
        else:
            flash('Incorrect Password!', 'danger')
            return render_template('login.html', title='Login', form=form)

    return render_template('login.html', title='Login', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/dataform', methods=['GET', 'POST'])
def dataform():
    form = DataForm()
    if form.validate_on_submit():
        n_ppl = form.no_ppl.data
        n_gas = form.natural_gas.data
        elec = form.electricity.data
        fue = form.fuel.data
        now = datetime.now()
        timestamp = now.strftime("%Y") + '-' + now.strftime("%m") + '-' +  now.strftime("%d")
        with sqlite3.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO user_data (email, timestamp, no_ppl, natural_gas, electricity, fuel) VALUES (?,?,?,?,?,?)", (session['email'],timestamp,n_ppl,n_gas, elec, fue) )
            con.commit()
            msg = "Record successfully added"
            return render_template("successful_submission.html")
            con.close()
    return render_template('user_summary.html', title='Data Form', form=form)

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

@app.route('/user_summary')
def user_summary():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("select * from user_data")
    data = cur.fetchall() 
    total = {}
    user_total = {}
    ngas_cp = {}
    elec_cp = {}
    fuel_cp = {}
    for i in data:
        natural_gas = i[3] * 55
        electricity = i[4] * 429
        fuel = i[5] * 887
        sum = natural_gas + electricity + fuel
        if i[1] in total:
            total[i[1]] += sum
        else:
            total[i[1]] = sum
        if i[0] in user_total:
            if i[1] in user_total[i[0]]:
                user_total[i[0]][i[1]] += sum
            else:
                user_total[i[0]][i[1]] = sum
        else:
            user_total[i[0]] = {i[1]:{}}
            user_total[i[0]][i[1]] = sum
        
        if i[0] in ngas_cp:
            ngas_cp[i[0]] = Merge(ngas_cp[i[0]], {i[1]: natural_gas})
        else:
            ngas_cp[i[0]] = {i[1]: natural_gas}

        if i[0] in elec_cp:
            elec_cp[i[0]] = Merge(elec_cp[i[0]], {i[1]: electricity})
        else:
            elec_cp[i[0]] = {i[1]: electricity}

        if i[0] in fuel_cp:
            fuel_cp[i[0]] = Merge(fuel_cp[i[0]], {i[1]: fuel})
        else:
            fuel_cp[i[0]] = {i[1]: fuel}
    
    print(total)
    print(user_total)
    print(ngas_cp)
    print(elec_cp)
    print(fuel_cp)

    dates = total.keys().tolist()

    count = len(dates)
    xScale = [d.date() for d in pd.to_datetime(dates)]
    yScale = total.values.tolist()
 
    # Create a trace
    trace = go.Scatter(
        x = xScale,
        y = yScale
    )
 
    data = [trace]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html',
                               graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True)