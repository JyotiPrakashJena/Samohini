from models.fibo_model import(
    request_fibo_module,
    response_fibo_module,
    stock_levels
)
from module_stock.stock import StockDetails
import pandas as pd

class FiboModules:
    """Helper class for Fibo Indictors"""

    def get_fibo_levels(self, request: request_fibo_module) -> response_fibo_module:
        """Method responsible for fetching Fibo levels of a Stock
        
        request (request_fibo_module): Object containing required inputs for fibo levels
        response_fibo_module: Object containing response along with fibo levels
        """
        stock_data = StockDetails().get_stock_data(stock_id=request.stock_id,
                                                 period=request.period,
                                                 time_frame=request.time_frame)
        stock_levels = self.fibo_indicator(stock_data)
        return response_fibo_module(stock_id=request.stock_id,
                                    stock_name=request.stock_name,
                                    time_period = f'{request.period}{request.time_frame}',
                                    market=request.market,
                                    levels=stock_levels)


    def fibo_indicator(self, data:pd.DataFrame) -> list:
        """Helper function generate fibo levels of a stock

        data (pd.DataFrame): Dataframe containinf stock details
        levels (dict) : dictionary with fibo ratios as key & fibo levels as value
        """
        highest_swing = -1
        lowest_swing = -1
        ratios = [0, 0.236, 0.618, 1]
        for i in range(1, data.shape[0] - 1):
            if data['high'][i] > data['high'][i - 1] and data['high'][i] > data['high'][i + 1] and (
                    highest_swing == -1 or data['high'][i] > data['high'][highest_swing]):
                highest_swing = i
            if data['low'][i] < data['low'][i - 1] and data['low'][i] < data['low'][i + 1] and (
                    lowest_swing == -1 or data['low'][i] < data['low'][lowest_swing]):
                lowest_swing = i

        fibo_levels = []
        max_level = data['high'][highest_swing]
        min_level = data['low'][lowest_swing]
        for ratio in ratios:
            if highest_swing > lowest_swing:  # Uptrend
                stock_level = stock_levels(ratio=ratio,
                                           level=float("{:.2f}".format(max_level - (max_level - min_level) * ratio)))
                fibo_levels.append(stock_level)
            else:  # Downtrend
                stock_level = stock_levels(ratio=ratio,
                                           level=float("{:.2f}".format(min_level + (max_level - min_level) * ratio)))
                fibo_levels.append(stock_level)
        return fibo_levels