from Data_conversion import dc
from Account import Account
from typing import List
from abc import abstractmethod, ABCMeta
import datetime

# could be changed
trading_symbols = ['ADAUSDT', 'BATUSDT', 'BNBUSDT']
start_time = '2021-01-14 08:00:00'
end_time = '2021-01-14 12:02:00'

use_frequency = '1m'

# get history kline to backtest
for symbol in trading_symbols:
    dc.get_data(symbol, use_frequency, start_time, end_time)
history_kline = dc.kline_history_backtest


class Strategy_BackTest(metaclass = ABCMeta):
    def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime, trading_symbols: List,
                 account: Account,
                 delay_min: int):
        self.symbols = trading_symbols
        self.start_time = start_time
        self.end_time = end_time
        self.account = account
        self.delay_min = delay_min  # signal generated at T and trade at T+delay_min

    @abstractmethod
    def start_run(self):
        pass

    @abstractmethod
    def rerun_from_stop(self, stop_time: datetime.datetime, stop_time_length_min: int):
        pass


class BackTest:
    def run_strategy(self, strategy, stop_time_length_min: int):
        status, time = strategy.start_run()
        while status == -1:
            status, time = strategy.rerun_from_stop(time, stop_time_length_min)


#
class strategy_DualMA(Strategy_BackTest):
    def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime, trading_symbols: List,
                 account: Account, long_term: int, short_term: int, delay_min = 1, quantity = 1):
        '''

        Dual MA strategy: if MA(short term)> MA(long term), then long the symbol else short
        if signal occurs then net short or long quantity unit symbol
        '''
        super().__init__(start_time, end_time, trading_symbols, account, delay_min)
        self.long_term = long_term
        self.short_term = short_term
        self.quantity = quantity
        for symbol in self.symbols:
            self.account.position[symbol] = 0

    def start_run(self):
        for date_time in history_kline.keys():
            if date_time >= self.start_time and date_time <= self.end_time:
                print(date_time)
                signal = self.account.Check_Warning(date_time, dc)
                if signal == True:
                    index = list(history_kline.keys()).index(date_time)
                    for symbol in self.symbols:
                        # get the mean close price
                        short_term_mean_now = sum([float(history_kline[x][symbol]['k']["c"]) for x in
                                                   list(history_kline.keys())[
                                                   index + 1 - self.short_term:index + 1]]) / self.short_term
                        long_term_mean_now = sum([float(history_kline[x][symbol]['k']["c"]) for x in
                                                  list(history_kline.keys())[
                                                  index + 1 - self.long_term:index + 1]]) / self.long_term

                        short_term_mean_last_minute = sum([float(history_kline[x][symbol]['k']["c"]) for x in
                                                           list(history_kline.keys())[
                                                           index - self.short_term:index]]) / self.short_term
                        long_term_mean_last_minute = sum([float(history_kline[x][symbol]['k']["c"]) for x in
                                                          list(history_kline.keys())[
                                                          index - self.long_term:index]]) / self.long_term

                        if (short_term_mean_now > long_term_mean_now) and (
                                long_term_mean_last_minute > short_term_mean_last_minute):
                            # if short position:

                            if self.account.position[symbol] < 0:
                                # consider the delay, the price make change when we trade, so check if the balance could buy 1 more unit

                                if self.account.balance > (self.account.position[symbol] + self.quantity + 1) * float(
                                        history_kline[date_time][symbol]['k']["c"]):
                                    buy_price, buy_time = dc.get_market_price_trade(date_time, symbol, self.delay_min)
                                    self.account.buy(date_time, symbol, buy_price,
                                                     self.quantity + self.account.position[symbol])
                                else:
                                    print('Not enough Money!')

                            elif self.account.position[symbol] == 0:
                                if self.account.balance > (self.quantity + 1) * float(
                                        history_kline[date_time][symbol]['k']["c"]):
                                    buy_price, buy_time = dc.get_market_price_trade(date_time, symbol, self.delay_min)
                                    self.account.buy(date_time, symbol, buy_price, self.quantity)
                                else:
                                    print('Not enough Money!')


                        elif (short_term_mean_now < long_term_mean_now) and (
                                long_term_mean_last_minute < short_term_mean_last_minute):
                            # if long position:
                            if self.account.position[symbol] > 0:
                                sell_price, sell_time = dc.get_market_price_trade(date_time, symbol, self.delay_min)
                                self.account.sell(date_time, symbol, sell_price,
                                                  self.quantity + self.account.position[symbol])

                            elif self.account.position[symbol] == 0:
                                sell_price, sell_time = dc.get_market_price_trade(date_time, symbol, self.delay_min)
                                self.account.sell(date_time, symbol, sell_price, self.quantity)

                    continue
                elif signal == -1:
                    self.account.close_position(date_time, dc, signal, self.delay_min)
                    break
                elif signal == 1:
                    self.account.close_position(date_time, dc, signal, self.delay_min)
                    break
            if date_time == self.end_time:  # test done
                return 0, date_time

        return -1, date_time  # reach stop line

    def rerun_from_stop(self, stop_time: datetime.datetime, stop_time_length_min: int):
        self.start_time = stop_time + datetime.timedelta(minutes = stop_time_length_min)
        return self.start_run()


account = Account(balance_init = 100000, start_time = datetime.datetime(2021, 1, 14, 9, 00),
                  end_time = datetime.datetime(2021, 1, 14, 11, 00), stop_loss_rate = -0.1, stop_profit_rate = 0.2)
a = strategy_DualMA(start_time = datetime.datetime(2021, 1, 14, 9, 00),
                    end_time = datetime.datetime(2021, 1, 14, 11, 00),
                    trading_symbols = trading_symbols[0:3], account = account, long_term = 20, short_term = 5,
                    delay_min = 1,
                    quantity = 1)
