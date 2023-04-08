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
        self.balance = 0  # default is usdt
        self.position = {}
        for symbol in symbols:  self.position[symbol] = 0

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
        for symbol in symbols:
            new_kline = self.klines[symbol]
            if new_kline not in self.kline_history[symbol]:
                self.kline_history[symbol].append(new_kline)
                # 同样防止内存过载，我们只记录20次历史数据
                self.kline_history[symbol] = self.kline_history[symbol][-20:]
                print('add new kline for', symbol)

    def strategy(self):
        """
        define your strategy here
        """
        self.update_data()
        # sig = xxxxx

        # if exist sig:
        # trade_prc = self.market_buy(symbol,qty)
        pass

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
    # 此情况下请检查您的网络
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

    print('start bot')
    BMMB.start()
