from pydantic import BaseModel, Field
from typing import Optional, Any

from models.candlestick_model import response_candle_module
from models.indicators_model import response_indicator_module
from models.support_resistance_model import response_SR_module
from models.fibo_model import response_fibo_module
from models.volume_model import response_volume_module

import pandas as pd


class request_all_screener_details(BaseModel):
    """
    Request Object contained for the response_all_screener_details
    """

    stock_id: str
    stock_name: str
    period: int = Field(default=1)
    time_frame: str = Field(default="y")
    market: str = Field(default="NSE")
    stock_data: Any = pd.DataFrame()


class response_all_screener_details(BaseModel):
    """
    Response Object contained for the response_all_screener_details
    """

    stock_id: str
    stock_name: Optional[str]
    time_period: str
    market: str = Field(default="NSE")
    candle_stick_response: response_candle_module
    indicator_response: response_indicator_module
    fibo_response: response_fibo_module
    sr_response: response_SR_module
    volume_response: response_volume_module


class response_bull_buy_call(BaseModel):
    """Object with details of stock to be traded."""

    stock_id: str
    stock_name: Optional[str]
    cur_market_price: float
    stoploss: float
    target: float
    expected_profit: float
    expected_loss: float
    exp_risk_reward_ratio: float
