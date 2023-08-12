from pydantic import BaseModel, Field
from typing import Optional


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
    time_frame: str = Field(default='y')
    market: str = Field(default="NSE")


class response_SR_module(BaseModel):
    """
    Response Object contained for the SR Module
    """
    stock_id: str
    stock_name: Optional[str]
    time_period: str
    market: str = Field(default="NSE")
    levels: list[float]
