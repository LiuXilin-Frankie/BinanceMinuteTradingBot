"""
This module logs buy or sell messages into the CLI terminal
"""
import asyncio
import sys
from loguru import logger
logger.remove(0)
logger.add(sys.stderr, format="<green>{time}</green> | <red>{level}</red> | <yellow>{message}</yellow>", colorize=True)

class OrderManager():
    """
    This class contains a function that takes in signals from the Strategy class
    in file strategy.py and then logs messages into the terminal
    """
    def __init__(self, signal):
        self.signal = signal

    async def orders(self):
        try:
            if self.signal == "buy":
                return logger.success(f"{self.signal.title()} Bitcoin")
            elif self.signal == "sell":
                return logger.info(f"{self.signal.title()} Bitcoin")
            else:
                return logger.info(f"{self.signal.title()}")

        except (Exception, ValueError) as e:
            logger.exception(f"Error! {e}")
