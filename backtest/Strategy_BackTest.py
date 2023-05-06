from DataHandler import DataHandler
from Account import Account
from typing import List
from abc import abstractmethod, ABCMeta
import datetime

'''
There are 3 strategies here temporarily: DualMA, DualThrust, and R_Breaker inherited from
Strategy_BackTest object, and they would send orders through method start run
'''


class Strategy_BackTest(metaclass = ABCMeta):
    def __init__(self, strategy_name, dh: DataHandler, start_time: datetime.datetime, end_time: datetime.datetime,
                 trading_symbols: List, account: Account):
        self.strategy_name = strategy_name
        self.symbols = trading_symbols
        self.start_time = start_time
        self.end_time = end_time
        self.account = account
        # get iter of datetime to backtest
        self.dh = dh
        self.dh.generate_backtest_datetime_iter(self.start_time, self.end_time)

        # action
        self.long_action = 'Long'
        self.short_action = 'Short'

        # initial status
        self.continue_backtest = True

        # 
        for symbol in self.symbols:
            self.account.position[symbol] = 0
            self.account.buy_time[symbol] = []
            self.account.buy_num[symbol] = []
            self.account.buy_price[symbol] = []
            self.account.sell_time[symbol] = []
            self.account.sell_num[symbol] = []
            self.account.sell_price[symbol] = []

    @abstractmethod
    def start_run(self):
        pass


class strategy_DualMA(Strategy_BackTest):
    def __init__(self, strategy_name, dh: DataHandler, start_time: datetime.datetime, end_time: datetime.datetime,
                 trading_symbols: List,
                 account: Account, long_term: int, short_term: int, quantity = 1):
        '''

        Dual MA strategy: if MA(short term)> MA(long term), then long the symbol else short
        if signal occurs then net short or long quantity unit symbol
        '''
        super().__init__(strategy_name, dh, start_time, end_time, trading_symbols, account)
        self.long_term = long_term
        self.short_term = short_term
        self.quantity = quantity
        # first update data in order to get signal
        for i in range(self.long_term * 2):
            self.dh.update_data()

    def start_run(self):
        order = {}
        update_symbols, date_time = self.dh.update_data()

        if update_symbols != None:
            use_kline_history = self.dh.get_latest_use_data(update_symbols, n = self.long_term + 2)
            warning_signal = self.account.Check_Warning(date_time, self.dh)

            if warning_signal == None:
                for symbol in use_kline_history.keys():
                    # get the mean close price
                    short_term_mean_now = sum(
                        [kline['k']["c"] for kline in use_kline_history[symbol][-self.short_term:]]) / self.short_term
                    long_term_mean_now = sum(
                        [kline['k']["c"] for kline in use_kline_history[symbol][-self.long_term:]]) / self.long_term
                    short_term_mean_last_minute = sum(
                        [kline['k']["c"] for kline in
                         use_kline_history[symbol][-self.short_term - 1:-1]]) / self.short_term
                    long_term_mean_last_minute = sum(
                        [kline['k']["c"] for kline in
                         use_kline_history[symbol][-self.long_term - 1:-1]]) / self.long_term

                    # long action
                    if (short_term_mean_now > long_term_mean_now) and (
                            long_term_mean_last_minute > short_term_mean_last_minute):
                        # if short position:
                        if self.account.position[symbol] < 0:
                            # consider the delay, the price make change when we trade, so check if the balance could buy 1 more unit

                            if self.account.balance > (-self.account.position[symbol] + self.quantity + 1) * \
                                    use_kline_history[symbol][-1]['k']["c"]:
                                order[symbol] = {}
                                order[symbol]['action'] = self.long_action
                                order[symbol]['quantity'] = self.quantity - self.account.position[symbol]
                            else:
                                print('Not enough Money!')
                                return {}, date_time, warning_signal

                        elif self.account.position[symbol] == 0:
                            if self.account.balance > (self.quantity + 1) * use_kline_history[symbol][-1]['k']["c"]:
                                order[symbol] = {}
                                order[symbol]['action'] = self.long_action
                                order[symbol]['quantity'] = self.quantity
                            else:
                                print('Not enough Money!')
                                return {}, date_time, warning_signal

                    # short action
                    elif (short_term_mean_now < long_term_mean_now) and (
                            long_term_mean_last_minute < short_term_mean_last_minute):
                        # if long position:
                        if self.account.position[symbol] > 0:
                            order[symbol] = {}
                            order[symbol]['action'] = self.short_action
                            order[symbol]['quantity'] = self.quantity + self.account.position[symbol]

                        elif self.account.position[symbol] == 0:
                            order[symbol] = {}
                            order[symbol]['action'] = self.short_action
                            order[symbol]['quantity'] = self.quantity


            elif warning_signal == -1 or warning_signal == 1:
                # reach the loss or profit line
                self.continue_backtest = False
                return self.account.close_position(), date_time, warning_signal

        return order, date_time, None  # no update data or no action generated


