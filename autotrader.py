__author__ = 'AbsoluteX'
__email__ = 'l276660317@gmail.com'

import time
from binance import ThreadedWebsocketManager
from framework_old import BinanceTradingBot
import sys

"""
Todo:

1.您可以更改symbols中的标的，这代表我们将会交易什么，
    symbols为list但是目前我们只能交易第一个元素，后续版本可能对此进行改进
2.update_data数据自定义
    为您的策略保存一些自定义的历史数据，比如长度为30的分钟k线，您同样可以在init中添加属性
3.strategy是您的策略
    函数会持续运行，一旦产生信号则交易
    我们只能模拟下市价单，返回的值为如果我们真的下市价单成交的价格（忽略了数量
    请在position balance等属性中同步更新方便计算净值
"""


class MyTradingBot(BinanceTradingBot):
    def __init__(self, api_key, api_secret, symbols):
        super().__init__(api_key, api_secret)
        self.symbols = symbols
        self.balance = 1000000  # default is usdt
        self.position = {}
        self.NetValue = self.balance
        for symbol in symbols:
            self.position[symbol] = 0.0001

        ### this is your self-defined parameters
        self.kline_history = {}
        for symbol in symbols:
            self.kline_history[symbol] = list()

    def update_data(self):
        """
        在我们每一次查看self.klines数据的时候，我们仅能获取最新的数据
        但是无法获取到历史的，这样写的目的是防止self.klines中的k线数据一味append导致内存过载
        请在这里写下您的历史数据记录函数，帮助您判断是否需要交易
        """
        self.NetValue = self.balance
        for symbol in self.symbols:
            new_kline = self.klines[symbol]
            if new_kline not in self.kline_history[symbol]:
                self.kline_history[symbol].append(new_kline)
                # 同样防止内存过载，我们只记录20次历史数据
                self.kline_history[symbol] = self.kline_history[symbol][-20:]
                # print('add new kline for', symbol)

            prc = new_kline
            self.NetValue += float(prc['k']['c']) * float(self.position[symbol])

        if self.position[symbol] != 0.0001:
            print('NetValue is:', self.NetValue)

    def strategy(self):
        """
        define your strategy here
        """
        time.sleep(1)
        self.strategy_DualMA(20, 5)
        pass

    def strategy_DualMA(self, long_term: int, short_term: int, quantity = 1):
        '''
        Dual MA strategy: if MA(short term)> MA(long term), then long the symbol else short
        if signal occurs then net short or long quantity unit symbol
        '''
        self.update_data()

        for symbol in self.symbols:
            # get the mean close price
            short_term_mean_now = sum(
                [float(kline['k']["c"]) for kline in self.kline_history[symbol][-short_term:]]) / short_term
            long_term_mean_now = sum(
                [float(kline['k']["c"]) for kline in self.kline_history[symbol][-long_term:]]) / long_term
            short_term_mean_last_minute = sum([
                float(kline['k']["c"]) for kline in self.kline_history[symbol][-short_term - 1:-1]]) / short_term
            long_term_mean_last_minute = sum(
                [float(kline['k']["c"]) for kline in self.kline_history[symbol][-long_term - 1:-1]]) / long_term

            if (short_term_mean_now > long_term_mean_now) and (
                    long_term_mean_last_minute > short_term_mean_last_minute):
                # if short position:
                if self.position[symbol] < 0:
                    # consider the delay, the price make change when we trade, so check if the balance could buy 1 more unit

                    if self.balance > (self.position[symbol] + quantity + 1) * float(self.klines[symbol]['k']["c"]):
                        price = self.market_buy(symbol, self.position[symbol] + quantity)
                        self.position[symbol] = quantity
                        self.balance = self.balance - price * (self.position[symbol] + quantity)
                    else:
                        print('Not enough Money!')

                elif self.position[symbol] == 0:
                    if self.balance > (quantity + 1) * float(self.klines[symbol]['k']["c"]):
                        price = self.market_buy(symbol, qty = quantity)
                        self.position[symbol] = self.position[symbol] + quantity
                        self.balance = self.balance - price * quantity
                    else:
                        print('Not enough Money!')

                elif self.position[symbol] > 0:
                    return

            elif (short_term_mean_now < long_term_mean_now) and (
                    long_term_mean_last_minute < short_term_mean_last_minute):
                # if long position:
                if self.position[symbol] > 0:
                    price = self.market_sell(symbol, self.position[symbol] + quantity)
                    self.position[symbol] = -quantity
                    self.balance = self.balance + price * (self.position[symbol] + quantity)

                elif self.position[symbol] == 0:
                    price = self.market_sell(symbol, qty = quantity)
                    self.position[symbol] = self.position[symbol] - quantity
                    self.balance = self.balance + price * quantity

                elif self.position[symbol] < 0:
                    return

    def strategy_DualThrust(self, n1: int, n2: int, k1: float, k2: float, quantity: int):
        '''
        :params n1: use T-n1-n2 ~ T-n2-1 history minute bars (n1 in total) as the baselines to generate the range
        :params n2: use T-n2 history minute bar's open price to generate the signal
        :params k1: parameter for the buy line
        :params k2: parameter for the sell line
        '''
        self.update_data()

        for symbol in self.symbols:
            use_klines = self.kline_history[symbol][-n1 - n2:-n2]
            HH = max([float(kline['k']["h"]) for kline in use_klines])
            HC = max([float(kline['k']["c"]) for kline in use_klines])
            LC = min([float(kline['k']["c"]) for kline in use_klines])
            LL = min([float(kline['k']["l"]) for kline in use_klines])
            range = max(HH - LC, HC - LL)
            buy_line = float(self.kline_history[symbol][-n2]["k"]["o"]) + range * k1
            sell_line = float(self.kline_history[symbol][-n2]["k"]["o"]) - range * k2

            if float(self.klines[symbol]["k"]["c"]) > buy_line:
                # if short position:
                if self.position[symbol] < 0:
                    # consider the delay, the price make change when we trade, so check if the balance could buy 1 more unit
                    if self.balance > (self.position[symbol] + quantity + 1) * float(self.klines[symbol]["k"]["c"]):
                        price = self.market_buy(symbol, self.position[symbol] + quantity)
                        self.position[symbol] = quantity
                        self.balance = self.balance - price * (self.position[symbol] + quantity)
                    else:
                        print('Not enough Money!')

                elif self.position[symbol] == 0:
                    if self.balance > (quantity + 1) * float(self.klines[symbol]["k"]["c"]):
                        price = self.market_buy(symbol, qty = quantity)
                        self.position[symbol] = self.position[symbol] + quantity
                        self.balance = self.balance - price * quantity
                    else:
                        print('Not enough Money!')

                elif self.position[symbol] > 0:
                    return

            elif float(self.klines[symbol]["k"]["c"]) < sell_line:
                # if long position:
                if self.position[symbol] > 0:
                    price = self.market_sell(symbol, self.position[symbol] + quantity)
                    self.position[symbol] = -quantity
                    self.balance = self.balance + price * (self.position[symbol] + quantity)

                elif self.position[symbol] == 0:
                    price = self.market_sell(symbol, qty = quantity)
                    self.position[symbol] = self.position[symbol] - quantity
                    self.balance = self.balance + price * quantity

                elif self.position[symbol] < 0:
                    return


