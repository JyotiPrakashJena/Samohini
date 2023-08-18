from models.volume_model import (
    current_market_price,
    request_volume_module,
    response_volume_module,
    volume_indicators,
)
from module_stock.stock import StockDetails
from models.stock import request_stock_data
from utils.extras import format_float
from statistics import mean


LAST_FIFTEEN_VOLUME_CONSTANT = -16


class VolumeIndicator:
    """Class with functionality to check volume indicator."""

    def get_avg_volume(self) -> float:
        """Helper function to extract the average volume."""
        volume_data = self.stock_data["volume"]
        last_fifteen_volume = volume_data[LAST_FIFTEEN_VOLUME_CONSTANT:-1]
        return mean(last_fifteen_volume)

    def get_check_vol_indicator(self):
        """Helper function to validate if the volume greater than avg volume."""
        avg_volume = self.get_avg_volume()
        cur_volume = self.stock_data["volume"][-1]
        return cur_volume > avg_volume

    def volume_indicator_response(
        self, request: request_volume_module
    ) -> response_volume_module:
        """Helper function to handle Volume Indicator."""
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

        cur_market_price = current_market_price(
            open=format_float(self.stock_data["open"][-1]),
            price_now=format_float(self.stock_data["close"][-1]),
            low=format_float(self.stock_data["low"][-1]),
            high=format_float(self.stock_data["high"][-1]),
        )
        volume_indicator = volume_indicators(
            volume_now=self.stock_data["volume"][-1],
            avg_volume=self.get_avg_volume(),
            vol_indicator_check=self.get_check_vol_indicator(),
        )
        volume_response = response_volume_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            time_period=f"{request.period}{request.time_frame}",
            volume_indicators=volume_indicator,
            cur_market_price=cur_market_price,
        )
        return volume_response
