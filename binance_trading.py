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

    def subscribe_to_klines(self):
        for symbol in self.symbols:
            self.klines[symbol] = {}
            conn_key = self.bm.start_kline_socket(
                symbol=symbol,
                interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
                callback=self.process_klines
            )
            self.conn_key = conn_key

    def subscribe_to_trades(self):
        for symbol in self.symbols:
            self.trades[symbol] = []
            conn_key = self.bm.start_trade_socket(
                symbol=symbol,
                callback=self.process_trades
            )
            self.conn_key = conn_key

    def subscribe_to_tickers(self):
        for symbol in self.symbols:
            self.tickers[symbol] = {}
            conn_key = self.bm.start_symbol_ticker_socket(
                symbol=symbol,
                callback=self.process_tickers
            )
            self.conn_key = conn_key

    def process_klines(self, msg):
        symbol = msg['s']
        self.klines[symbol][msg['k']['t']] = msg['k']

    def process_trades(self, msg):
        symbol = msg['s']
        self.trades[symbol].append(msg)

    def process_tickers(self, msg):
        symbol = msg['s']
        self.tickers[symbol] = msg

    async def close(self):
        await self.bm.close()
        await self.client.close()

    # 基本的交易方法
    async def buy_market_order(self, symbol, quantity):
        order = await self.client.create_order(
            symbol=symbol,
            side=AsyncClient.SIDE_BUY,
            type=AsyncClient.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return order

    async def sell_market_order(self, symbol, quantity):
        order = await self.client.create_order(
            symbol=symbol,
            side=AsyncClient.SIDE_SELL,
            type=AsyncClient.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return order
