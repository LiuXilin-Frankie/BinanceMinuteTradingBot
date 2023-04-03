# Binance Trading System
used for binance trading frame-work.

+ TradingBot会是独立写在文件binance_trading.py中的一个基类，提供数据更新和处理的方法，以及基本的交易方法。
+ 你可以在外部文件中创建一个新的类，让它继承自TradingBot类，并添加任何你想要的新方法或覆盖父类中的现有方法。代码示例已经在autotrader中给出。
+ 在这个示例中，我们创建了一个名为MyTradingBot的新类，继承自TradingBot类，并添加了一个新的方法my_new_method()。我们还覆盖了父类中的buy_market_order()方法，以便在方法执行时打印一条自定义消息。

### quick start
note: if there exists some import error when you are trying to import python-binance, please delete the env and recreate by the following command.

"--conda install" command or the package "jupyter" may be the reason caused this error (not sure). So please keep the trading environment clean. This env is used only for trading, you can backtest your strategy in other env and with your local data.
```shell
conda create -n BinanceTrading python=3.8
conda activate BinanceTrading
pip install pandas
pip install numpy
pip install ccxt
pip install urllib3==1.25.8
pip install python-binance==1.0.17
```

### file structure
+ binance_trading.py: trading frame work
+ autotrader.py: strategy sample
+ python-binance-readthedocs-io-en-latest.pdf: docs of python-binance==1.0.17