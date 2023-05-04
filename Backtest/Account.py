import datetime
from pandas import DataFrame
from DataHandler import DataHandler
import pandas as pd
from Evaluation import Evaluation

'''
this class would record all the trading information.
'''


class Account:
    def __init__(self, balance_init, start_time, end_time, buy_cost_rate = 0.0001, sell_cost_rate = 0.0001,
                 stop_loss_rate = -0.1, stop_profit_rate = 0.2):

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
        self.netValue_time_series = {}  # record the change of netvalue

        # self.info = pd.DataFrame(
        #     columns = ['code', 'buy_price', 'buy_time', 'buy_num', 'sell_price', 'sell_time', 'sell_num'])

    def buy(self, buy_time, symbol, buy_price, buy_num):
        self.position[symbol] += buy_num
        self.buy_num[symbol].append(buy_num)
        self.buy_price[symbol].append(buy_price)
        self.buy_time[symbol].append(buy_time)

        self.balance -= buy_price * buy_num * (1 + self.buy_cost_rate)

    def sell(self, sell_time, symbol, sell_price, sell_num):

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
        self.netValue_time_series[time] = self.netValue
        return self.netValue

    def Check_Warning(self, time: datetime.datetime, dh: DataHandler):
        '''
        check if reach the profit or loss line
        '''

        self.update_net_value(time, dh)
        if self.netValue < self.balance_init * (1 + self.stop_loss_rate):
            print("Reach the stop loss line. Stop trading!")
            return -1

        elif self.netValue > self.balance_init * (1 + self.stop_profit_rate):
            print("Reach the stop profit line. Could consider closing out the positions and leave.")
            return 1

        else:
            return None

    def close_position(self):
        '''
        send order to close out all the positions
        '''

        order = {}
        for symbol in self.position.keys():
            order[symbol] = {}
        for symbol in self.position.keys():
            if self.position[symbol] > 0:
                order[symbol]['action'] = 'Short'
                order[symbol]['quantity'] = self.position[symbol]
            elif self.position[symbol] < 0:
                order[symbol]['action'] = 'Long'
                order[symbol]['quantity'] = -self.position[symbol]

        return order

    def get_all_trading_info(self) -> DataFrame:
        '''
        get trading info of all backtesting period
        '''

        # index is symbol
        buy_time_df = pd.DataFrame(data = self.buy_time.values(), index = list(self.buy_time.keys())).stack().droplevel(
            level = 1)
        buy_num_df = pd.DataFrame(data = self.buy_num.values(), index = list(self.buy_time.keys())).stack().droplevel(
            level = 1)
        buy_price_df = pd.DataFrame(data = self.buy_price.values(),
                                    index = list(self.buy_time.keys())).stack().droplevel(level = 1)
        buy_info = pd.concat([buy_time_df, buy_num_df, buy_price_df], axis = 1)
        buy_info['action'] = 'buy'
        buy_info.columns = ['time', 'num', 'price', 'action']
        sell_time_df = pd.DataFrame(data = self.sell_time.values(),
                                    index = list(self.sell_time.keys())).stack().droplevel(level = 1)
        sell_num_df = pd.DataFrame(data = self.sell_num.values(),
                                   index = list(self.sell_time.keys())).stack().droplevel(level = 1)
        sell_price_df = pd.DataFrame(data = self.sell_price.values(),
                                     index = list(self.sell_time.keys())).stack().droplevel(level = 1)
        sell_info = pd.concat([sell_time_df, sell_num_df, sell_price_df], axis = 1)
        sell_info['action'] = 'sell'
        sell_info.columns = ['time', 'num', 'price', 'action']
        all_trading_info = pd.concat([buy_info, sell_info])
        all_trading_info = all_trading_info.reset_index(drop = False).set_index('time').sort_index()
        all_trading_info.rename(columns = {'index': 'code'}, inplace = True)

        stop_loss_df = pd.DataFrame(index = self.stop_loss_time, data = 1, columns = ["stop_loss"])
        stop_profit_df = pd.DataFrame(index = self.stop_profit_time, data = 1, columns = ["stop_profit"])

        all_trading_info = pd.concat([all_trading_info, stop_loss_df, stop_profit_df], join = 'outer',axis = 1).fillna(0)
        return all_trading_info

    def get_netvalue_time_series(self) -> DataFrame:
        '''
        record the changing of netvalue
        '''

        nav = (pd.DataFrame(index = list(self.netValue_time_series.keys()),
                            data = self.netValue_time_series.values()).stack().droplevel(level = 1).to_frame())
        nav.columns = ['net_value']
        return nav

    def get_evaluation(self, strategy_name, period_num) -> DataFrame:
        nav = self.get_netvalue_time_series()
        sharpe_ratio = Evaluation.get_shape_ratio(nav, period_num)
        max_drawdown, drawdown_duration = Evaluation.get_max_drawdown(nav)
        evaluation = pd.DataFrame(index = ['sharpe_ratio', 'max_drawdown', 'drawdown_duration'],
                                  columns = [strategy_name], data = [sharpe_ratio, max_drawdown, drawdown_duration])
        return evaluation
