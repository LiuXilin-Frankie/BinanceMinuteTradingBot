import pandas as pd

from Order_Execution import OrderExecutionHandler
from Strategy_BackTest import *
from BackTest import BackTest

# test

# could be changed
trading_symbols = ['ADAUSDT', 'BATUSDT', 'BNBUSDT']
# 'BATUSDT', 'BNBUSDT','BTCUSDT'
start_time = '2021-01-14 08:00:00'
end_time = '2021-01-14 12:02:00'

use_frequency = '1m'
dh = DataHandler(symbols = trading_symbols)


dh.get_all_data(use_frequency, start_time, end_time)

start_time_backtest = datetime.datetime(2021, 1, 14, 9, 00)
end_time_backtest = datetime.datetime(2021, 1, 14, 11, 50)

account = Account(balance_init = 100000, start_time = start_time_backtest,
                  end_time = end_time_backtest, stop_loss_rate = -0.0001, stop_profit_rate = 0.2)

strategy = strategy_DualMA('DualMA', dh, start_time = start_time_backtest,
                           end_time = end_time_backtest, trading_symbols = trading_symbols,
                           account = account, long_term = 10, short_term = 5, quantity = 10)

# strategy = strategy_DualThrust('DualThrust',dh, start_time = start_time_backtest,
#                                end_time = end_time_backtest, trading_symbols = trading_symbols,
#                                account = account, n1 = 20, n2 = 10, k1 = 0.2, k2 = 0.2, quantity = 10)

# strategy = strategy_R_Breaker('R_Breaker',dh, start_time = start_time_backtest,
#                               end_time = end_time_backtest, trading_symbols = trading_symbols,
#                               account = account, n1 = 20, n2 = 10, quantity = 10)

order_execution_handler = OrderExecutionHandler(dh, account, delay_min = 1)
BackTest(strategy, order_execution_handler, 20).run_strategy()
netvalue = strategy.account.get_netvalue_time_series()
trading_info = strategy.account.get_all_trading_info()
eval = account.get_evaluation(strategy.strategy_name, 365 * 24 * 60)