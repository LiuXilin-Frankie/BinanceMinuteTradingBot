__author__ = 'AbsoluteX'
__email__ = 'l276660317@gmail.com'

from binance_trading import TradingBot

class MyTradingBot(TradingBot):
    def __init__(self, api_key, api_secret, symbols, my_param):
        super().__init__(api_key, api_secret, symbols)
        self.my_param = my_param

    def my_new_method(self):
        # 在这里实现你的新方法
        pass

    # 基本的交易方法
    async def buy_market_order(self, symbol, quantity):
        # 覆盖TradingBot中的buy_market_order方法
        print("我正在执行自定义的buy_market_order方法！")
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

