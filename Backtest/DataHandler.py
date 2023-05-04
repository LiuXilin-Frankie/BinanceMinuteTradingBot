import datetime
import pandas as pd
import pymysql
import datetime
from typing import List

'''
before conversion, run Data_to_SQL.py to store the data

and this file is to read the data from Mysql and convert it to the dict type
'''

# connect to your database and get open,high,low, close, volume data
db = pymysql.connect(host = '127.0.0.1', user = 'root', passwd = 'root', db = 'CryptoCurrency', charset = 'utf8')


class DataHandler:
    def __init__(self, symbols: List):
        # data dict
        self.kline_history_backtest = {}  # the keys is datetime and every datetime is a dict which keys are symbols and the value are also dicts containing data
        self.latest_data = {}
        self.symbols = symbols
        self.datetimelist = []
        self.datetimeiter = iter([])

    def get_all_data(self, use_frequency: str, start_time: str, end_time: str):

        # get trading datetimelist:could be change according to other time interval data
        if use_frequency == "1m":
            self.datetimelist = [datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') for x in
                                 pd.date_range(start = start_time, end = end_time, freq = 'T').tolist()]
        elif use_frequency == "5m":
            self.datetimelist = [datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S') for x in
                                 pd.date_range(start = start_time, end = end_time, freq = '5T').tolist()]
        '''
        get the history kline data of symbol from start_time to end_time with use_frequency :now only could choose from "1m" or "5m"

        :params symbol: code
        :params use_frequency: choose from '1m' or '5m'
        :params start_time : starting time to backtesting eg: '2018-01-14 08:00:00'
        :params end_time : ending time to backtesting eg: '2018-01-14 08:00:00'
        '''
        db.ping(reconnect = True)
        cursor = db.cursor()

        # fetch the data in symbols one by one
        for symbol in self.symbols:
            sql = "SELECT * FROM %s  where code = '%s' and time >= '%s' and time <= '%s' order by time asc" % (
                use_frequency, symbol, start_time, end_time)

            cursor.execute(sql)
            data_set = cursor.fetchall()

            if len(data_set) == 0:
                print("No data!")
                raise Exception

            # similar to the live data but filter something not used every date, keys of self.kline_history_backtest is datetime
            for i in range(len(data_set)):
                if data_set[i][0] not in self.kline_history_backtest.keys():  # time
                    self.kline_history_backtest[data_set[i][0]] = {}

                self.kline_history_backtest[data_set[i][0]][symbol] = []
                self.kline_history_backtest[data_set[i][0]][symbol] = {"e": "kline", "E": data_set[i][0], "s": symbol,
                                                                       "k": {"o": data_set[i][2], "h": data_set[i][3],
                                                                             "l": data_set[i][4], "c": data_set[i][5],
                                                                             "v": data_set[i][6]}}

        cursor.close()
        db.close()

    def get_market_price_trade(self, time: datetime.date, symbol, delay_min: int = 1):
        '''

        if at time T generate the buy or sell signal, then buy or sell at T+n at its close price
        return the trading price and trading time

        :params delay_min: consider the delay, trading at T+n minute

        return the trade price and the trade time
        '''

        try:
            price = self.kline_history_backtest[time + datetime.timedelta(minutes = delay_min)][symbol]["k"]["c"]
            return price, time + datetime.timedelta(minutes = delay_min)
        except:
            print("No price data.")
            raise ValueError

    def get_market_price_now(self, time: datetime.datetime, symbol):
        '''
        get the latest close price

        '''
        price = self.kline_history_backtest[time][symbol]["k"]["c"]
        return price

    def generate_backtest_datetime_iter(self, start_time: datetime.datetime, end_time: datetime.datetime):
        try:
            self.datetimeiter = iter(
                self.datetimelist[self.datetimelist.index(start_time):self.datetimelist.index(end_time) + 1])
        except ValueError:
            print("Historical data couldn't cover this time span!")

    def _get_new_datetime(self):
        return next(self.datetimeiter)

    def get_latest_use_data(self, use_symbol_list, n = 1):
        use_symbol_data = {}
        if use_symbol_list is not None:
            for symbol in use_symbol_list:
                try:  # in case for symbol is not valid
                    use_symbol_data[symbol] = []
                    try:  # in case couldn't get n historical data
                        use_symbol_data[symbol] = self.latest_data[symbol][-n:]
                    except:
                        continue
                except KeyError:
                    print("{symbol} is not a valid symbol.").format(symbol = symbol)

            return use_symbol_data

    def update_data(self):
        '''
        return the update symbol list and the time
        '''
        try:
            datatime = self._get_new_datetime()
            print(datatime)
            if datatime in self.kline_history_backtest.keys():
                update_symbol_list = list(self.kline_history_backtest[datatime].keys())
                for symbol in update_symbol_list:
                    if symbol not in self.latest_data.keys():
                        self.latest_data[symbol] = []
                        self.latest_data[symbol].append(self.kline_history_backtest[datatime][symbol])
                    else:
                        self.latest_data[symbol].append(self.kline_history_backtest[datatime][symbol])
                return update_symbol_list, datatime  # so the strategy will generate action of this symbols
            else:  # if at this time no  data to update due to some errors
                return None, datatime  # that means no update this time

        except StopIteration:  # no data
            print("Backtesting done!")
            return None, None  # so if date_time is None ,means backtest done
