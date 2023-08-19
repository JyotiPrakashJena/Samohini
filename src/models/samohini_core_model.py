from pydantic import BaseModel


class PySelectedTradeTable(BaseModel):
    """Stocks Selected to be Traded added to the trade_selection_table."""
    stock_id : str
    stock_name : str
    buy_price : float
    stoploss : float
    target : float
    expected_profit : float
    expected_loss : float
    exp_risk_reward_ratio : float

    class Config:
        from_attributes = True


class PyExecutedTradeTable(BaseModel):
    """Stocks actual Executed added to the trade_executed table."""

    stock_id : str
    stock_name : str
    buy_price : float
    stoploss : float
    current_market_price : float #Updated for every executions
    target : float
    profit_till_now : float
    loss_till_now : float
    profit_check : bool
    loss_check : bool

    class Config:
        from_attributes = True