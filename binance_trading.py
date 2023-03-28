import asyncio
import json
from binance import AsyncClient, BinanceSocketManager


class TradingBot:
    def __init__(self, api_key, api_secret):
        self.client = None
        self.bm = None
        self.conn_key = None
        self.klines = {}
        self.trades = {}
        self.tickers = {}
        self.api_key = api_key
        self.api_secret = api_secret

    async def start(self, symbols):
        self.client = await AsyncClient.create(api_key=self.api_key, api_secret=self.api_secret)
        self.bm = BinanceSocketManager(self.client)
        self.subscribe_to_klines(symbols)
        self.subscribe_to_trades(symbols)
        self.subscribe_to_tickers(symbols)
        await self.bm.start()

    def subscribe_to_klines(self, symbols):
        for symbol in symbols:
            self.klines[symbol] = {}
            conn_key = self.bm.start_kline_socket(
                symbol=symbol,
                interval=AsyncClient.KLINE_INTERVAL_1MINUTE,
                callback=self.process_klines
            )
            self.conn_key = conn_key

    def subscribe_to_trades(self, symbols):
        for symbol in symbols:
            self.trades[symbol] = []
            conn_key = self.bm.start_trade_socket(
                symbol=symbol,
                callback=self.process_trades
            )
            self.conn_key = conn_key

    def subscribe_to_tickers(self, symbols):
        for symbol in symbols:
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


async def main():
    bot = TradingBot(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')
    symbols = ['btcusdt', 'ethusdt']
    await bot.start(symbols)

    # 等待接收到一些信息
    await asyncio.sleep(10)

    # 输出收到的klines信息
    print('Klines:')
    print(json.dumps(bot.klines, indent=4))

    # 输出收到的trades信息
    print('Trades:')
    print(json.dumps(bot.trades, indent=4))

    # 输出收到的tickers信息
    print('Tickers:')
    print(json.dumps(bot.tickers, indent=4))

    # 关闭WebSocket连接
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

