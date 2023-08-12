from pydantic import BaseModel, Field
from typing import Optional


class request_risk_reward_module(BaseModel):
    """
    Request Object contained for the risk_reward Module
    """
    buy_price: float
    sell_price: float
    stop_loss: float
    rr_ratio: float

class response_risk_reward_module(BaseModel):
    """
    Response Object contained for the risk_reward Module
    """
    buy_price: float
    sell_price: float
    stop_loss: float
    rr_ratio: float
    exp_risk_reward: float
    risk_reward_check: bool
