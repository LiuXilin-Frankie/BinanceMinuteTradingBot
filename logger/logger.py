import json
#from datamodel import Order, ProsperityEncoder, Symbol, Trade, TradingState
from typing import Any
import datetime

class Logger:
    def __init__(self,UI_path) -> None:
        self.logs = ""
        self.UI_path = UI_path

    def print(self, *objects: Any, sep: str = " ", end: str = "\n") -> None:
        self.logs += sep.join(map(str, objects)) + end

    def flush_netvalue(self,value):
        time_now = str(datetime.datetime.now())[:16]+':00'
        info_operation = time_now +' , ' + value
        self.flush_file((self.UI_path+'NetValueTemp.log'), info_operation)

    def flush_trades(self,symbol,direction,qty,prc):
        time_now = str(datetime.datetime.now())[:16]+':00'
        info_operation = time_now +', '+direction +', '+str(qty) +', '+str(prc)
        self.flush_file(self.UI_path+'Operation.log', info_operation)

    def flush_file(self,filepath,infoadd):
        with open(filepath, "r") as f:
            text = f.read()+'\n'
        with open(filepath, "w+") as f:
            f.write(text + infoadd)
        print(infoadd)


#logger = Logger(UI_path)
#logger.flush(state, orders)