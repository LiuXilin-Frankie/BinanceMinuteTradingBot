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
    This function connects to binance's web socket streaming using AsyncClient
    and outputs a list, containing both the market depth data dictionary and the
    historical klines, the latest being a list of lists itself
    Used https://sammchardy.github.io/async-binance-basics/ and and the official
    documentation https://python-binance.readthedocs.io/en/latest/, to build
    this code
    """

    processed_data = []# Declare the necessary variables


    try:
        #Initialize the connection / "client" with try/except for error catching
        client = await AsyncClient.create()
        # Initialize web socket manager
        ws_mng = BinanceSocketManager(client)
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