class strategy_DualThrust(Strategy_BackTest):
    def __init__(self, strategy_name, dh: DataHandler, start_time: datetime.datetime, end_time: datetime.datetime,
                 trading_symbols: List, account: Account, n1: int, n2: int, k1: float, k2: float, quantity: int):

        '''
        :params n1: use T-n1-n2 ~ T-n2-1 history minute bars (n1 in total) as the baselines to generate the range
        :params n2: use T-n2 history minute bar's open price to generate the signal
        :params k1: parameter for the buy line
        :params k2: parameter for the sell line
        '''

        super().__init__(strategy_name, dh, start_time, end_time, trading_symbols, account)
        self.n1 = n1
        self.n2 = n2
        self.k1 = k1
        self.k2 = k2
        self.quantity = quantity
        # first update data in order to get signal
        for i in range((self.n1 + self.n2) * 2):
            self.dh.update_data()

    def start_run(self):
        order = {}
        update_symbols, date_time = self.dh.update_data()

        if update_symbols != None:
            use_kline_history = self.dh.get_latest_use_data(update_symbols, n = self.n1 + self.n2 + 2)
            warning_signal = self.account.Check_Warning(date_time, self.dh)

            if warning_signal == None:
                for symbol in use_kline_history.keys():
                    use_klines = use_kline_history[symbol][-self.n1 - self.n2:-self.n2]
                    HH = max([kline['k']["h"] for kline in use_klines])
                    HC = max([kline['k']["c"] for kline in use_klines])
                    LC = min([kline['k']["c"] for kline in use_klines])
                    LL = min([kline['k']["l"] for kline in use_klines])
                    range = max(HH - LC, HC - LL)
                    buy_line = use_kline_history[symbol][-self.n2]["k"]["o"] + range * self.k1
                    sell_line = use_kline_history[symbol][-self.n2]["k"]["o"] - range * self.k2

                    # long action
                    if use_kline_history[symbol][-1]["k"]["c"] > buy_line:
                        # if short position:
                        if self.account.position[symbol] < 0:
                            # consider the delay, the price make change when we trade, so check if the balance could buy 1 more unit
                            if self.account.balance > (-self.account.position[symbol] + self.quantity + 1) * \
                                    use_kline_history[symbol][-1]["k"]["c"]:
                                order[symbol] = {}
                                order[symbol]['action'] = self.long_action
                                order[symbol]['quantity'] = self.quantity - self.account.position[symbol]

                            else:
                                print('Not enough Money!')
                                return {}, date_time, warning_signal

                        elif self.account.position[symbol] == 0:
                            if self.account.balance > (self.quantity + 1) * use_kline_history[symbol][-1]["k"]["c"]:
                                order[symbol] = {}
                                order[symbol]['action'] = self.long_action
                                order[symbol]['quantity'] = self.quantity
                            else:
                                print('Not enough Money!')
                                return {}, date_time, warning_signal
                        elif self.account.position[symbol] > 0:
                            continue

                    # short action
                    elif use_kline_history[symbol][-1]["k"]["c"] < sell_line:
                        # if long position:
                        if self.account.position[symbol] > 0:
                            order[symbol] = {}
                            order[symbol]['action'] = self.short_action
                            order[symbol]['quantity'] = self.quantity + self.account.position[symbol]

                        elif self.account.position[symbol] == 0:
                            order[symbol] = {}
                            order[symbol]['action'] = self.short_action
                            order[symbol]['quantity'] = self.quantity

                        elif self.account.position[symbol] < 0:
                            continue

            elif warning_signal == -1 or warning_signal == 1:
                # reach the loss or profit line
                self.continue_backtest = False
                return self.account.close_position(), date_time, warning_signal

        return order, date_time, None  # no update data or no action generated


