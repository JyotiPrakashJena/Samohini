from models.support_resistance_model import (
    current_market_price,
    request_SR_module,
    response_SR_module,
)
from module_stock.stock import StockDetails
from models.stock import request_stock_data
from utils.support_resistance import SupportResistance
from utils.extras import format_float


class SupportResistanceIndicator:
    """Helper class with methods for Finding Support Resistance levels."""

    def get_support_resistance_levels(
        self, request: request_SR_module
    ) -> response_SR_module:
        """Helper method to find the support resistance levels."""
        if request.stock_data.empty:
            self.stock_data = StockDetails().get_stock_data(
                request_stock_data(
                    stock_id=request.stock_id,
                    period=request.period,
                    time_frame=request.time_frame,
                )
            )
        else:
            self.stock_data = request.stock_data

        sr_levels = SupportResistance().sr_levels(self.stock_data)
        cur_market_price = current_market_price(
            open=format_float(self.stock_data["open"][-1]),
            price_now=format_float(self.stock_data["close"][-1]),
            low=format_float(self.stock_data["low"][-1]),
            high=format_float(self.stock_data["high"][-1]),
        )
        sr_level_response = response_SR_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            time_period=f"{request.period}{request.time_frame}",
            levels=sr_levels,
            cur_market_price=cur_market_price,
        )

        return sr_level_response
