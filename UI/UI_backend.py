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
import pandas_market_calendars as mcal
import random 
import math

import os
import sys


sse = mcal.get_calendar('SSE')#上海证券交易所日历

app = Flask(__name__)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route("/get_netvaluetemp")
def update_NVT_data():
    return jsonify(NVP)


@app.route("/get_operationhistory")
def update_OP_data():
    return jsonify(OP)


@app.route("/get_TCA")
def update_TCA_data():
    return jsonify(TCA)




#交易时间判断
def is_trade_day(date):
    td_df = sse.schedule(start_date=date, end_date=date)
    return len(td_df.index)


def is_trade_time():#延迟1min结束
    global trade_time
    trade_time = False
    while True:
        today = str(datetime.date.today())
        if is_trade_day(today):
            while True:
                if ('09:30:00'<datetime.datetime.now().strftime("%H:%M:%S")<'11:31:00') or ('13:00:00'<datetime.datetime.now().strftime("%H:%M:%S")<'15:01:00'):
                    trade_time = True
                    time.sleep(1)
               
                else:
                    trade_time = False
                    time.sleep(1)
                    if datetime.datetime.now().strftime("%H:%M:%S")>'17:00:00':
                        time.sleep(60*60*15)
                        break
        else:
            time.sleep(60*60*24)



def read_netvalue():
    global NVP
    while True:
        if trade_time:
            path = str(os.path.abspath(sys.argv[0]))[:-13]
            data = pd.read_table(path+'NetValueTemp.log',sep=',',header=None)
            if len(data)>300:
                data = data[-300:]
            NVP = data[1].values.tolist()
            time.sleep(1)
        else:
            time.sleep(1)
            
def read_op():
     global OP
     while True:
         if trade_time:
             path = str(os.path.abspath(sys.argv[0]))[:-13]
             data = pd.read_table(path+'Operation.log',sep=',',header=None)
             if len(data)>10:
                 data = data[-10:]
             OP = data.values.tolist()
             time.sleep(1)
         else:
             time.sleep(1)       
    
def read_TCA():
     global TCA
     while True:
         if trade_time:
             path = str(os.path.abspath(sys.argv[0]))[:-13]
             data = pd.read_table(path+'TCA.log',sep=',',header=None)
             if len(data)>10:
                 data = data[-10:]
             TCA = data.values.tolist()
             time.sleep(1)
         else:
             time.sleep(1)      



if __name__ == "__main__":
   # 实盘用运行这两行
   # t1=threading.Thread(target=is_trade_time)
   # t1.start()
    trade_time = True#演示用
    t2=threading.Thread(target=read_netvalue)
    t3=threading.Thread(target=read_op)
    t4=threading.Thread(target=read_TCA)
    t2.start()
    t3.start()
    t4.start()
    
    app.run(host='0.0.0.0',port=1122)
    """
    /opt/anaconda3/envs/BinanceTrading/bin/python /Users/absolutex/Library/CloudStorage/OneDrive-个人/market/BlockChain/BinanceMarketmaking/UI/UI_backend.py
    
    http://0.0.0.0:1122/dashboard
    """
