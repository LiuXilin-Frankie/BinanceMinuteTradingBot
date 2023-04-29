from DataHandler import DataHandler
from Account import Account
from typing import List
from abc import abstractmethod, ABCMeta
import datetime
from Order_Execution import OrderExecutionHandler
from Strategy_BackTest import *


class BackTest:
    def __init__(self, strategy, order_execution_handler: OrderExecutionHandler, stop_time_length_min: int):

        self.strategy = strategy
        self.order_execution_handler = order_execution_handler
        self.stop_time_length_min = stop_time_length_min # if the strategy reach the profit or loss line, then stop for stop_time_length_min minutes

    def run_strategy(self):
        while True:
            if self.strategy.continue_backtest:
                order, time, warning_signal = self.strategy.start_run()
                print(order)
                if time == None:  # means already reach the end date of the backtest
                    self.strategy.continue_backtest = False
                    break
                elif order != {}: # means having order to be sent
                    self.order_execution_handler.execute(order, time, warning_signal)
            else:
                if self.rerun_from_stop() != None:
                    break
                else:
                    continue

    def rerun_from_stop(self):
        # stop the strategy but update data
        for i in range(self.stop_time_length_min):
            _, date_time = self.strategy.dh.update_data()
        if date_time != None:  # backtest done
            self.strategy.continue_backtest = True
            # reset the balance_init
            self.strategy.account.balance_init = self.strategy.account.balance
        else:
            return 0

# test

# could be changed
# trading_symbols = ['ADAUSDT', 'BTCUSDT']
# # 'BATUSDT', 'BNBUSDT',
# start_time = '2021-01-14 08:00:00'
# end_time = '2021-01-14 12:02:00'
#
# use_frequency = '1m'
# dc = DataHandler(symbols = trading_symbols)
# dc.get_all_data(use_frequency, start_time, end_time)
#
# account = Account(balance_init = 100000, start_time = datetime.datetime(2021, 1, 14, 9, 00),
#                   end_time = datetime.datetime(2021, 1, 14, 11, 00), stop_loss_rate = -0.1, stop_profit_rate = 0.2)
# # a = strategy_DualMA(dc, start_time = datetime.datetime(2021, 1, 14, 9, 00),
# #                     end_time = datetime.datetime(2021, 1, 14, 11, 50), trading_symbols = trading_symbols,
# #                     account = account, long_term = 20, short_term = 5, quantity = 1)
#
# # a = strategy_DualThrust(dc, start_time = datetime.datetime(2021, 1, 14, 9, 00),
# #                         end_time = datetime.datetime(2021, 1, 14, 11, 50), trading_symbols = trading_symbols,
# #                         account = account, n1 = 10, n2 = 5, k1 = 0.2, k2 = 0.2, quantity = 1)
#
# a = strategy_R_Breaker(dc, start_time = datetime.datetime(2021, 1, 14, 9, 00),
#                         end_time = datetime.datetime(2021, 1, 14, 11, 50), trading_symbols = trading_symbols,
#                         account = account, n1 = 20, n2 = 10, quantity = 1)
#
# order_execution_handler = OrderExecutionHandler(dc, account, delay_min = 1)
# BackTest(a, order_execution_handler, 20).run_strategy()
#
