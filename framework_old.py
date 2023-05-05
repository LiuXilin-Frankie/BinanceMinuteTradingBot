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


class BinanceTradingBot:

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
            if s['status'] != 'TRADING': continue
            # 更新交易所基本信息
            symbol = s['symbol']
            #print(s)
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
            try: self.symbol_info[symbol]['minNotional'] = s['filters'][2]['minNotional']
            except: self.symbol_info[symbol]['minNotional'] = '0.000100'

        # Init to accept websocket of Individual Symbol klines
        ### 创建用于接收kline数据的类
        self.klines = {}

        print('/*----- Initial Success -----*/')

    ### /*----- orders func -----*/
    ### below are all func about palce order in the market
    ### you can directly set market order since I have defined here

    def market_buy(self, symbol, qty):
        """
        下市价买单
        """
        symbol = symbol.upper()
        if self.order_errors(qty, symbol):  # used for catching the error
            print("symbol,qty: ", symbol, qty)
            start_time = time.time()
            # order_info = self.client.order_market_buy(symbol=symbol, quantity=str(qty))
            # print("time cost for place the buy pivot order is:",time.time()-start_time)
            # self.order_info_dict[symbol] = order_info
            # return order_info['orderId']
            actually_trade = self.client.aggregate_trade_iter(symbol = symbol)
            actually_trade = next(actually_trade)['p']
            actually_trade = self.client.get_recent_trades(symbol=symbol)[-1]['price']
            return float(actually_trade)
        else:
            time.sleep(0.1)
            return False

    def market_sell(self, symbol, qty):
        """
        下市价卖单
        """
        symbol = symbol.upper()
        if self.order_errors(qty, symbol):  # used for catching the error
            print("symbol,qty: ", symbol, qty)
            # start_time = time.time()
            # order_info = self.client.order_market_sell(symbol=symbol, quantity=str(qty))
            # print("time cost for place the buy pivot order is:",time.time()-start_time)
            # self.order_info_dict[symbol] = order_info
            # return order_info['orderId']
            actually_trade = self.client.aggregate_trade_iter(symbol = symbol)
            actually_trade = next(actually_trade)['p']
            actually_trade = self.client.get_recent_trades(symbol=symbol)[-1]['price']
            return float(actually_trade)
        else:
            time.sleep(0.1)
            return False

    ### /*----- moduls -----*/
    ### tools functiuon in our BinanceMarketMakingBot
    ### most of time you can just ignore below self.func

    def order_errors(self, qty, symbol, prc = None):
        """
        检查函数
        用于检查下单量是否符合交易所规则
        """
        if qty < float(self.symbol_info[symbol]['minQty']):
            print('not enough to sell')
            return False
        if prc is None: return True
        if qty * prc < float(self.symbol_info[symbol]['minNotional']):
            print('qty*prc too small')
            return False
        return True

    def get_time_diff(self):
        """
        用于获取交易所延迟的函数
        - request_time_cost: 是我们开始向交易所请求，交易所向我们返回值结束这一整个过程的耗时
        - arrival_time_cost: 我们发送指令的那一刻与指令到达交易所时交易所时间的差值，我们通常更关注这个
                             差值通常有两个部分组成：指令发送过程中的时间，交易所推送服务器与本地服务器的时间戳可能不同步（由交易所特性决定
        """
        start_time = int(time.time() * 1000)
        z = self.client.get_server_time()['serverTime']
        end_time = int(time.time() * 1000)

        request_time_cost = end_time - start_time
        arrival_time_cost = z - start_time

        print('request time cost is ', request_time_cost, 'ms')
        return arrival_time_cost
