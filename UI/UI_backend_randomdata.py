# -*- coding: utf-8 -*-
"""
Created on Wed May  3 11:33:35 2023

@author: Sherry
"""
from flask import Flask, render_template
from flask.json import jsonify
from flask import request
from flask import json

import time,threading,datetime,copy,traceback

import numpy as np
import pandas as pd
#import pymysql as psql
#import akshare as ak
#import scipy.stats as st
#import pandas_market_calendars as mcal
import random 
import math


sse = mcal.get_calendar('SSE')#上海证券交易所日历

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/get_netvaluetemp")
def update_NVT_data():
    tt = []
    for i in range(300):
        tt.append(random.randint(0,100))
    return jsonify(tt)


@app.route("/get_operationhistory")
def update_OP_data():
    OP = [['2023-04-06 10:32:00', 'Buy', 21, 4500],
    ['2023-04-06 10:35:00', 'Sell', 20, 4700],
    ['2023-04-06 10:37:00', 'Buy', 21, 4900],
    ['2023-04-06 10:39:00', 'Buy', 11, 4500],
    ['2023-04-06 10:43:00', 'Sell', 10, 4700],
    ['2023-04-06 10:45:00', 'Buy', 21, 4700],
    ['2023-04-06 10:55:00', 'Sell', 10, 4700],
    ['2023-04-06 11:03:00', 'Sell', 11, 4700],
    ['2023-04-06 11:20:00', 'Buy', 21, 4500],
    ['2023-04-06 11:22:00', 'Sell', 10, 4600],
    ['2023-04-06 11:28:00', 'Sell', 20, 5000],
    ['2023-04-06 11:38:00', 'Buy', 21, 4600]]
    for i in range(len(OP)):
        OP[i][2] =  random.randint(10,30)
        OP[i][3] = OP[i][2]*100*random.randint(1,10)
    return jsonify(OP)


@app.route("/get_TCA")
def update_TCA_data():
    TCA = [
['pnl(M)',0.088],
['%ret',0.91],   
['%tvr',36.27],  
['shrp (IR)','0.33( 0.02)'],
['%dd',3.62],   
['%win',0.52],   
['margin',0.51],   
['fitsc',0.05],  
['lnum',583.4],  
['snum',584.7],   
['tdays',240], 
['Tratio',1.00]
]
    for i in range(len(TCA)):
        if i != 3:
            TCA[i][1] =  TCA[i][1] + TCA[i][1]*0.1*math.sin(random.randint(0,100))
    return jsonify(TCA)







if __name__ == "__main__":
    app.run(host='0.0.0.0',port=1122)
