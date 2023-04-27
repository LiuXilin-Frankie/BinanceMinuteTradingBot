import datetime
from pandas import DataFrame
import numpy as np
import pandas as pd


class Account:
    def __init__(self, balance_init, start_time, end_time, buy_cost_rate = 0, sell_cost_rate = 0,
                 stop_loss_rate = -0.03,stop_profit_rate = 0.05):

        self.balance_init = balance_init
        self.balance = balance_init  # initial balance
        self.position_value = 0
        self.netValue = self.balance + self.position_value
        self.buy_time = {}
        self.sell_time = {}
        self.buy_price = {}
        self.sell_price = {}
        self.buy_num = {}
        self.sell_num = {}
        self.start_time = start_time
        self.end_time = end_time
        self.position = {}
        self.stop_loss_time = []
        self.stop_profit_time = []
        self.buy_cost_rate = buy_cost_rate
        self.sell_cost_rate = sell_cost_rate
        self.stop_loss_rate = stop_loss_rate
        self.stop_profit_rate = stop_profit_rate

        # self.info = pd.DataFrame(
        #     columns = ['code', 'buy_price', 'buy_time', 'buy_num', 'sell_price', 'sell_time', 'sell_num'])

    def buy(self, buy_time, symbol, buy_price, buy_num):
        if symbol not in self.buy_time.keys():
            self.position[symbol] = buy_num
            self.buy_num[symbol] = []
            self.buy_num[symbol].append(buy_num)
            self.buy_price[symbol] = []
            self.buy_price[symbol].append(buy_price)
            self.buy_time[symbol] = []
            self.buy_time[symbol].append(buy_time)
        else:
            self.position[symbol] += buy_num
            self.buy_num[symbol].append(buy_num)
            self.buy_price[symbol].append(buy_price)
            self.buy_time[symbol].append(buy_time)

        self.balance -= buy_price * buy_num * (1 + self.buy_cost_rate)

    def sell(self, sell_time, symbol, sell_price, sell_num):
        if symbol not in self.sell_time.keys():
            self.position[symbol] = -sell_num
            self.sell_num[symbol] = []
            self.sell_num[symbol].append(sell_num)
            self.sell_price[symbol] = []
            self.sell_price[symbol].append(sell_price)
            self.sell_time[symbol] = []
            self.sell_time[symbol].append(sell_time)
        else:
            self.position[symbol] -= sell_num
            self.sell_num[symbol].append(sell_num)
            self.sell_price[symbol].append(sell_price)
            self.sell_time[symbol].append(sell_time)

        self.balance += sell_price * sell_num * (1 - self.sell_cost_rate)

    def update_net_value(self, time: datetime.datetime, dc):
        for symbol in self.position.keys():
            market_price = dc.get_market_price_now(time, symbol)
            self.position_value = self.position[symbol] * market_price

        self.netValue = self.balance + self.position_value
        return self.netValue

    def Check_Warning(self, time: datetime.datetime, dc):
        self.update_net_value(time, dc)
        if self.netValue < self.balance_init * (1 + self.stop_loss_rate):
            print("Reach the stop loss line. Stop trading!")
            return -1

        elif self.netValue > self.balance_init * (1 + self.stop_profit_rate):
            print("Reach the stop profit line. Could consider closing out the positions and leave.")
            return 1

        else:
            return True

    def close_position(self, time, dc, signal: int, n: int = 1):
        '''
        close all the position, and return the remain balance

        :params signal: 1 is stop from profit and -1 is stop from loss
        :params n: consider the delay, trading at T+n minute
        '''
        operation_time = time + datetime.timedelta(minutes = n) # trade done at this time, not the signal generation time
        if signal == 1:
            self.stop_profit_time.append(operation_time)
        elif signal == -1:
            self.stop_loss_time.append(operation_time)

        for symbol in self.position.keys():
            if self.position[symbol] > 0:
                sell_price, sell_time = dc.get_market_price_trade(time, symbol, n)
                self.sell(sell_time, symbol, sell_price, self.position[symbol])
            elif self.position[symbol] < 0:
                buy_price, buy_time = dc.get_market_price_trade(time, symbol, n)
                self.buy(buy_time, symbol, buy_price, -self.position[symbol])

        self.update_net_value(operation_time, dc)
        return self.balance

    def get_all_trading_info(self) -> DataFrame :
        pass
