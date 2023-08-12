from pydantic import BaseModel, Field
from typing import Optional

class bull_candles(BaseModel):
    """
    Object with details of the Bullish Candles.
    """
    bull_engulf: bool
    bull_harami: bool
    bull_pinbar: bool
    bull_inverted_hammer: bool
    bull_green_marubozu: bool
    bull_morning_star: bool
    bull_piercing_pattern: bool


class request_candle_module(BaseModel):
    """
    Request Object contained for the candle Module
    """
    stock_id: str
    stock_name: Optional[str]
    period: int = Field(default=1)
    time_frame: str = Field(default='y')
    market: str = Field(default="NSE")


class response_candle_module(BaseModel):
    """
    Response Object contained for the candle Module
    """
    stock_id: str
    stock_name: Optional[str]
    time_period: str
    market: str = Field(default="NSE")
    bullish_candles: bull_candles
