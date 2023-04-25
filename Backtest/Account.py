import datetime

import numpy as np
import pandas as pd
from Data_conversion import Data_conversion

dc = Data_conversion()


class Account:
    def __init__(self, balance_init, start_time, end_time, stop_loss_rate = -0.03, stop_profit_rate = 0.05):
        self.balance_init = balance_init
        self.balance = balance_init  # initial balance
        self.postion_value = 0
        self.netValue = self.cash + self.postion_value
        self.buy_time = {}
        self.sell_time = {}
        self.buy_price = {}
        self.sell_price = {}
        self.start_time = start_time
        self.end_time = end_time
        self.position = {}
        self.buy_cost_rate = 0
        self.sell_cost_rate = 0
        self.stop_loss_rate = stop_loss_rate
        self.stop_profit_rate = stop_profit_rate

        # self.info = pd.DataFrame(
        #     columns = ['code', 'buy_price', 'buy_time', 'buy_num', 'sell_price', 'sell_time', 'sell_num'])

    def buy(self, buy_time, symbol, buy_price, buy_num):
        if symbol not in self.position.keys():
            self.position[symbol] = buy_num
            self.buy_price[symbol] = []
            self.buy_price[symbol].append(buy_price)
            self.buy_time[symbol] = []
            self.buy_time[symbol].append(buy_time)
        else:
            self.position[symbol] += buy_num
            self.buy_price[symbol].append(buy_price)
            self.buy_time[symbol].append(buy_time)

        self.cash -= buy_price * buy_num * (1 + self.buy_cost_rate)

    def sell(self, sell_time, symbol, sell_price, sell_num):
        if symbol not in self.position.keys():
            self.position[symbol] = -sell_num
            self.sell_price[symbol] = []
            self.sell_price[symbol].append(sell_price)
            self.sell_time[symbol] = []
            self.sell_time[symbol].append(sell_time)
        else:
            self.position[symbol] -= sell_num
            self.sell_price[symbol].append(sell_price)
            self.sell_time[symbol].append(sell_time)

        self.cash += sell_price * sell_num * (1 - self.sell_cost_rate)

    def update_net_value(self, time: datetime.datetime):
        for symbol in self.position.keys():
            market_price = dc.get_market_price_now(time, symbol)
            self.postion_value += self.position[symbol] * market_price

        self.netValue = self.cash + self.postion_value
        return self.netValue

    def Check_Warning(self):
        if self.netValue < self.balance_init * (1 + self.stop_loss_rate):
            print("Reach the stop loss line. Stop trading!")

        elif self.netValue > self.balance_init * (1 + self.stop_profit_rate):
            print("Reach the stop profit line. Could consider closing out the positions and leave.")
