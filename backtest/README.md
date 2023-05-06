# 简单回测系统

#### 回测系统主要可分为五大模块，数据读取模块DataHandler，策略模块Strategy_Backtest，交易执行模块Order_Execution，账户模块Account，以及最终策略运行模块BackTest。

1. DataHandler.py :该模块功能为从MySQL数据库中读取读取历史交易数据。(在此之前，需要运行Data_to_SQL.py把数据压缩包中的数据储存到Mysql数据库中。)
2. Account.py : 该模块功能是记录策略运行过程中的交易信息(包括资产名称，买卖头寸，买卖价格，买卖时间，账户头寸净值，账户可用交易金额等等)，考虑了单边0.0001的手续费，以及加入了止盈止损的监测和策略回测结束后策略效果的评估方法(get_evaluation方法会调用Evaluation.py 类中的方法来评估策略，指标为夏普比，最大回撤率以及最大回撤时间(分钟))。
3. Strategy_BackTest.py : 该模块用于封装策略，策略中的start_run方法会根据从DataHandler类中不断更新获取到的行情数据来成Order(格式为字典，若无信号则为空字典{}。 eg: {'ADAUSDT': {'action': 'Short', 'quantity': 20}, 'BATUSDT': {'action': 'Short', 'quantity': 20}}) ，目前封装了三个经典策略，分别为 Dual MA, Dual Thrust 和 R Breaker。
目前策略的风控是达到我们设定的止盈止损线时就会进行平仓，停止一段时间后再重新运行。
4. Order_Execution.py : 该模块会接收Strategy_BackTest模块中具体策略运行过程中产生的Order，然后进行交易，我们目前的回测系统是用Order生成时滞后一分钟的收盘价格进行回测(即delay_min=1)
5. BackTest.py : 该模块用于运行策略进行回测，类参数stop_time_length_min是当具体策略运行过程中达到止盈止损线停止的时间(分钟)。
6. Test.py: 导入以上模块运行策略进行回测。

### 有待完善之处
1. 回测时简单地使用了一个时间生成器，根据时间一条一条来更新数据，但是和Order发出后读取交易买卖价的函数分开了，所以目前该系统只支持使用延迟1分钟的close价格，还不能支持使用更长时间的延迟来进行回测交易（虽然delay_min设成了参数），后续或许可以使用事件驱动和队列进行完善。
2. 回测时假设的是order会被完全执行，没考虑交易执行过程中一些市场摩擦，后续可增加更多的Order执行结果，记录执行状态。
3. 目前所有封装进去的策略采取的是简单固定策略执行后资产头寸绝对值的方法，比如设定了策略中的参数quantity为10，多头信号时产生时，当Order执行结束会使得头寸为10，当空头信号产生时，当Order执行结束会使得头寸为-10。后续可进行更精细化的仓位管理。
4. 风控没有单独设立模块，只是比较简单地通过监测账户的止盈止损来平仓以及停止运行策略一段时间。

### 参考资料
1. https://github.com/tobiasbrodd/backtester
2. https://www.tushare.pro/document/1?doc_id=90
3. https://blog.csdn.net/qq_31611005/article/details/103834578
4. https://www.myquant.cn/docs/python_strategyies/153