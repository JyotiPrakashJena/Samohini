from pydantic import BaseModel, Field
from typing import Optional


class volume_indicators(BaseModel):
    """
    Object with details of the Volume indicators.
    """
    volume_now: float
    avg_volume: float
    vol_indicator_check: bool


class current_market_price(BaseModel):
    """Object to hold the current market price."""
    open: float
    price_now: float
    low: float
    high: float


class request_volume_module(BaseModel):
    """
    Request Object contained for the volume Module
    """
    stock_id: str
    stock_name: Optional[str]
    period: int = Field(default=1)
    time_frame: str = Field(default='y')
    market: str = Field(default="NSE")


class response_volume_module(BaseModel):
    """
    Response Object contained for the volume Module
    """
    stock_id: str
    stock_name: Optional[str]
    time_period: str
    market: str = Field(default="NSE")
    volume_indicators: volume_indicators
    cur_market_price: current_market_price
