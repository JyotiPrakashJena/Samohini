from pydantic import BaseModel, Field
from typing import Optional, Any
from pandas import DataFrame


# class sr_levels(BaseModel):
#     """Object for maintaining Stock levels along with the ratio."""
#     level: float


class request_SR_module(BaseModel):
    """
    Request Object contained for the SR Module
    """

    stock_id: str
    stock_name: Optional[str]
    period: int = Field(default=1)
    time_frame: str = Field(default="y")
    market: str = Field(default="NSE")
    stock_data: Any = DataFrame()


class current_market_price(BaseModel):
    """Object to hold the current market price."""

    open: float
    price_now: float
    low: float
    high: float


class response_SR_module(BaseModel):
    """
    Response Object contained for the SR Module
    """

    stock_id: str
    stock_name: Optional[str]
    time_period: str
    market: str = Field(default="NSE")
    levels: list[float]
    cur_market_price: current_market_price


class response_stock_sr(BaseModel):
    """Response Object containing details of stock like stoploss & target."""

    price_now: float
    stop_loss: float = Field(default=0)
    target: float = Field(default=0)
    sr_indicator: bool
