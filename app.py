from inspect import trace
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
from statsmodels.tsa.arima.model import ARIMA
from dateutil.relativedelta import relativedelta


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
            flash('Record successfully added', 'success')
            return redirect(url_for('dataform'))
            # return render_template('dataform.html', title='Data Form', form=DataForm())
            con.close()
    else:
        return render_template('dataform.html', title='Data Form', form=form)

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res

def get_forecast(y, time_period):
    model = ARIMA(y, order=(5,1,0))
    model_fit = model.fit()
    forecast = model_fit.predict(start=len(y),end=len(y)+time_period,dynamic=True)
    return list(forecast)
    
@app.route('/user_summary')
def user_summary():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("select * from user_data")
    data = cur.fetchall() 
    total = {}
    user_total = {}
    ngas_total = {}
    elec_total = {}
    fuel_total = {}
    ngas_cp = {}
    elec_cp = {}
    fuel_cp = {}
    for i in data:
        natural_gas = i[3] * 55
        electricity = i[4] * 429
        fuel = i[5] * 887
        sum = natural_gas + electricity + fuel
        avg = (natural_gas + electricity + fuel) / i[2]
        if i[1] in total:
            total[i[1]] += avg
        else:
            total[i[1]] = avg
        if i[0] in user_total:
            if i[1] in user_total[i[0]]:
                user_total[i[0]][i[1]] += avg
            else:
                user_total[i[0]][i[1]] = avg
        else:
            user_total[i[0]] = {i[1]:{}}
            user_total[i[0]][i[1]] = avg
        
        if i[1] in ngas_total:
            ngas_total[i[1]] += natural_gas/i[2]
        else:
            ngas_total[i[1]] = natural_gas/i[2]
        if i[1] in elec_total:
            elec_total[i[1]] += electricity/i[2]
        else:
            elec_total[i[1]] = electricity/i[2]
        if i[1] in fuel_total:
            fuel_total[i[1]] += fuel/i[2]
        else:
            fuel_total[i[1]] = fuel/i[2]
        
        if i[0] in ngas_cp:
            ngas_cp[i[0]] = Merge(ngas_cp[i[0]], {i[1]: natural_gas/i[2]})
        else:
            ngas_cp[i[0]] = {i[1]: natural_gas/i[2]}

        if i[0] in elec_cp:
            elec_cp[i[0]] = Merge(elec_cp[i[0]], {i[1]: electricity/i[2]})
        else:
            elec_cp[i[0]] = {i[1]: electricity/i[2]}

        if i[0] in fuel_cp:
            fuel_cp[i[0]] = Merge(fuel_cp[i[0]], {i[1]: fuel/i[2]})
        else:
            fuel_cp[i[0]] = {i[1]: fuel/i[2]}
    
    
    print(total)
    print(user_total)

    dates = total.keys()

    xScale = [datetime.strptime(d,"%Y-%m-%d").date() for d in dates]
    yScale = list(total.values())

    yScale2 = list(user_total[session['email']].values())
    yScale3 = list(ngas_total.values())
    yScale4 = list(ngas_cp[session['email']].values())
    yScale5 = list(elec_total.values())
    yScale6 = list(elec_cp[session['email']].values())
    yScale7 = list(fuel_total.values())
    yScale8 = list(fuel_cp[session['email']].values())
 
    # Create a trace
    trace1 = go.Scatter(
        x = xScale,
        y = yScale,
        name = "Total"
    )
    trace2 = go.Scatter(
        x = xScale,
        y = yScale2,
        name = "User total"
    )
    trace3 = go.Scatter(
        x = xScale,
        y = yScale3,
        name = "Natural Gas Total"
    )
    trace4 = go.Scatter(
        x = xScale,
        y = yScale4,
        name = "User Natural Gas total"
    ) 
    trace5 = go.Scatter(
        x = xScale,
        y = yScale5,
        name = "Electricity total"
    )
    trace6 = go.Scatter(
        x = xScale,
        y = yScale6,
        name = "User Electricity total"
    )
    trace7 = go.Scatter(
        x = xScale,
        y = yScale7,
        name = "Fuel total"
    )
    trace8 = go.Scatter(
        x = xScale,
        y = yScale8,
        name = "User Fuel total"
    )
 
    data = [trace1, trace2, trace3, trace4, trace5, trace6, trace7, trace8]
    graphJSON = [json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)]

    x_dates = [datetime.strptime(d,"%Y-%m-%d").date() for d in dates]
    y_ng = list(ngas_cp[session['email']].values())
    forecast_dates = []
    for i in range(5):
        d_date = x_dates[-1] + relativedelta(months=i)
        forecast_dates.append(d_date)
        
    ng_forecast = [y_ng[-1]] + get_forecast(y_ng, 4)
    
    trace_natural_gas = go.Scatter(
        x = x_dates,
        y = y_ng,
        name = "Your natural gas consumption"
    )
    trace_natural_gas_forecast = go.Scatter(
        x = forecast_dates,
        y = ng_forecast,
        name = "Your natural gas  projection"
    )

    trace_natural_gas_avg = go.Scatter(
        x = x_dates + forecast_dates[1:],
        y = [110008, 130406, 132789, 150234, 142839, 123674, 131244, 123064, 131475],
        name = "Per capita natural gas consumption"
    )

    data_natural_gas = [trace_natural_gas, trace_natural_gas_forecast, trace_natural_gas_avg]

    graphJSON.append(json.dumps(data_natural_gas, cls=plotly.utils.PlotlyJSONEncoder))

    return render_template('index.html',
                               graphJSON=graphJSON)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)