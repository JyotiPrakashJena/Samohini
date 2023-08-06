from pydantic import BaseModel, Field

class stock_levels(BaseModel):
    """Object for maintaining Stock levels along with the ratio."""
    ratio: float
    level: float

class request_fibo_module(BaseModel):
    """
    Request Object contained for the Fibo Module
    """
    stock_id: str
    stock_name: str
    period: int = Field(default=3)
    market: str = Field(default="NSE")

class response_fibo_module(BaseModel):
    """
    Response Object contained for the Fibo Module
    """
    stock_id: str
    stock_name: str
    period: int
    market: str
    levels: list[stock_levels]