class strategy_R_Breaker(Strategy_BackTest):

    def __init__(self, strategy_name, dh: DataHandler, start_time: datetime.datetime, end_time: datetime.datetime,
                 trading_symbols: List, account: Account, n1: int, n2: int, quantity: int):
        '''
        we don't use the prices last day, we use the prices of T-n1-n2 ~ T-n2-1 history minute bars.
    
        :params n1: use T-n1-n2 ~ T-n2-1 history minute bars (n1 in total) as the baselines to generate the range
        :params n2: use T-n2~T history minute bars to compare with the range
        '''

        super().__init__(strategy_name, dh, start_time, end_time, trading_symbols, account)
        self.n1 = n1
        self.n2 = n2
        self.quantity = quantity

        # first update data in order to get signal
        for i in range((self.n1 + self.n2) * 2):
            self.dh.update_data()

    def start_run(self):

        order = {}
        update_symbols, date_time = self.dh.update_data()

        if update_symbols != None:
            use_kline_history = self.dh.get_latest_use_data(update_symbols, n = self.n1 + self.n2 + 2)
            warning_signal = self.account.Check_Warning(date_time, self.dh)

            if warning_signal == None:
                for symbol in use_kline_history.keys():
                    use_klines = use_kline_history[symbol][-self.n1 - self.n2:-self.n2]

                    high = max([kline["k"]["h"] for kline in use_klines])
                    low = min([kline["k"]["l"] for kline in use_klines])
                    close = use_kline_history[symbol][-self.n2 - 1]["k"]["c"]

                    pivot = (high + low + close) / 3
                    buyBreak = high + 2 * (pivot - low)
                    sellSetup = pivot + (high - low)
                    turnToShort = 2 * pivot - low
                    turnToLong = 2 * pivot - high
                    buySetup = pivot - (high - low)
                    sellBreak = low - 2 * (high - pivot)

                    # not long or short position : trend strategy
                    if self.account.position[symbol] == 0:
                        if use_kline_history[symbol][-1]["k"]["c"] > buyBreak:
                            if self.account.balance > (self.quantity + 1) * use_kline_history[symbol][-1]["k"]["c"]:
                                order[symbol] = {}
                                order[symbol]['action'] = self.long_action
                                order[symbol]['quantity'] = self.quantity + self.account.position[symbol]

                            else:
                                print('Not enough Money!')
                                return {}, date_time, warning_signal

                        elif use_kline_history[symbol][-1]["k"]["c"] < sellBreak:
                            order[symbol] = {}
                            order[symbol]['action'] = self.short_action
                            order[symbol]['quantity'] = self.quantity

                    # long or short position: reversal strategy
                    elif self.account.position[symbol] > 0:
                        if (max([kline["k"]["h"] for kline in use_kline_history[symbol][-self.n2:]]) > sellSetup) and (
                                use_kline_history[symbol][-1]["k"]["c"] < turnToShort):
                            # short signal
                            order[symbol] = {}
                            order[symbol]['action'] = self.short_action
                            order[symbol]['quantity'] = self.quantity + self.account.position[symbol]

                    elif self.account.position[symbol] < 0:
                        if (min([kline["k"]["l"] for kline in use_kline_history[symbol][-self.n2:]]) < buySetup) and (
                                use_kline_history[symbol][-1]["k"]["c"] > turnToLong):
                            if self.account.balance > (-self.account.position[symbol] + self.quantity + 1) * \
                                    use_kline_history[symbol][-1]["k"]["c"]:
                                order[symbol] = {}
                                order[symbol]['action'] = self.long_action
                                order[symbol]['quantity'] = self.quantity - self.account.position[symbol]

                            else:
                                print('Not enough Money!')
                                return {}, date_time, warning_signal

            elif warning_signal == -1 or warning_signal == 1:
                # reach the loss or profit line
                self.continue_backtest = False
                return self.account.close_position(), date_time, warning_signal

        return order, date_time, None  # no update data or no action generated
