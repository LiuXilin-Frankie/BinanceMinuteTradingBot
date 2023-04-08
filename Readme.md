# Binance Trading System

used for binance trading frame-work.

+ BinanceTradingBot会是独立写在文件framework_old.py中的一个基类，提供数据更新和处理的方法，以及基本的交易方法。正常的情况下，您无需阅读此文件的代码就可以编写您的数据
+ 你可以在外部文件中创建一个新的类，让它继承自BinanceTradingBot类，并添加任何你想要的新方法或覆盖父类中的现有方法。代码示例已经在autotrader中给出。
+ 在这个示例中，我们创建了一个名为MyTradingBot的新类，继承自BinanceTradingBot类，并添加了3个新的函数，这三个新的函数将会是您编写策略的关键，我已经给出了样例，如果没有出现任何的bug请联系我
+ 其他编写事项请向下划动

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

+ framework_old.py: trading frame work
+ autotrader.py: strategy sample
+ python-binance-readthedocs-io-en-latest.pdf: docs of python-binance==1.0.17

### logic

事实上，这仅仅只是一次模拟交易

+ 程序能够实时接收的行情数据仅仅为您给出symbol的kline数据，数据格式在后文给出
+ 如果您的策略判断进行交易，您只能选择市价单的方式成交，函数返回的数字，为下单命令到达交易所之后，最新且最近的一次成交发生的价格，我们假设这是我们策略实际成交的价格（我们忽略了数量的问题）
+ logger会每分钟记录我们的净值变动

kline数据格式如下：

```shell
{
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
    }
}
```
