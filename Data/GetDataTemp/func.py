"""pip install binance-history"""

import numpy as np
import pandas as pd
import binance_history as bh
import time
import datetime
import os
from tqdm import *

def GetCoinHistry(Symbol,startTime,endTime,freq='1m'):
    """
    分段拿回需要的历史数据
    如果拿取失败会return False
    """
    klines = np.nan #作为我们的初始表单
    HaveStart = 0   #作为我们是否已经开始下载数据的指针
    for i in range(int(startTime[:4]), (int(endTime[:4]))):
        try:
            TmpStart = str(i)+startTime[4:]
            TmpEnd = str(i+1)+endTime[4:]
            
            TmpData = bh.fetch_klines(
                symbol=Symbol,
                timeframe=freq,
                start=TmpStart,
                end=TmpEnd,
            )

            HaveStart = 1   #如果成功拿取数据，指针变为1
            TmpData = pd.DataFrame(TmpData).reset_index(drop=False)
            try: klines = pd.concat([klines,TmpData])
            except: klines = TmpData
        except:
            if HaveStart==0: continue
            if HaveStart==1: #之前成功拿取过数据，代表错误由于网络原因导致，停止拿取该symbol
                return False
        time.sleep(2)
    try:
        klines['code'] = str(Symbol)
        klines = klines.drop_duplicates(subset=['open_datetime','code'],keep='last').reset_index(drop=True)
        return klines
    except: return False
