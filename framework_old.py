__author__ = 'AbsoluteX'
__email__ = 'l276660317@gmail.com'
import time
import math
import threading
import sys
import pandas as pd
import numpy as np
from typing import Dict, List

import binance


class BinanceMarketMakingBot:

    def __init__(self, api_key, api_secret):
        """
        对类进行初始化
        针对之后websocket订阅接受的数据格式  创建相关dict
        同时利用向交易所的请求为这些dict初始赋值  避免访问失败的情况出现。
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = binance.Client(self.api_key, self.api_secret)
        self.btc_min_balance = 0
        # 初始化交易所信息
        info = self.client.get_exchange_info()
        self.symbol_info = dict()

        # Init for exchange Info
        ### 创建用于初始化每一个交易对的基本信息
        for s in info['symbols']:
            # 如果不交易则跳过
            if s['status']!='TRADING': continue
            # 更新交易所基本信息
            symbol = s['symbol']
            self.symbol_info[symbol] = dict()
            self.symbol_info[symbol]['baseAsset'] = s['baseAsset']
            self.symbol_info[symbol]['quoteAsset'] = s['quoteAsset']  # 用于标价的资产
            self.symbol_info[symbol]['orderTypes'] = s['orderTypes']
            self.symbol_info[symbol]['isSpotTradingAllowed'] = s['isSpotTradingAllowed']
            self.symbol_info[symbol]['isMarginTradingAllowed'] = s['isMarginTradingAllowed']
            self.symbol_info[symbol]['minPrice'] = s['filters'][0]['minPrice']
            self.symbol_info[symbol]['tickSize'] = s['filters'][0]['tickSize']
            self.symbol_info[symbol]['minQty'] = s['filters'][1]['minQty']
            self.symbol_info[symbol]['stepSize'] = s['filters'][1]['stepSize']
            self.symbol_info[symbol]['minNotional'] = s['filters'][2]['minNotional']

        # Init for account balance
        ### 创建用于实时更新账户余额数据
        self.account_balances = {}
        z = self.client.get_account()
        for i in z['balances']:
            temp_balance = {}
            temp_balance['asset'] = i['asset']
            temp_balance['free'] = i['free']
            temp_balance['locked'] = i['locked']
            self.account_balances[i["asset"]] = temp_balance

        # Init to accept websocket of Individual Symbol klines
        ### 创建用于接收kline数据的类
        self.klines = {}

        print('/*----- Initial Success -----*/')


    def get_time_diff(self):
        """
        用于获取交易所延迟的函数
        - request_time_cost: 是我们开始向交易所请求，交易所向我们返回值结束这一整个过程的耗时
        - arrival_time_cost: 我们发送的请求到达交易所的耗时，因为已经开启订阅，所以我们通常更关注这个
        """
        start_time = int(time.time()*1000)
        z = self.client.get_server_time()['serverTime']
        end_time = int(time.time()*1000)
        
        request_time_cost = end_time-start_time
        arrival_time_cost = z - start_time
        
        print('request time cost is ',request_time_cost,'ms')
        return arrival_time_cost


if __name__ == "__main__":
    # 初始化api的账号以及密码
    # 账号和密码被存在本地的文件中没有上传
    # 请私聊我获取api_key.txt的最新文件 或者创建您的api key
    with open('api_key.txt','r') as file:
        api_content = file.read().split('\n')
    api_key = api_content[0]
    secret_key = api_content[1]
    
    # 创建交易机器人
    BMMB = BinanceMarketMakingBot(api_key, secret_key)

    cnt=0
    while cnt<10:
        time_diff = BMMB.get_time_diff()
        print("excution arrive exchange cost: ",time_diff,'ms\n')
        cnt+=1
        if time_diff>=1000:
            print('high latency')
            sys.exit(0)

