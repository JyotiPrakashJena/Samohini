from pydantic import BaseModel, Field
from typing import Optional, Any
from pandas import DataFrame


class stock_levels(BaseModel):
    """Object for maintaining Stock levels along with the ratio."""

    ratio: float
    level: float


class current_market_price(BaseModel):
    """Object to hold the current market price."""

    open: float
    price_now: float
    low: float
    high: float


class request_fibo_module(BaseModel):
    """
    Request Object contained for the Fibo Module
    """

    stock_id: str
    stock_name: Optional[str]
    period: int = Field(default=1)
    time_frame: str = Field(default="y")
    market: str = Field(default="NSE")
    stock_data: Any = DataFrame()


class response_fibo_module(BaseModel):
    """
    Response Object contained for the Fibo Module
    """

    stock_id: str
    stock_name: Optional[str]
    time_period: str
    market: str = Field(default="NSE")
    levels: list[stock_levels]
    cur_market_price: current_market_price
