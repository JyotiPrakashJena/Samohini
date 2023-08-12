from pydantic import BaseModel, Field
from typing import Optional

class bull_indicators(BaseModel):
    """
    Object with details of the Bullish indicators.
    """
    cross_mov_avg: bool
    macd: bool
    mov_avg: bool
    rsi: bool


class request_indicator_module(BaseModel):
    """
    Request Object contained for the indicator Module
    """
    stock_id: str
    stock_name: Optional[str]
    period: int = Field(default=1)
    time_frame: str = Field(default='y')
    market: str = Field(default="NSE")


class response_indicator_module(BaseModel):
    """
    Response Object contained for the indicator Module
    """
    stock_id: str
    stock_name: Optional[str]
    time_period: str
    market: str = Field(default="NSE")
    bull_indicators: bull_indicators