def strategy_R_Breaker(self, n1: int, n2: int, quantity: int):

    '''
    we don't use the prices last day, we use the prices of T-n1-n2 ~ T-n2-1 history minute bars.

    :params n1: use T-n1-n2 ~ T-n2-1 history minute bars (n1 in total) as the baselines to generate the range
    :params n2: use T-n2~T history minute bars to compare with the range
    '''

    self.update_data()

    for symbol in self.symbols:
        use_klines = self.kline_history[symbol][-n1 - n2:-n2]
        high = max([float(kline["k"]["h"]) for kline in use_klines])
        low = min([float(kline["k"]["l"]) for kline in use_klines])
        close = float(self.kline_history[symbol][-n2 - 1]["k"]["c"])

        pivot = (high + low + close) / 3
        buyBreak = high + 2 * (pivot - low)
        sellSetup = pivot + (high - low)
        turnToShort = 2 * pivot - low
        turnToLong = 2 * pivot - high
        buySetup = pivot - (high - low)
        sellBreak = low - 2 * (high - pivot)

        # not long or short position : trend strategy
        if self.position[symbol] == 0:
            if float(self.klines[symbol]["k"]["c"]) > buyBreak:
                if self.balance > (quantity + 1) * float(self.klines[symbol]["k"]["c"]):
                    price = self.market_buy(symbol, qty = quantity)
                    self.position[symbol] = quantity
                    self.balance = self.balance - price * quantity
                else:
                    print('Not enough Money!')

            elif float(self.klines[symbol]["k"]["c"]) < sellBreak:
                price = self.market_sell(symbol, qty = quantity)
                self.position[symbol] = - quantity
                self.balance = self.balance + price * quantity

        # long or short position: reversal strategy
        elif self.position[symbol] > 0:
            if (max(float(kline["k"]["h"]) for kline in self.kline_history[symbol][-n2:]) > sellSetup) and (
                    float(self.klines[symbol]["k"]["c"]) < turnToShort):
                # short signal
                price = self.market_sell(symbol, self.position[symbol] + quantity)
                self.position[symbol] = -quantity
                self.balance = self.balance + price * (self.position[symbol] + quantity)

        elif self.position[symbol] < 0:
            if (min(float(kline["k"]["l"]) for kline in self.kline_history[symbol][-n2:]) < buySetup) and (
                    float(self.klines[symbol]["k"]["c"]) > turnToLong):
                if self.balance > (self.position[symbol] + quantity + 1) * float(self.klines[symbol]["k"]["c"]):
                    price = self.market_buy(symbol, self.position[symbol] + quantity)
                    self.position[symbol] = quantity
                    self.balance = self.balance - price * (self.position[symbol] + quantity)
                else:
                    print('Not enough Money!')


def start(self):
    while True:
        self.strategy()


if __name__ == "__main__":

    symbols = ['BTCUSDT']  # the symbol you want to trade

    # 初始化api的账号以及密码
    # 账号和密码被存在本地的文件中没有上传
    # 请私聊我获取api_key.txt的最新文件 或者创建您的api key
    with open('api_key.txt', 'r') as file:
        api_content = file.read().split('\n')
    api_key = api_content[0]
    secret_key = api_content[1]

    BMMB = MyTradingBot(api_key, secret_key, symbols)
    # 检测api延迟 如果延迟过高我们会直接退出程序
    #此情况下请检查您的网络
    cnt = 0
    while cnt < 3:
        time_diff = BMMB.get_time_diff()
        print("excution arrive exchange cost: ", time_diff, 'ms\n')
        cnt += 1
        if time_diff >= 1000:
            print('high latency')
            sys.exit(0)


    ### websocket callback function
    ### callback function for start_kline_socke
    def update_klines_dict(msg):
        BMMB.klines[msg['s']] = msg


    bm = ThreadedWebsocketManager(api_key = api_key, api_secret = secret_key)
    bm.start()
    for symbol in symbols:
        bm.start_kline_socket(callback = update_klines_dict, symbol = symbols[0])
    time.sleep(2)  # wait for initialize
    #
    print('start bot')
    time.sleep(5)
    BMMB.start()
