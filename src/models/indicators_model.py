from pydantic import BaseModel, Field
from typing import Optional, Any
from pandas import DataFrame


class bull_indicators(BaseModel):
    """
    Object with details of the Bullish indicators.
    """

    cross_mov_avg: bool
    macd: bool
    mov_avg: bool
    rsi: bool


class current_market_price(BaseModel):
    """Object to hold the current market price."""

    open: float
    price_now: float
    low: float
    high: float


class request_indicator_module(BaseModel):
    """
    Request Object contained for the indicator Module
    """

    stock_id: str
    stock_name: Optional[str]
    period: int = Field(default=1)
    time_frame: str = Field(default="y")
    market: str = Field(default="NSE")
    stock_data: Any = DataFrame()


class response_indicator_module(BaseModel):
    """
    Response Object contained for the indicator Module
    """

    stock_id: str
    stock_name: Optional[str]
    time_period: str
    market: str = Field(default="NSE")
    bull_indicators: bull_indicators
    cur_market_price: current_market_price
