"""
This module is testing some data types. Will create more in the future
"""
import os
import asyncio
import sys
sys.path.append('../crypto-signals')
from mock_data import mock_data

def test_market_depth(pair:str='btcusdt'):
    """
    This test is checking whether the data type from depth_socket is a dictionary
    """
    data = mock_data()
    assert type(data[0]) is dict, f"The order book depth data type should be a dictionary, got: {type(data)}"

def test_historical_klines(pair:str='btcusdt'):
    """
    This test is checking whether the data type from historical_klines socket is a list
    """
    data = mock_data()
    assert type(data[1]) is list, f"The historical klines data type should be a list, got: {type(data)}"
