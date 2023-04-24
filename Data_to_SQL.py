'''
download MYSQL8.0 and install pymsql and sqlalchemy before running!
'''

import pymysql
import zipfile
import pandas as pd
import os
from sqlalchemy import create_engine, VARCHAR, DATETIME

# change your zip data path
history_data_path = r"E:/binance data/"

# change your own account
db = pymysql.connect(host = '127.0.0.1', user = 'root', passwd = 'root')
cursor = db.cursor()

# create the database
# sql1 = "create database CryptoCurrency;"
# cursor.execute(sql1)

engine = create_engine('mysql+pymysql://root:root@localhost:3306/CryptoCurrency?charset-utf-8')

for use_frequency in [x.split('.')[0] for x in os.listdir(history_data_path)]:  # 1m and 5m
    with zipfile.ZipFile(history_data_path + use_frequency + ".zip") as zipobj:
        for file_name in zipobj.namelist():
            data = pd.read_parquet(zipobj.open(file_name))
            data['time'] = pd.to_datetime(data['close_datetime'])
            # only keep the close datetime
            data = data.reset_index().loc[:, ['time', 'code', 'open', 'high', 'low', 'close', 'volume']]
            dtype_dict = {
                'time': DATETIME,
                'code': VARCHAR(data['code'].str.len().max() * 2),
            }
            data.to_sql(use_frequency, con = engine, dtype = dtype_dict, if_exists = 'append', index = False)

# need to be soloved later:some error from duplicated data: IntegrityError: (1062, "Duplicate entry 'LTCUSDT-2021-04-25 12:01:00' for key '1m.PRIMARY'")
# cursor.execute('alter table CryptoCurrency.1m add primary key(code,time);')
# cursor.execute('alter table CryptoCurrency.5m add primary key(code,time);')
cursor.close()
