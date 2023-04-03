"""
This module connects to the exchange and streams data
"""
from binance import AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException
import sys
import asyncio
from loguru import logger

#=======================CONNECTION SETTINGS======================
async def data_stream(pair:str, depth:str = 5, interval: int = None):
    """
    Connects to binance's web socket streaming using AsyncClient
    Used https://sammchardy.github.io/async-binance-basics/ and and the official
    documentation https://python-binance.readthedocs.io/en/latest/, to build this code

    Input: 
        - pair: the symbol youn want to scribe
        - depth: the order book depth you used, default is 5
        - interval: frequency, default means the highest frequency supported by the exchange
    Output:
        - processed_data: list, contains 2 data, data and hist_data
            - data: real time order book data
            - hist_data: history kline data
    """

    #Initial output list
    processed_data = []

    try:
        # Initial the connection
        client = await AsyncClient.create()
        ws_mng = BinanceSocketManager(client)   # websocket manager
        
        # order book depth settings for the depth_socket
        socket1 = ws_mng.depth_socket(pair, interval)
        # start streaming asynchronously
        async with socket1 as stream:
            while True:
                # orderbook depth data stored into a variable
                data = await stream.recv()
                # historical klines stored in to a variable
                hist_data = await client.get_historical_klines(pair, AsyncClient.KLINE_INTERVAL_1HOUR, "15 Apr, 2022")
                # create a list with both sets of data for easier transmision
                # to a another function
                processed_data.append(data)
                processed_data.append(hist_data)
                return processed_data
        # closing the connection
        await client.close_connection()

    except (Exception, ValueError) as e:
        return logger.exception(f"{e}")
