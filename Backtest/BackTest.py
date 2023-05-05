from Order_Execution import OrderExecutionHandler


'''
this class would run the whole strategy through the method named run_strategy method.
'''
class BackTest:
    def __init__(self, strategy, order_execution_handler: OrderExecutionHandler, stop_time_length_min: int):

        self.strategy = strategy
        self.order_execution_handler = order_execution_handler
        self.stop_time_length_min = stop_time_length_min  # if the strategy reach the profit or loss line, then stop for stop_time_length_min minutes

    def run_strategy(self):
        while True:
            if self.strategy.continue_backtest:
                order, time, warning_signal = self.strategy.start_run()
                # print(order)
                if time == None:  # means already reach the end date of the backtest
                    self.strategy.continue_backtest = False
                    break
                elif order != {}:  # means having order to be sent
                    self.order_execution_handler.execute(order, time, warning_signal)
            else:
                if self.rerun_from_stop() != None:
                    break
                else:
                    continue

    def rerun_from_stop(self):
        # stop the strategy but update data
        for i in range(self.stop_time_length_min):
            _, date_time = self.strategy.dh.update_data()
            if date_time != None:
                self.strategy.account.update_net_value(date_time, self.strategy.dh)
            else:
                break

        if i == self.stop_time_length_min - 1:  # backtest done
            self.strategy.continue_backtest = True
            # reset the balance_init
            self.strategy.account.balance_init = self.strategy.account.balance
        else:
            return 0



