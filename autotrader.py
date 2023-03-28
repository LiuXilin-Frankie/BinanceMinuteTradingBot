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

        """
        /*----- websocket market data -----*/   
        以下字典用于接受不同的websocket行情自动更新信息
        请根据策略特性选择需要开启的行情接受
        请不要过度开启 避免过高的流量费用以及内存占用
        """

        # Init to accept websocket of Individual Symbol Book Ticker Streams
        ### 创建用于接收实时推送的最优买卖价格以及数量
        self.orderbook_tickers = self.client.get_orderbook_tickers()
        self.orderbook_best = {}
        for i in self.orderbook_tickers: # initialize values of self.orderbook_tickers_dict
            temp_book = {} #for the uniform format
            temp_book['u'] = int(1838597807)
            temp_book['s'] = i['symbol']
            temp_book['b'] = i['bidPrice']
            temp_book['B'] = i['bidQty']
            temp_book['a'] = i['askPrice']
            temp_book['A'] = i['askQty']
            self.orderbook_best[i['symbol']] = temp_book

        
        print('/*----- Initial Success -----*/')


if __name__ == "__main__":
    api_key = 'rF7wq1ri0kMJBxRhQZTiFUx5U8OO50oNi9iOZhzLD6kf9N7dIwG4mowiHz7psGX1'
    secret_key = 'cWtzGZsaoddLMYlw5MghAQDVqm12rkAYiJDxfQwa26WwQRaUnNeXw5dc06KLVzjw'
    BMMB = BinanceMarketMakingBot(api_key, secret_key)

    # socket manager using threads
    twm = binance.ThreadedWebsocketManager()
    twm.start()

    # depth cache manager using threads
    # dcm = binance.ThreadedDepthCacheManager()
    # dcm.start()

    # def handle_socket_message(msg):
    #     print(f"message type: {msg['e']}")
    #     print(msg)

    # def handle_dcm_message(depth_cache):
    #     print(f"symbol {depth_cache.symbol}")
    #     print("top 5 bids")
    #     print(depth_cache.get_bids()[:5])
    #     print("top 5 asks")
    #     print(depth_cache.get_asks()[:5])
    #     print("last update time {}".format(depth_cache.update_time))

    # twm.start_kline_socket(callback=handle_socket_message, symbol='BNBBTC')

    # dcm.start_depth_cache(callback=handle_dcm_message, symbol='ETHBTC')
    #tm = 

