__author__ = 'AbsoluteX'
__email__ = 'l276660317@gmail.com'

import asyncio
from binance import AsyncClient, BinanceSocketManager


class TradingBot:
    def __init__(self, api_key, api_secret, symbols):
        self.client = None
        self.bm = None
        self.conn_key = None
        self.klines = {}
        self.trades = {}
        self.tickers = {}
        self.balance = {}
        self.api_key = api_key
        self.api_secret = api_secret
        self.symbols = symbols

    async def start(self):
        self.client = await AsyncClient.create(api_key=self.api_key, api_secret=self.api_secret)
        self.bm = BinanceSocketManager(self.client)
        self.subscribe_to_klines()
        self.subscribe_to_trades()
        self.subscribe_to_tickers()
        await self.bm.start()

    """ 
    订阅kline数据的操作 
    The Kline/Candlestick Stream push updates to the current klines/candlestick every second.

    数据说明如下：
    {
        "e": "kline",     // Event type
        "E": 123456789,   // Event time
        "s": "BNBBTC",    // Symbol
        "k": {
            "t": 123400000, // Kline start time
            "T": 123460000, // Kline close time
            "s": "BNBBTC",  // Symbol
            "i": "1m",      // Interval
            "f": 100,       // First trade ID
            "L": 200,       // Last trade ID
            "o": "0.0010",  // Open price
            "c": "0.0020",  // Close price
            "h": "0.0025",  // High price
            "l": "0.0015",  // Low price
            "v": "1000",    // Base asset volume
            "n": 100,       // Number of trades
            "x": false,     // Is this kline closed?
            "q": "1.0000",  // Quote asset volume
            "V": "500",     // Taker buy base asset volume
            "Q": "0.500",   // Taker buy quote asset volume
            "B": "123456"   // Ignore
        }
    }
    """
    def subscribe_to_klines(self):
        for symbol in self.symbols:
            self.klines[symbol] = {}
            conn_key = self.bm.start_kline_socket(
                symbol=symbol,
                interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
                callback=self.process_klines
            )
            self.conn_key = conn_key

    def process_klines(self, msg):
        symbol = msg['s']
        self.klines[symbol][msg['k']['t']] = msg['k']

    # """
    # 订阅交易数据的操作
    # """
    # def subscribe_to_trades(self):
    #     for symbol in self.symbols:
    #         self.trades[symbol] = []
    #         conn_key = self.bm.start_trade_socket(
    #             symbol=symbol,
    #             callback=self.process_trades
    #         )
    #         self.conn_key = conn_key

    # def process_trades(self, msg):
    #     symbol = msg['s']
    #     self.trades[symbol].append(msg)

    """
    订阅
    """
    def subscribe_to_tickers(self):
        for symbol in self.symbols:
            self.tickers[symbol] = {}
            conn_key = self.bm.start_symbol_ticker_socket(
                symbol=symbol,
                callback=self.process_tickers
            )
            self.conn_key = conn_key

    def process_tickers(self, msg):
        symbol = msg['s']
        self.tickers[symbol] = msg

    async def close(self):
        await self.bm.close()
        await self.client.close()
