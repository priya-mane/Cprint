'''
from flask import Flask, redirect, url_for, render_template
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)
csrf.init_app(app)

app.config['SECRET_KEY'] = "priyamane"

@app.route('/')
def signup():
    return render_template('login.html')

@app.route('/signup')
def login():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)

'''
import email
from flask import Flask, render_template
from flask_mysqldb import MySQL 
import datetime
import mysql.connector
import json
import plotly
import plotly.graph_objs as go
 
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    count = 500
    xScale = np.linspace(0, 100, count)
    yScale = np.random.randn(count)
 
    # Create a trace
    trace = go.Scatter(
        x = xScale,
        y = yScale
    )
 
    data = [trace]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html',
                               graphJSON=graphJSON)
    #return render_template('index.html')

if __name__ == '__main__':
    app.run()
