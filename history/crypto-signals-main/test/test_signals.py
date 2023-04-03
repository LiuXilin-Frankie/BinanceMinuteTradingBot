"""
This module is testing the buy or sell signals issuance, when the price is a the
lower bollinger band or at the upper bollinger band
It uses mock binance api data from a local file: 'mock_data.py'
"""
import datetime
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import numpy as np
import requests
import math
import os
import pytest
import asyncio
import sys
sys.path.append('../crypto-signals')
from mock_data import mock_data


def test_buy_signal(pair:str='btcusdt'):
    result = {}
    # fetch mock data from mock_data.py which resembles the data that the connections
    # outputs
    data = mock_data()
    # Below i turned the historical klines lists to a dataframe for easier
    # calculations
    hist_df = pd.DataFrame(data[1], columns = [
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
    sma = closing_prices.rolling(20).mean().iloc[-1]
    # standard deviation calculation
    std = closing_prices.rolling(20).std().iloc[-1]
    # calculations to get bollinger bands
    bb_upper = (sma + std*2)
    bb_lower = (sma - std*2)

    """
    Below i built a dictionary by putting together all the data calculated
    above: current average price, SMA, Upper BB, Lower BB
    """
    # i set the ticker price to be equal to the lower bollinger band in order
    # to assert if the buy signal is loged
    result['current'] = bb_lower
    result['SMA'] = sma
    result['BB_UPPER'] = bb_upper
    result['BB_LOWER'] = bb_lower

    # Below is the logic to generate buy or sell signals using the data in the
    # dictionary stored in "result" variable
    if result['current'] >= result['BB_UPPER']:
        signal = f"sell"

    elif result['current'] <= result['BB_LOWER']:
        signal = f"buy"
    else:
        signal = f"wait"

    assert signal == "buy", f"The logged message should be 'buy', got: {ord}"


def test_sell_signal(pair:str='btcusdt'):
    result = {}
    # fetch mock data from mock_data.py which resembles the data that the connections
    # outputs
    data = mock_data()
    # Below i turned the historical klines lists to a dataframe for easier
    # calculations
    hist_df = pd.DataFrame(data[1], columns = [
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
    sma = closing_prices.rolling(20).mean().iloc[-1]
    # standard deviation calculation
    std = closing_prices.rolling(20).std().iloc[-1]
    # calculations to get bollinger bands
    bb_upper = (sma + std*2)
    bb_lower = (sma - std*2)

    """
    Below i built a dictionary by putting together all the data calculated
    above: current average price, SMA, Upper BB, Lower BB
    """
    # i set the ticker price to be equal to the lower bollinger band in order
    # to assert if the buy signal is loged
    result['current'] = bb_upper
    result['SMA'] = sma
    result['BB_UPPER'] = bb_upper
    result['BB_LOWER'] = bb_lower

    # Below is the logic to generate buy or sell signals using the data in the
    # dictionary stored in "self.result"
    if result['current'] >= result['BB_UPPER']:
        signal = f"sell"

    elif result['current'] <= result['BB_LOWER']:
        signal = f"buy"
    else:
        signal = f"wait"

    assert signal == "sell", f"The logged message should be 'sell', got: {ord}"
