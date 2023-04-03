"""
This module is testing the connection to binance. It uses pytest_asyncio to work with the async function
"""
import os
import asyncio
import pytest
import sys
sys.path.append('../crypto-signals')
from main.exchange import data_stream

@pytest.mark.asyncio
async def test_connection(pair:str='btcusdt'):
    """
    This test is checking connection online
    """
    data = data_stream(pair)
    assert data, f"Connection error!"
