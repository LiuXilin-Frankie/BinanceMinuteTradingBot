import datetime
import pymysql

'''
before conversion, run Data_to_SQL.py to store the data

and this file is to read the data from Mysql and convert it to the dict type
'''

# connect to your database and get open,high,low, close, volume data
db = pymysql.connect(host = '127.0.0.1', user = 'root', passwd = 'root', db = 'CryptoCurrency',
                     charset = 'utf8')


class Data_conversion(object):

    def get_data(self, symbol: str, use_frequency: str, start_time: str,
                 end_time: str):
        '''
        get the history kline data of symbol from start_time to end_time with use_frequency

        :params symbol: code
        :params use_frequency: choose from '1m' or '5m'
        :params start_time : starting time to backtesting eg: '2018-01-14 08:00:00'
        :params end_time : ending time to backtesting eg: '2018-01-14 08:00:00'

        '''
        db.ping(reconnect = True)
        cursor = db.cursor()

        sql = "SELECT * FROM %s  where code = '%s' and time >= '%s' and time <= '%s' order by time asc" % (
            use_frequency, symbol, start_time, end_time)

        cursor.execute(sql)
        data_set = cursor.fetchall()

        if len(data_set) == 0:
            print("No data!")
            raise Exception

        # data dict
        self.kline_history_backtest = {}
        self.kline_history_backtest[symbol] = []
        self.time_index = {}

        # similar to the live data but filter something not used
        for i in range(len(data_set)):
            self.kline_history_backtest[symbol].append({"e": "kline", "E": data_set[i][0], "s": symbol,
                                                        "k": {"o": str(data_set[i][2]), "h": str(
                                                            data_set[i][3]), "l": str(data_set[i][4]),
                                                              "c": str(data_set[i][5]),
                                                              "v": str(data_set[i][6])}})
            self.time_index[data_set[i][0]] = i

        cursor.close()
        db.close()

    def get_market_price_trade(self, time: datetime.datetime, symbol, n: int = 1):
        '''

        if at time T generate the buy or sell signal, then buy or sell at T+n at its close price
        return the trading price and trading time
        '''

        price = float(self.kline_history_backtest[symbol][self.time_index[time] + n]["k"]["c"])
        return price, self.kline_history_backtest[symbol][self.time_index[time] + n]["E"]

    def get_market_price_now(self, time: datetime.datetime, symbol):

        price = float(self.kline_history_backtest[symbol][self.time_index[time]]["k"]["c"])
        return price


# test
symbol = 'LTCUSDT'
start_time = '2018-01-14 08:00:00'
end_time = '2018-01-14 08:02:00'
use_frequency = '1m'

dc = Data_conversion()
dc.get_data(symbol, use_frequency, start_time, end_time)
price, trade_time = dc.get_market_price(dc.kline_history_backtest[symbol][1]["E"], symbol, 1)