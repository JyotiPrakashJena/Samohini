from pydantic import BaseModel, Field
from datetime import datetime

import pytz


class request_stock_data(BaseModel):
    """Request Object for Stock Data."""

    stock_id: str
    period: int
    time_frame: str


class request_stock_data_by_start_end_date(BaseModel):
    """Request to fetch details by start and end date."""

    stock_id: str
    start_date: str
    end_date: str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y")
    period: int = Field(default=1)
    time_frame: str = Field(default="d")


class request_stock_data_by_period(BaseModel):
    """Request to fetch details by period."""

    stock_id: str
    back_in_period: int
    period: int
    time_frame: str
    end_day_period: int = Field(default=0)
    end_date: str = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%d-%m-%Y")
