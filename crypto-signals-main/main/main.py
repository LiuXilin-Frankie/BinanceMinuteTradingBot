"""
This module puts all the different functions to work together. It's the
executable file
"""
import asyncio
from asyncio import Queue
from loguru import logger
import sys
# check min. python version
if sys.version_info < (3, 8):
    sys.exit("This program requires Python version >= 3.8")

from strategy import Strategy
from exchange import data_stream
from order_manager import OrderManager

async def start(pair: str):
    """
    Here all the different modules are centralized and ran using statement
    at the bottom, with the 'run_until_complete' command specific to async
    functions
    """
    try:
        while True:
                # create a task in asyncio for data_stream function
                strm = await asyncio.create_task(
                    data_stream(pair)
                )
                # serve the streamed data to the strategy function
                sig = await Strategy(strm).signals()
                # serve the strategy module output (signal) to the order Order
                # manager module
                ord = await OrderManager(sig).orders()
    except (Exception, ValueError) as e:
        logger.exception(f"Error! {e}")


if __name__ == "__main__":
    # Fetch the CLI command first argument, which should be btcusdt
    sym = sys.argv[1].upper()
    # Printing a notice on what is being streamed into the command terminal
    print(f"Will stream pair: {sym}")
    print(f"Starting...")
    # Execution of the program
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(sym))
