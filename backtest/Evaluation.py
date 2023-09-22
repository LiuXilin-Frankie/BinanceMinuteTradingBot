import numpy as np
import pandas as pd
from pandas import DataFrame, Series

'''
get some indicator to evaluate the performance of the strategy.

'''


class Evaluation:
    def _get_return(cls, nav: DataFrame) -> Series:
        '''

        :params nav: nav from get_netvalue_time_series in class Account
        '''

        nav_s = nav.iloc[:, 0]
        return_p = (nav_s / nav_s.shift(1) - 1).dropna()
        return return_p

    @classmethod
    def get_sharpe_ratio(cls, nav: DataFrame, period_num: int):
        '''
        get annualized sharpe ratio

        :params nav: nav from get_netvalue_time_series in class Account
        '''
        return_p = cls._get_return(cls, nav)
        sharpe_ratio = return_p.mean() / return_p.std() * np.sqrt(period_num)
        return sharpe_ratio

    @classmethod
    def get_max_drawdown(cls, nav: DataFrame):
        nav_s = nav.iloc[:, 0]
        cummax = nav_s.expanding().max()
        drawdown = (cummax - nav_s) / cummax 
        max_drawdown = max(drawdown)
        duration = pd.Series(index = drawdown.index)
        duration.iloc[0] = 0
        for i in range(1, len(drawdown)):
            duration.iloc[i] = 0 if drawdown.iloc[i] == 0 else duration.iloc[i - 1] + 1
        max_duration = duration.max()

        return max_drawdown, max_duration
