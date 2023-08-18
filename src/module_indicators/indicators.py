from models.indicators_model import (
    bull_indicators,
    current_market_price,
    request_indicator_module,
    response_indicator_module,
)
from module_stock.stock import StockDetails
from models.stock import request_stock_data
from utils.extras import format_float


class BullIndicators:
    """Class with functionality for detection of Bullish Pattern."""

    def cross_moving_avg(self) -> bool:
        """Helper function to check for cross_moving average pattern.

        Rule: 50days EMA is greater than 100days EMA
        """
        fiftyEMA = self.stock_data.close.ewm(span=50, adjust=False).mean()
        centEMA = self.stock_data.close.ewm(span=50, adjust=False).mean()
        return fiftyEMA[-1] > centEMA[-1]

    def moving_avg(self) -> bool:
        """Helper function to check for moving average indicator.

        Rule:Current M.P is greater than 50days EMA.
        """
        fiftyEMA = self.stock_data.close.ewm(span=12, adjust=False).mean()
        return self.stock_data["close"][-1] > fiftyEMA[-1]

    def indicator_rsi(self) -> bool:
        """Helper function to check for RSI Indicator."""
        rsi_threshold = 25
        delta = self.stock_data.close.diff()
        window = 15
        up_days = delta.copy()
        up_days[delta <= 0] = 0.0
        down_days = abs(delta.copy())
        down_days[delta > 0] = 0.0
        RS_up = up_days.rolling(window).mean()
        RS_down = down_days.rolling(window).mean()
        rsi = 100 - 100 / (1 + RS_up / RS_down)
        return rsi[-1] <= rsi_threshold

    def indicator_macd(self) -> bool:
        """Helper function to check for MACD Indicator.

        Rule: MACD greater than Signal Line."""
        exp1 = self.stock_data.close.ewm(span=12, adjust=False).mean()
        exp2 = self.stock_data.close.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        exp3 = macd.ewm(span=9, adjust=False).mean()
        return macd[-1] > exp3[-1]

    def get_bullish_indicators(self) -> bull_indicators:
        """Helper function to extract bullish Indicators."""
        indicator_response = bull_indicators(
            cross_mov_avg=self.cross_moving_avg(),
            macd=self.indicator_macd(),
            rsi=self.indicator_macd(),
            mov_avg=self.moving_avg(),
        )
        return indicator_response

    def get_indicators_response(
        self, request: request_indicator_module
    ) -> response_indicator_module:
        """Helper function handles response of Bullish Indicators."""
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
        indicator_response = response_indicator_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            time_period=f"{request.period}{request.time_frame}",
            bull_indicators=self.get_bullish_indicators(),
            cur_market_price=cur_market_price,
        )
        return indicator_response
