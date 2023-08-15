import concurrent.futures
import time

from module_stock.stock import StockDetails
from module_candlestick.bull_candlestick import BullCandleStick
from module_indicators.indicators import BullIndicators
from module_sr.support_resistance import SupportResistanceIndicator
from module_fibo.fibo import FiboModules
from module_volume.bull_volume import VolumeIndicator

from models.stock_screener_model import (request_all_screener_details, response_all_screener_details)
from models.candlestick_model import (request_candle_module, response_candle_module)
from models.indicators_model import (request_indicator_module, response_indicator_module)
from models.support_resistance_model import (request_SR_module, response_SR_module)
from models.fibo_model import (request_fibo_module, response_fibo_module)
from models.volume_model import (request_volume_module, response_volume_module)

class StockScreener:
    """Class with methods to screen stocks from the pool."""

    def handler_bull_candle_response(self, request: request_all_screener_details) -> response_candle_module:
        """Handler for Bull Candle Response."""
        bull_candle_stick_request = request_candle_module(stock_id=request.stock_id,
                                                          stock_name=request.stock_name,
                                                          period=request.period,
                                                          time_frame=request.time_frame,
                                                          market=request.market,
                                                          stock_data=request.stock_data)
        return BullCandleStick().get_candle_bull_response(bull_candle_stick_request)
    

    def handler_indicator_response(self, request: request_all_screener_details) -> response_indicator_module:
        """Handler for Bull Indicator Response."""
        bull_candle_stick_request = request_indicator_module(stock_id=request.stock_id,
                                                          stock_name=request.stock_name,
                                                          period=request.period,
                                                          time_frame=request.time_frame,
                                                          market=request.market,
                                                          stock_data=request.stock_data)
        return BullIndicators().get_indicators_response(bull_candle_stick_request)


    def handler_sr_response(self, request: request_all_screener_details) -> response_SR_module:
        """Handler for Support Resistance."""
        support_resistance_request = request_SR_module(stock_id=request.stock_id,
                                                          stock_name=request.stock_name,
                                                          period=request.period,
                                                          time_frame=request.time_frame,
                                                          market=request.market,
                                                          stock_data=request.stock_data)
        return SupportResistanceIndicator().get_support_resistance_levels(support_resistance_request)


    def handler_fibo_response(self, request: request_all_screener_details) -> response_fibo_module:
        """Handler for Fibo Response."""
        fibo_request = request_fibo_module(stock_id=request.stock_id,
                                                          stock_name=request.stock_name,
                                                          period=request.period,
                                                          time_frame=request.time_frame,
                                                          market=request.market,
                                                          stock_data=request.stock_data)
        return FiboModules().get_fibo_levels(fibo_request)
    

    def handler_volume_response(self, request: request_all_screener_details) -> response_volume_module:
        """Handler for Volume Response."""
        volume_request = request_volume_module(stock_id=request.stock_id,
                                                          stock_name=request.stock_name,
                                                          period=request.period,
                                                          time_frame=request.time_frame,
                                                          market=request.market,
                                                          stock_data=request.stock_data)
        return VolumeIndicator().volume_indicator_response(volume_request)



    def get_all_screener_details(self, request: request_all_screener_details) -> response_all_screener_details:
        """Validate if a stock passes all the checks."""
        try:
            stock_data = StockDetails().get_stock_data(
                stock_id=request.stock_id,
                period=request.period,
                time_frame=request.time_frame,
            )
            request.stock_data = stock_data
            candle_stick_response = self.handler_bull_candle_response(request)
            indicator_response = self.handler_indicator_response(request)
            sr_response = self.handler_sr_response(request)
            fibo_response = self.handler_fibo_response(request)
            volume_response = self.handler_volume_response(request)
            get_all_screener_response = response_all_screener_details(stock_id=request.stock_id,
                                                                    stock_name=request.stock_name,
                                                                    time_period=f'{request.period}{request.time_frame}',
                                                                    candle_stick_response=candle_stick_response,
                                                                    indicator_response=indicator_response,
                                                                    fibo_response=fibo_response,
                                                                    sr_response=sr_response,
                                                                    volume_response=volume_response)
            return get_all_screener_response
        except Exception as e:
            print(e)


    def recommended_stocks(self):
        """Helper method to extract stocks from the pool."""
        stock_list = StockDetails().get_stock_list()
        
        start_time = time.time()
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = []
            for index, row in stock_list[:200].iterrows():
                request_screener = request_all_screener_details(stock_id=row['Symbol'],
                                                stock_name=row['Name'])
                futures.append(executor.submit(self.get_all_screener_details, request_screener))
            # futures = [executor.submit(self.get_all_screener_details, request_all_screener_details(stock_id=row['Symbol'],
            #                                     stock_name=row['Name'])) for index, row in stock_list[:10].iterrows()]
            
            results = []
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                result = future.result()
                print(f'Task Completed with Id: {i}')
                results.append(result)
            print(f'Total Time Consumed: {time.time()-start_time}')
            return results
