from binance import BinanceSocketManager
from framework_old import BinanceTradingBot
import json

with open('api_key.txt','r') as file:
    api_content = file.read().split('\n')
api_key = api_content[0]
secret_key = api_content[1]

BMMB = BinanceTradingBot(api_key, secret_key)
next_trade = BMMB.client.aggregate_trade_iter(symbol='BTCUSDT')

#print(json.loads(next(next_trade)))
print(next(next_trade))