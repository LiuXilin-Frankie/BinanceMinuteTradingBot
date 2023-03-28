# Binance Trading System
used for binance trading frame-work.

### quick start
note: if there exists some import error when you are trying to import python-binance, please delete the env and recreate by the following command, "--conda install" command or the package "jupyter" may be the reason caused this error (not sure). So please keep the trading environment clean. This env is used only for trading, you can backtest your strategy in other env and with your local data.
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
+ autotrader.py: trading frame work
+ python-binance-readthedocs-io-en-latest.pdf: docs of python-binance==1.0.17