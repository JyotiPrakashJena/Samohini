from models.indicators_model import (
    bull_indicators,
    request_indicator_module,
    response_indicator_module
)
from module_stock.stock import StockDetails

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
        return self.stock_data['close'][-1] > fiftyEMA[-1]
    

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
        indicator_response = bull_indicators(cross_mov_avg=self.cross_moving_avg(),
                                          macd=self.indicator_macd(),
                                          rsi=self.indicator_macd(),
                                          mov_avg=self.moving_avg())
        return indicator_response


    def get_indicators_response(self, request: request_indicator_module) -> response_indicator_module:
        """Helper function handles response of Bullish Indicators."""
        self.stock_data = StockDetails().get_stock_data(stock_id=request.stock_id,
                                                        period=request.period,
                                                        time_frame=request.time_frame)
        indicator_response = response_indicator_module(stock_id=request.stock_id,
                                                         stock_name=request.stock_name,
                                                         time_period=f'{request.period}{request.time_frame}',
                                                         bull_indicators=self.get_bullish_indicators())
        return indicator_response
