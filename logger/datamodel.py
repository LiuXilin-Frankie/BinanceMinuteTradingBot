"""
see https://imc-prosperity.notion.site/Writing-an-Algorithm-in-Python-c44b46f32941430fa1eccb6ff054be26
for parameter details and meaning
"""
import json
from typing import Dict, List
from json import JSONEncoder

Time = int
Symbol = str
Product = str
Position = int
UserId = str
Observation = int


class Listing:
    def __init__(self, symbol: Symbol, product: Product, denomination: Product):
        self.symbol = symbol
        self.product = product
        self.denomination = denomination


class Order:
    """
    发送由参赛者定义的 Trade.run() 生成的订单
    请注意: 
    岛上交易所玩家的执行速度是无限快的，这意味着他们的所有订单都可以毫无延迟地到达交易所撮合引擎。
    """
    def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
        self.symbol = symbol
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

    def __repr__(self):
        return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"
    

class OrderDepth:
    """
    包含所有未完成的买卖订单的集合
    字典 keys 是价格，后面的值是数量，卖单中数量统一为负数
    """
    def __init__(self):
        self.buy_orders: Dict[int, int] = {}
        self.sell_orders: Dict[int, int] = {}


class Trade:
    """
    可以参考 TradingState
    own_trades 和 market_trades 是两个list
    其中 list 的每一个元素都是 Trade 属性的一个实例
    """
    def __init__(self, symbol: Symbol, price: int, quantity: int,
                 buyer: UserId = None, seller: UserId = None, timestamp: int = 0):
        self.symbol = symbol
        self.price: int = price
        self.quantity: int = quantity
        self.buyer = buyer   #买方的ID
        self.seller = seller   #卖房的ID
        self.timestamp = timestamp
        # 如果成交方是算法，则标记为Submission，如果不是则为空值

class TradingState(object):
    """
    TradingState 类包含所有重要的市场信息，算法需要这些信息来决定发送哪些订单。
    """
    def __init__(self,
                 timestamp: Time,
                 listings: Dict[Symbol, Listing],
                 order_depths: Dict[Symbol, OrderDepth],
                 own_trades: Dict[Symbol, List[Trade]],
                 market_trades: Dict[Symbol, List[Trade]],
                 position: Dict[Product, Position],
                 observations: Dict[Product, Observation]):
        self.timestamp = timestamp
        self.listings = listings
        self.order_depths = order_depths  #all the buy and sell orders per product
        self.own_trades = own_trades  #the trades the algorithm itself has done
        self.market_trades = market_trades  #the trades that other market participants have done
        self.position = position
        self.observations = observations
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)
    
class ProsperityEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__