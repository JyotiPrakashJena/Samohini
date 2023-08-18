from candlestick import candlestick as cs
from utils.candlestick import average_body, stock_ratio
from utils.extras import format_float
from models.candlestick_model import (
    bull_candles,
    current_market_price,
    request_candle_module,
    response_candle_module,
)
from models.stock import request_stock_data
from module_stock.stock import StockDetails


class BullCandleStick:
    """Class with functionality for detection of Bullish Pattern."""

    def bull_engulf(self) -> bool:
        """Helper function to detect Bullish Engulf Pattern."""
        data = cs.bullish_engulfing(self.stock_data, target="result")
        return data["result"][-1]

    def bull_harami(self) -> bool:
        """Helper function to detect Bullish Harami Pattern."""
        data = cs.bullish_harami(self.stock_data, target="result")
        return data["result"][-1]

    def bull_pinbar(self) -> bool:
        """Helper function to detect Bullish PinBar Pattern."""
        current = self.stock_data.iloc[-1]

        prev = self.stock_data.iloc[-2]
        realbody = abs(current["open"] - current["close"])
        candle_range = current["high"] - current["low"]
        return (
            realbody <= candle_range / 3
            and min(current["open"], current["close"])
            > (current["high"] + current["low"]) / 2
            and current["low"] < prev["low"]
        )

    def bull_inverted_hammer(self) -> bool:
        """Helper function to detect Bullish Inverted Hammer Pattern."""
        data = cs.inverted_hammer(self.stock_data, target="result")
        return data["result"][-1]

    def bull_green_marubozu(self) -> bool:
        """Helper function to detect Bullish Green Marubozu Candle Pattern."""
        current = self.stock_data.iloc[-1]
        realbody = abs(current["open"] - current["close"])
        return (
            stock_ratio(current["open"], current["low"]) < 0.0015
            and stock_ratio(current["high"], current["close"]) < 0.0015
            and realbody
            >= average_body(self.stock_data["open"], self.stock_data["close"])
        )

    def bull_morning_star(self) -> bool:
        """Helper function to detect Bullish Morning Star Pattern."""
        data = cs.morning_star(self.stock_data, target="result")
        return data["result"][-1]

    def bull_piercing_pattern(self) -> bool:
        """Helper function to detect Bullish Morning Star Pattern."""
        data = cs.piercing_pattern(self.stock_data, target="result")
        return data["result"][-1]

    def get_bullish_candles(self) -> bool:
        """Helper function to extract bullish candles."""
        candle_response = bull_candles(
            bull_engulf=self.bull_engulf(),
            bull_harami=self.bull_harami(),
            bull_pinbar=self.bull_pinbar(),
            bull_inverted_hammer=self.bull_inverted_hammer(),
            bull_green_marubozu=self.bull_green_marubozu(),
            bull_morning_star=self.bull_morning_star(),
            bull_piercing_pattern=self.bull_piercing_pattern(),
        )
        return candle_response

    def get_candle_bull_response(
        self, request: request_candle_module
    ) -> response_candle_module:
        """Helper function handles response of Bullish candlestick."""
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
        candle_bull_response = response_candle_module(
            stock_id=request.stock_id,
            stock_name=request.stock_name,
            time_period=f"{request.period}{request.time_frame}",
            bullish_candles=self.get_bullish_candles(),
            cur_market_price=cur_market_price,
        )
        return candle_bull_response
