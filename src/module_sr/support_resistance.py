from models.support_resistance_model import (request_SR_module,
                                             response_SR_module)
from module_stock.stock import StockDetails
from utils.support_resistance import SupportResistance


class SupportResistanceIndicator:
    """Helper class with methods for Finding Support Resistance levels."""

    def get_support_resistance_levels(self, request: request_SR_module) -> response_SR_module:
        """Helper method to find the support resistance levels."""
        self.stock_data = StockDetails().get_stock_data(stock_id=request.stock_id,
                                                        period=request.period,
                                                        time_frame=request.time_frame)
        sr_levels = SupportResistance().sr_levels(self.stock_data)
        sr_level_response = response_SR_module(stock_id=request.stock_id,
                                               stock_name=request.stock_name,
                                               time_period=f'{request.period}{request.time_frame}',
                                               levels=sr_levels)
        
        return sr_level_response
