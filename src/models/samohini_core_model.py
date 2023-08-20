from pydantic import BaseModel

from datetime import datetime


class PySelectedTradeTable(BaseModel):
    """Stocks Selected to be Traded added to the trade_selection_table."""

    stock_id: str
    stock_name: str
    buy_price: float
    stoploss: float
    target: float
    expected_profit: float
    expected_loss: float
    exp_risk_reward_ratio: float

    class Config:
        from_attributes = True


class PyExecutedTradeTable(BaseModel):
    """Stocks actual Executed added to the trade_executed table."""

    stock_id: str
    stock_name: str
    buy_price: float
    stoploss: float
    current_market_price: float  # Updated for every executions
    target: float
    profit_till_now: float = 0
    loss_till_now: float = 0
    profit_check: bool = False
    loss_check: bool = False

    class Config:
        from_attributes = True


class PyProfitExecutedTable(BaseModel):
    """Model to hold details of Stocks which gave profit."""

    stock_id: str
    stock_name: str
    buy_price: float
    sell_price: float
    curr_price: float
    target: float
    loss: float
    booked_profit: float
    trade_date: datetime


class PyLossExecutedTable(BaseModel):
    """Model to hold details of Stocks which gave Loss."""

    stock_id: str
    stock_name: str
    buy_price: float
    sell_price: float
    curr_price: float
    target: float
    loss: float
    booked_loss: float
    trade_date: datetime
