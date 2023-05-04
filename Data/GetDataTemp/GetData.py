import numpy as np
import pandas as pd
import os
from func import *
import sys


def GetSymbolList(path):
    with open(path,'r') as file:
        SymbolList = file.read()    
        SymbolList = SymbolList.split('\n')
    temp = list()
    for i in SymbolList:
        if i.endswith('USDT'):
            temp.append(i)
    return temp

startTime = "2022-12-14"
endTime = str(datetime.datetime.now()-datetime.timedelta(days=1))[:10]
frq = '5m'
datapath = str(os.path.abspath(sys.argv[0]))[:-22]+'HistoryData/'+frq+'/'
UpdateAll = False
cnt = 0

while cnt<10: #循环10次，避免一些错误导致数据下载不成功
    SymbolList = GetSymbolList(str(os.path.abspath(sys.argv[0]))[:-10]+'symbol.txt')
    HasGet = pd.Series(os.listdir(datapath)).apply(lambda x: x[:-8]).tolist()
    #查找已经下载成功的，每次循环都会重复一次，目的是
    if UpdateAll is False:
        SymbolList = pd.Series(SymbolList)
        SymbolList = SymbolList[SymbolList.apply(lambda x: str(x) not in HasGet)].tolist()

    if SymbolList == []: 
        cnt+=1
        continue
    print('start get:',SymbolList)
    # 开始下载数据
    for Symbol in tqdm(SymbolList):
        klines = GetCoinHistry(Symbol,startTime,endTime,freq=frq)
        if klines is not False:
            klines.to_parquet(datapath+Symbol+'.parquet',index=False)
    cnt+=1

print('get data successfully!')

