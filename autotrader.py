__author__ = 'AbsoluteX'
__email__ = 'l276660317@gmail.com'

from binance import BinanceSocketManager
from framework_old import BinanceTradingBot


class BinanceMarketMakingBot(BinanceTradingBot):
    def __init__(self, api_key, api_secret):
        super().__init__(api_key, api_secret)
    
    
    def strategy(self):
        """
        define your strategy here
        """
        pass

    def start(self):
        while True:
            self.strategy()
            # if exist sig:
                # set orders



if __name__ == "__main__":
    # 初始化api的账号以及密码
    # 账号和密码被存在本地的文件中没有上传
    # 请私聊我获取api_key.txt的最新文件 或者创建您的api key
    with open('api_key.txt','r') as file:
        api_content = file.read().split('\n')
    api_key = api_content[0]
    secret_key = api_content[1]
    
    BMMB = BinanceMarketMakingBot(api_key, secret_key)
    # 检测api延迟 如果延迟过高我们会直接退出程序
    # 此情况下请检查您的网络
    cnt=0
    while cnt<3:
        time_diff = BMMB.get_time_diff()
        print("excution arrive exchange cost: ",time_diff,'ms\n')
        cnt+=1
        if time_diff>=1000:
            print('high latency')
            sys.exit(0)

    ### websocket callback function
    ### callback function for start_kline_socke
    def update_klines_dict(msg):
        BMMB.klines[msg['s']] = msg

    ### websocket callback function
    ### callback function for start_user_socket
    def update_user(msg): 
        if msg['e'] == 'executionReport':
            BMMB.trade_status_dict[msg['s']] = msg
        else:
            balances = msg['B']
            try:
                for i in balances:
                    BMMB.asset_balances[i['a']] = i
            except:
                print(msg)

    bm = BinanceSocketManager(BMMB.client)
    symbols = ['BTCUSDT','ETHUSDT'] #the symbol you want to trade
    for symbol in symbols:
        bm.start_kline_socke(callback=update_klines_dict,symbol=symbol)
    bm.start_user_socket(update_user)
    time.sleep(10) #wait for initialize
    bm.start()