# a.start_run()
BackTest().run_strategy(a, 40)

#
# def strategy_DualThrust(self, n1: int, n2: int, k1: float, k2: float, quantity: int):
#     '''
#     :params n1: use T-n1-n2 ~ T-n2-1 history minute bars (n1 in total) as the baselines to generate the range
#     :params n2: use T-n2 history minute bar's open price to generate the signal
#     :params k1: parameter for the buy line
#     :params k2: parameter for the sell line
#     '''
#
#
# self.update_data()
#
# for symbol in self.symbols:
#     use_klines = history_kline[symbol][-n1 - n2:-n2]
#     HH = max([float(kline['k']["h"]) for kline in use_klines])
#     HC = max([float(kline['k']["c"]) for kline in use_klines])
#     LC = min([float(kline['k']["c"]) for kline in use_klines])
#     LL = min([float(kline['k']["l"]) for kline in use_klines])
#     range = max(HH - LC, HC - LL)
#     buy_line = float(history_kline[symbol][-n2]["k"]["o"]) + range * k1
#     sell_line = float(history_kline[symbol][-n2]["k"]["o"]) - range * k2
#
#     if float(self.klines[symbol]["k"]["c"]) > buy_line:
#         # if short position:
#         if self.position[symbol] < 0:
#             # consider the delay, the price make change when we trade, so check if the balance could buy 1 more unit
#             if self.balance > (self.position[symbol] + quantity + 1) * float(self.klines[symbol]["k"]["c"]):
#                 price = self.market_buy(symbol, self.position[symbol] + quantity)
#                 self.position[symbol] = quantity
#                 self.balance = self.balance - price * (self.position[symbol] + quantity)
#             else:
#                 print('Not enough Money!')
#
#         elif self.position[symbol] == 0:
#             if self.balance > (quantity + 1) * float(self.klines[symbol]["k"]["c"]):
#                 price = self.market_buy(symbol, qty = quantity)
#                 self.position[symbol] = self.position[symbol] + quantity
#                 self.balance = self.balance - price * quantity
#             else:
#                 print('Not enough Money!')
#
#         elif self.position[symbol] > 0:
#             return
#
#     elif float(self.klines[symbol]["k"]["c"]) < sell_line:
#         # if long position:
#         if self.position[symbol] > 0:
#             price = self.market_sell(symbol, self.position[symbol] + quantity)
#             self.position[symbol] = -quantity
#             self.balance = self.balance + price * (self.position[symbol] + quantity)
#
#         elif self.position[symbol] == 0:
#             price = self.market_sell(symbol, qty = quantity)
#             self.position[symbol] = self.position[symbol] - quantity
#             self.balance = self.balance + price * quantity
#
#         elif self.position[symbol] < 0:
#             return
#
#
# def strategy_R_Breaker(self, n1: int, n2: int, quantity: int):
#     '''
#
#     we don't use the prices last day, we use the prices of T-n1-n2 ~ T-n2-1 history minute bars.
#
#     :params n1: use T-n1-n2 ~ T-n2-1 history minute bars (n1 in total) as the baselines to generate the range
#     :params n2: use T-n2~T history minute bars to compare with the range
#     '''
#
#
# self.update_data()
#
# for symbol in self.symbols:
#     use_klines = history_kline[symbol][-n1 - n2:-n2]
#     high = max([float(kline["k"]["h"]) for kline in use_klines])
#     low = min([float(kline["k"]["l"]) for kline in use_klines])
#     close = float(history_kline[symbol][-n2 - 1]["k"]["c"])
#
#     pivot = (high + low + close) / 3
#     buyBreak = high + 2 * (pivot - low)
#     sellSetup = pivot + (high - low)
#     turnToShort = 2 * pivot - low
#     turnToLong = 2 * pivot - high
#     buySetup = pivot - (high - low)
#     sellBreak = low - 2 * (high - pivot)
#
#     # not long or short position : trend strategy
#     if self.position[symbol] == 0:
#         if float(self.klines[symbol]["k"]["c"]) > buyBreak:
#             if self.balance > (quantity + 1) * float(self.klines[symbol]["k"]["c"]):
#                 price = self.market_buy(symbol, qty = quantity)
#                 self.position[symbol] = quantity
#                 self.balance = self.balance - price * quantity
#             else:
#                 print('Not enough Money!')
#
#         elif float(self.klines[symbol]["k"]["c"]) < sellBreak:
#             price = self.market_sell(symbol, qty = quantity)
#             self.position[symbol] = - quantity
#             self.balance = self.balance + price * quantity
#
#     # long or short position: reversal strategy
#     elif self.position[symbol] > 0:
#         if (max(float(kline["k"]["h"]) for kline in history_kline[symbol][-n2:]) > sellSetup) and (
#                 float(self.klines[symbol]["k"]["c"]) < turnToShort):
#             # short signal
#             price = self.market_sell(symbol, self.position[symbol] + quantity)
#             self.position[symbol] = -quantity
#             self.balance = self.balance + price * (self.position[symbol] + quantity)
#
#     elif self.position[symbol] < 0:
#         if (min(float(kline["k"]["l"]) for kline in history_kline[symbol][-n2:]) < buySetup) and (
#                 float(self.klines[symbol]["k"]["c"]) > turnToLong):
#             if self.balance > (self.position[symbol] + quantity + 1) * float(self.klines[symbol]["k"]["c"]):
#                 price = self.market_buy(symbol, self.position[symbol] + quantity)
#                 self.position[symbol] = quantity
#                 self.balance = self.balance - price * (self.position[symbol] + quantity)
#             else:
#                 print('Not enough Money!')
