"""
This module takes the streamed data from exchange.py file, processes it returns
buy, sell or wait signals
"""
import pandas as pd
import pandas_datareader as pdr
import asyncio
import sys
from loguru import logger
import matplotlib.pyplot as plt
import numpy as np
import requests
import math

# =============================BUILD BOLLINGER BANDS==================================
class Strategy:
    """
    This class will receive data streams from the 'data_stream' function in
    file exchange.py and will do some processing on that data, then output buy,
    sell or wait signals.
    Will declare 2 variable in this class, initialized below: "data" is a list
    containing the best bid/ask prices and the historical klines;
    tf is the timeframe for Bollinger Bands set to 20 days, by default
    """
    def __init__(self, data: list, tf: int = 20):
        self.tf = tf
        self.data = data

    async def signals(self):
        """
        This function is taking the streamed data, and using pandas, it calculates
        the SMA, UPPER BB AND LOWER BB, then puts it all together into a dictionary
        Then it puts out a "signal" variable that contains a string saying buy or
        sell, or wait
        """
        result = {} # necessary variable declaration
        try:
            ticker = self.data[0] # fetching the
            klines = self.data[1]

            bid = float(ticker['b'][0][0]) #accessing bid price and convert to float
            ask = float(ticker['a'][0][0]) #accessing ask price and convert to float

            # calculate a rounded average price using bid and ask prices
            avg_price = round((bid + ask)/2,2)

            # Below i turned the historical klines lists to a dataframe for easier
            # calculations
            hist_df = pd.DataFrame(klines, columns = [
                'Open_time',
                'Open',
                'High',
                'Low',
                'Close',
                'Volume',
                'Close_time',
                'Quote_asset_vol',
                'No_trades',
                'Taker_buy_base',
                'Taker_buy_quote',
                'Ignore'
                ])
            # convert close price to float and round the decimals
            hist_df['Close'] = hist_df.Close.astype(float)
            hist_df['Close'].round(decimals=2)

            closing_prices = hist_df['Close']

            # simple moving average calculation
            sma = closing_prices.rolling(self.tf).mean().iloc[-1]
            # standard deviation calculation
            std = closing_prices.rolling(self.tf).std().iloc[-1]
            # calculations to get bollinger bands
            bb_upper = (sma + std*2)
            bb_lower = (sma - std*2)


            #Below i built a dictionary by putting together all the data calculated
            # above: current average price, SMA, Upper BB, Lower BB
            result['current'] = avg_price
            result['SMA'] = sma
            result['BB_UPPER'] = bb_upper
            result['BB_LOWER'] = bb_lower

            # Below is the logic to generate buy or sell signals using the data in the
            # dictionary stored in "result" variable
            if result['current'] >= result['BB_UPPER']:
                signal = f"sell"
                return signal

            elif result['current'] <= result['BB_LOWER']:
                signal = f"buy"
                return signal
            else:
                signal = f"----------------------"
                return signal

        except (Exception, ValueError) as e:
            logger.exception(f"Error! {e}")
